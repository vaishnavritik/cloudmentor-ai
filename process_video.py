
import os
import subprocess

VIDEO_DIR = "videos"
AUDIO_DIR = "audios"

os.makedirs(AUDIO_DIR, exist_ok=True)

video_files = [
    file for file in os.listdir(VIDEO_DIR)
    if file.lower().endswith(".mp4")
]

for index, file in enumerate(sorted(video_files), start=1):

    video_path = os.path.join(VIDEO_DIR, file)

    audio_name = os.path.splitext(file)[0] + ".mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_name)

    if os.path.exists(audio_path):
        print(f"Skipping existing audio: {audio_name}")
        continue

    print(f"\nConverting {index}/{len(video_files)}: {file}")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-b:a", "128k",
        "-y",
        audio_path
    ]

    subprocess.run(command, check=True)

    print(f"Saved: {audio_path}")

print("\nAll video conversions completed!")
