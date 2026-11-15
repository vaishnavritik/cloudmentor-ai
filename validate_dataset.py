
import json
from pathlib import Path

files = sorted(Path("processed_jsons").glob("*.json"))

total_chunks = 0
empty_chunks = 0
missing_metadata = 0

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data.get("chunks", [])
    total_chunks += len(chunks)

    for chunk in chunks:
        if not chunk.get("text", "").strip():
            empty_chunks += 1

        if not all(k in chunk for k in [
            "title", "start", "end", "source_file"
        ]):
            missing_metadata += 1

print("Files:", len(files))
print("Total segments:", total_chunks)
print("Empty segments:", empty_chunks)
print("Missing metadata:", missing_metadata)
