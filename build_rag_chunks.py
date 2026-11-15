
import json
from pathlib import Path

INPUT_DIR = Path("processed_jsons")
OUTPUT_DIR = Path("rag_chunks")

TARGET_WORDS = 320
OVERLAP_WORDS = 45

OUTPUT_DIR.mkdir(exist_ok=True)


def count_words(text):
    return len(text.split())


def create_chunks(segments):
    segments = [
        segment for segment in segments
        if segment.get("text", "").strip()
    ]

    chunks = []
    cursor = 0

    while cursor < len(segments):

        current_segments = []
        current_words = 0
        i = cursor

        # Collect complete Whisper segments
        while i < len(segments):
            segment = segments[i]
            text = segment["text"].strip()
            words = count_words(text)

            if current_segments and (
                current_words + words > TARGET_WORDS
            ):
                break

            current_segments.append(segment)
            current_words += words
            i += 1

            if current_words >= TARGET_WORDS:
                break

        # Build the chunk text
        chunk_text = " ".join(
            segment["text"].strip()
            for segment in current_segments
        )

        chunks.append({
            "start": current_segments[0]["start"],
            "end": current_segments[-1]["end"],
            "text": chunk_text,
            "word_count": count_words(chunk_text),
            "segment_count": len(current_segments)
        })

        if i >= len(segments):
            break

        # Retain trailing segments for overlap
        overlap_segments = []
        overlap_count = 0

        for segment in reversed(current_segments):
            words = count_words(segment["text"])

            if (
                overlap_segments
                and overlap_count + words > OVERLAP_WORDS
            ):
                break

            overlap_segments.insert(0, segment)
            overlap_count += words

            if overlap_count >= OVERLAP_WORDS:
                break

        next_cursor = i - len(overlap_segments)

        # Prevent an infinite loop
        if next_cursor <= cursor:
            next_cursor = i

        cursor = next_cursor

    return chunks


def main():

    files = sorted(INPUT_DIR.glob("*.json"))

    if not files:
        raise FileNotFoundError(
            f"No JSON files found inside {INPUT_DIR}"
        )

    total_chunks = 0
    total_words = 0

    for file in files:

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        segments = data.get("chunks", [])

        rag_chunks = create_chunks(segments)

        # Add lecture metadata to every chunk
        for index, chunk in enumerate(rag_chunks):

            chunk.update({
                "chunk_id": index,
                "number": data.get("number", "unknown"),
                "day": data.get("day", "unknown"),
                "title": data.get("title", file.stem),
                "source_file": file.name,
                "language": data.get("language", "unknown")
            })

        output_data = {
            "number": data.get("number", "unknown"),
            "day": data.get("day", "unknown"),
            "title": data.get("title", file.stem),
            "source_file": file.name,
            "language": data.get("language", "unknown"),
            "source_segment_count": len(segments),
            "chunks": rag_chunks
        }

        output_file = OUTPUT_DIR / file.name

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                output_data,
                f,
                indent=2,
                ensure_ascii=False
            )

        total_chunks += len(rag_chunks)
        total_words += sum(
            chunk["word_count"] for chunk in rag_chunks
        )

        print(
            f"Processed: {file.name} | "
            f"Segments: {len(segments)} | "
            f"RAG chunks: {len(rag_chunks)}"
        )

    print("\nChunking completed!")
    print("Lectures processed:", len(files))
    print("Original segments:", sum(
        json.load(open(file, encoding="utf-8"))["source_segment_count"]
        for file in OUTPUT_DIR.glob("*.json")
    ))
    print("Total RAG chunks:", total_chunks)
    print("Total chunk words (including overlap):", total_words)
    print("Average words per chunk:", round(total_words / total_chunks, 2))
    print("Output directory:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
