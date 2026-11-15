
import json
import csv
from pathlib import Path

VIDEO_DIR = Path("videos")
TRANSCRIPT_DIR = Path("processed_jsons")

OUTPUT_FILE = Path("video_manifest.csv")

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".webm"}

# Create video lookup using filenames
video_lookup = {
    video.stem.casefold(): video.name
    for video in VIDEO_DIR.iterdir()
    if video.is_file()
    and video.suffix.lower() in VIDEO_EXTENSIONS
}

manifest = []
missing_videos = []

# Read all normalized transcripts
for transcript in sorted(TRANSCRIPT_DIR.glob("*.json")):

    with open(transcript, "r", encoding="utf-8") as f:
        data = json.load(f)

    video_name = video_lookup.get(
        transcript.stem.casefold()
    )

    if not video_name:
        missing_videos.append(transcript.name)
        continue

    manifest.append({
        "number": data.get("number", ""),
        "day": data.get("day", ""),
        "title": data.get("title", ""),
        "source_file": transcript.name,
        "video_file": video_name,
        "video_path": str(VIDEO_DIR / video_name),
        "youtube_url": ""
    })

# Save manifest as CSV
if manifest:
    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=manifest[0].keys()
        )

        writer.writeheader()
        writer.writerows(manifest)

print("Video manifest created!")
print("Total lectures:", len(manifest))
print("Missing videos:", len(missing_videos))
print("Output:", OUTPUT_FILE)

print("\nFirst three mappings:")

for item in manifest[:3]:
    print("\nLecture:", item["title"])
    print("Video:", item["video_file"])
    print("Path:", item["video_path"])
