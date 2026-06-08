import json
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from src.preprocess import candidate_to_text
from src.config import (
    SAMPLE_CANDIDATES_FILE,
    EMBEDDINGS_FILE
)


def load_candidates():
    with open(
        SAMPLE_CANDIDATES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def generate_embeddings():

    print("Loading candidates...")

    candidates = load_candidates()

    print(f"Loaded {len(candidates)} candidates")

    texts = []

    for candidate in tqdm(candidates):

        texts.append(
            candidate_to_text(candidate)
        )

    print("Loading embedding model...")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print(f"Embedding shape: {embeddings.shape}")

    np.save(
        EMBEDDINGS_FILE,
        embeddings
    )

    print(
        f"Embeddings saved to:\n{EMBEDDINGS_FILE}"
    )

    return embeddings


if __name__ == "__main__":

    generate_embeddings()