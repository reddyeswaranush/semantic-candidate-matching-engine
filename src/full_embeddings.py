import os
import numpy as np

from sentence_transformers import SentenceTransformer
from src.storage_manager import load_candidates
from src.preprocess import candidate_to_text
from src.config import FULL_EMBEDDINGS_FILE


def generate_full_embeddings(
    limit=None,
    chunk_size=5000
):

    print("Loading model...")

    model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

    print("Loading candidates...")

    candidates = load_candidates()

    if limit:
        candidates = candidates[:limit]

    print(
        f"Loaded {len(candidates)} candidates"
    )

    chunk_dir = "storage/embedding_chunks"
    os.makedirs(
        chunk_dir,
        exist_ok=True
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

        chunk_file = (
            f"{chunk_dir}/chunk_{start}_{end}.npy"
        )

        if os.path.exists(
            chunk_file
        ):

            print(
                f"Skipping {start} → {end}"
            )

            embeddings = np.load(
                chunk_file
            )

            all_embeddings.append(
                embeddings
            )

            continue

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

        np.save(
            chunk_file,
            embeddings
        )

        print(
            f"Saved {chunk_file}"
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
        "\nSaved embeddings:"
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