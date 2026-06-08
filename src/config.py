from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

PROCESSED_DIR = DATA_DIR / "processed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
INDEX_DIR = DATA_DIR / "indexes"

PROCESSED_DIR.mkdir(exist_ok=True)
EMBEDDINGS_DIR.mkdir(exist_ok=True)
INDEX_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_CANDIDATES_FILE = DATA_DIR / "sample_candidates.json"
CANDIDATES_FILE = DATA_DIR / "candidates.jsonl"

EMBEDDINGS_FILE = EMBEDDINGS_DIR / "sample_embeddings.npy"
INDEX_FILE = INDEX_DIR / "sample_index.faiss"
FULL_EMBEDDINGS_FILE = EMBEDDINGS_DIR / "full_embeddings.npy"
FULL_INDEX_FILE = INDEX_DIR / "full_index.faiss"