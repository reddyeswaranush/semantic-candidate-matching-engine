import numpy as np

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from rec.src.full_dataset import load_candidates
from rec.src.preprocess import candidate_to_text
from rec.src.config import FULL_EMBEDDINGS_FILE


def generate_full_embeddings(
    limit=None,
    chunk_size=5000
):

    print("Loading model...")

    model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

    print("Loading candidates...")

    candidates = load_candidates(
        limit=limit
    )

    print(
        f"Loaded {len(candidates)} candidates"
    )

    all_embeddings = []

    for start in range(
        0,
        len(candidates),
        chunk_size
    ):

        end = min(
            start + chunk_size,
            len(candidates)
        )

        print(
            f"\nProcessing "
            f"{start} → {end}"
        )

        batch_candidates = (
            candidates[start:end]
        )

        texts = [
            candidate_to_text(c)
            for c in batch_candidates
        ]

        embeddings = model.encode(
            texts,
            batch_size=64,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        all_embeddings.append(
            embeddings
        )

    embeddings = np.vstack(
        all_embeddings
    )

    np.save(
        FULL_EMBEDDINGS_FILE,
        embeddings
    )

    print(
        f"\nSaved embeddings:"
    )

    print(
        embeddings.shape
    )

    return embeddings


if __name__ == "__main__":

    generate_full_embeddings(
        limit=None,
        chunk_size=5000
    )