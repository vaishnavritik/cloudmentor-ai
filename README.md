# CloudMentor AI – AWS & DevOps Learning Assistant

CloudMentor AI is a Retrieval-Augmented Generation (RAG) application
that helps learners understand AWS, DevOps, Docker, Kubernetes,
Terraform and cloud infrastructure concepts using recorded lecture
content.

It combines semantic search with Google's Gemini language model to
generate contextual answers and identify the original lecture sources.

## Features

- Ask questions about AWS and DevOps concepts in natural language.
- Retrieve relevant passages from recorded lectures.
- Generate contextual answers using Google Gemini.
- Semantic search using BGE-small embeddings.
- Display lecture titles, timestamps and similarity scores.
- Connect retrieved passages to original lecture videos.
- Play local lecture videos from relevant timestamps.
- Interactive Streamlit chat interface.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| LLM | Google Gemini |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Vector Operations | NumPy |
| Data Processing | Pandas |
| Embedding Storage | Joblib |
| Speech-to-Text | OpenAI Whisper |
| Audio Processing | FFmpeg |
| Environment Configuration | Python dotenv |

## RAG Architecture

```text
Recorded Lecture Videos
          |
          v
     FFmpeg Audio Extraction
          |
          v
       Whisper STT
          |
          v
    Transcript JSON Files
          |
          v
     Text Normalization
          |
          v
     RAG Chunk Creation
          |
          v
   BGE Embedding Generation
          |
          v
     Embedding Storage
          |
          v
       User Question
          |
          v
    Query Embedding
          |
          v
    Semantic Retrieval
          |
          v
   Relevant Lecture Chunks
          |
          v
      Gemini LLM
          |
          v
  Contextual Answer + Sources
          |
          v
       Streamlit UI

```

## Current Dataset

The current development dataset contains:

- 25 AWS and DevOps lecture videos.
- 13,106 transcript segments.
- 624 retrieval chunks.
- Approximately 320 target words per chunk.
- 45-word overlap between consecutive chunks.
- 384-dimensional BGE embeddings.
- Top-5 semantic retrieval using cosine similarity.

## Project Structure

```text
cloudmentor-ai/
├── app.py
├── rag_engine.py
├── config.py
├── requirements.txt
├── video_manifest.csv
├── README.md
├── .env.example
├── .gitignore
├── build_rag_chunks.py
├── normalize_whisper_json.py
├── validate_dataset.py
├── create_video_manifest.py
├── check_video_mapping.py
├── process_video.py
└── stt.py
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd cloudmentor-ai
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

```bash
cp .env.example .env
```

Edit `.env` and provide your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Never publish your actual API key.

### 5. Prepare the required data

The application expects:

- `embeddings.joblib` in the project root.
- `video_manifest.csv` in the project root.
- Corresponding MP4 files inside the `videos/` directory for video playback.

The embedding artifact and lecture videos are excluded from Git.

Generate or obtain the embedding artifact using the project's data preparation and embedding workflow before launching the application.

## Run the Application

```bash
streamlit run app.py
```

Open:

http://localhost:8501

## How Retrieval Works

1. The user submits a natural-language question.
2. BGE converts the question into an embedding.
3. NumPy calculates cosine similarity against stored embeddings.
4. The most relevant lecture chunks are retrieved.
5. Retrieved text is passed to Gemini as context.
6. Gemini generates a contextual answer.
7. Streamlit displays the answer and retrieved lecture sources.

## Future Improvements

- Introduce FAISS or ChromaDB for vector search.
- Improve retrieval using reranking and diversity techniques.
- Add retrieval evaluation and relevance thresholds.
- Support additional document collections.
- Deploy the application to a cloud platform.
- Add persistent chat history and user authentication.

## Security

- API credentials are stored in a local `.env` file.
- `.env` is excluded through `.gitignore`.
- Large media and embedding artifacts are not committed.
- Never publish private API keys or sensitive data.

## Author

**Vaishnav Srivastava**

Cloud Support Engineer | AWS | DevOps | AI/ML
