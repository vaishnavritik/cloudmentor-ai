
import os
from pathlib import Path
from dotenv import load_dotenv

# Root directory of our project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# Dataset locations
EMBEDDINGS_PATH = BASE_DIR / "embeddings.joblib"
VIDEO_MANIFEST_PATH = BASE_DIR / "video_manifest.csv"
VIDEO_DIR = BASE_DIR / "videos"

# Embedding configuration
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSION = 384
QUERY_INSTRUCTION = (
    "Represent this sentence for searching relevant passages: "
)

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

# Retrieval configuration
DEFAULT_TOP_K = 5
