import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from rec.src.config import (
    FULL_EMBEDDINGS_FILE,
    FULL_INDEX_FILE
)

from rec.src.full_dataset import load_candidates
from rec.src.ranking import compute_final_score


def build_full_index():

    embeddings = np.load(
        FULL_EMBEDDINGS_FILE
    )

    embeddings = embeddings.astype(
        "float32"
    )

    faiss.normalize_L2(
        embeddings
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    faiss.write_index(
        index,
        str(FULL_INDEX_FILE)
    )

    print(
        f"Index saved:\n{FULL_INDEX_FILE}"
    )

    return index


def search_candidates(
    query,
    limit=None,
    top_k=20
):

    candidates = load_candidates(
        limit=limit
    )

    index = faiss.read_index(
        str(FULL_INDEX_FILE)
    )

    model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

    query = (
        "Represent this candidate search query: "
        + query
    )

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(
        query_embedding
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i, idx in enumerate(
        indices[0]
    ):

        candidate = candidates[idx]

        semantic_score = float(
            scores[0][i]
        )

        ranking_result = (
            compute_final_score(
                candidate,
                semantic_score
            )
        )

        results.append({
            "candidate": candidate,
            "semantic_score": semantic_score,
            **ranking_result
        })

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    print("\nTOP CANDIDATES\n")

    for rank, result in enumerate(
        results,
        start=1
    ):

        candidate = result[
            "candidate"
        ]

        print(
            f"{rank}. "
            f"{candidate['candidate_id']} | "
            f"{candidate['profile']['current_title']} | "
            f"{result['final_score']:.4f}"
        )

    return results


if __name__ == "__main__":

    build_full_index()

    query = """
    Senior AI Engineer

    Python

    Retrieval Systems

    Ranking Systems

    Recommendation Systems

    Search Systems

    Embeddings

    FAISS

    Pinecone

    Milvus

    Machine Learning

    NLP

    Evaluation Frameworks

    NDCG

    MRR

    Product Engineering
    """

    search_candidates(
        query=query,
        limit=None,
        top_k=500
    )