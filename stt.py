
import whisper
import json
from pathlib import Path

AUDIO_DIR = Path("audios")
OUTPUT_DIR = Path("whisper")

OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading Whisper large-v2...")
model = whisper.load_model("large-v2")

audio_files = sorted(AUDIO_DIR.glob("*.mp3"))

print(f"Found {len(audio_files)} audio files")

for index, audio_file in enumerate(audio_files, start=1):

    output_file = OUTPUT_DIR / f"{audio_file.stem}.json"

    if output_file.exists():
        print(f"Skipping: {audio_file.name}")
        continue

    print(f"\nTranscribing {index}/{len(audio_files)}")
    print(audio_file.name)

    result = model.transcribe(
        str(audio_file),
        language="en",
        fp16=False,
        verbose=False
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Saved: {output_file}")

print("\nAll transcriptions completed!")
