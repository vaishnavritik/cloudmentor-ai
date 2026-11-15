
from pathlib import Path
import json

VIDEO_DIR = Path("videos")
TRANSCRIPT_DIR = Path("processed_jsons")

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".webm"}

# Build a lookup of available video filenames
video_files = {
    video.stem.casefold(): video
    for video in VIDEO_DIR.iterdir()
    if video.is_file()
    and video.suffix.lower() in VIDEO_EXTENSIONS
}

transcript_files = sorted(TRANSCRIPT_DIR.glob("*.json"))

matched = 0
missing = 0

print("Checking transcript-to-video mapping...\n")

for transcript in transcript_files:

    video = video_files.get(transcript.stem.casefold())

    if video:
        matched += 1
        print(f"MATCH: {transcript.name}")
        print(f"VIDEO: {video.name}\n")
    else:
        missing += 1
        print(f"MISSING VIDEO: {transcript.name}\n")

print("=" * 50)
print("Total transcripts:", len(transcript_files))
print("Matched videos:", matched)
print("Missing videos:", missing)
