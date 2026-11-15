
import json
import re
from pathlib import Path

INPUT_DIR = Path("whisper")
OUTPUT_DIR = Path("processed_jsons")

OUTPUT_DIR.mkdir(exist_ok=True)

json_files = sorted(INPUT_DIR.glob("*.json"))

if not json_files:
    raise FileNotFoundError("No JSON files found in jsons/")

total_chunks = 0

for file in json_files:

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract lecture metadata from filename
    filename = file.name.removesuffix(".json").removesuffix(".mp3")

    parts = re.split(r"[｜|]", filename)
    prefix = parts[0].strip()

    number_match = re.match(r"(\d+)", prefix)
    day_match = re.search(r"Day[- ]*(\d+)", prefix, re.I)

    number = number_match.group(1) if number_match else "unknown"
    day = f"Day-{day_match.group(1)}" if day_match else "unknown"

    title = " | ".join(parts[1:]).strip() if len(parts) > 1 else filename

    chunks = []

    for segment in data.get("segments", []):

        text = segment.get("text", "").strip()

        if not text:
            continue

        chunks.append({
            "number": number,
            "day": day,
            "title": title,
            "start": segment.get("start", 0),
            "end": segment.get("end", 0),
            "text": text,
            "source_file": file.name,
            "language": data.get("language", "unknown")
        })

    normalized_data = {
        "number": number,
        "day": day,
        "title": title,
        "language": data.get("language", "unknown"),
        "source_file": file.name,
        "text": data.get("text", ""),
        "chunks": chunks
    }

    output_file = OUTPUT_DIR / file.name

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(normalized_data, f, indent=2, ensure_ascii=False)

    total_chunks += len(chunks)

    print(f"Processed: {file.name} | Chunks: {len(chunks)}")

print("\nNormalization completed!")
print("Files processed:", len(json_files))
print("Total chunks:", total_chunks)
print("Output directory:", OUTPUT_DIR)
