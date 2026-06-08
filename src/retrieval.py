import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from rec.src.config import (
    SAMPLE_CANDIDATES_FILE,
    EMBEDDINGS_FILE,
    INDEX_FILE
)

from rec.src.ranking import compute_final_score


def build_faiss_index():

    embeddings = np.load(
        EMBEDDINGS_FILE
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
        str(INDEX_FILE)
    )

    print(
        f"Index saved:\n{INDEX_FILE}"
    )

    return index


def load_candidates():

    with open(
        SAMPLE_CANDIDATES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def search_candidates(
    query,
    top_k=20
):

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
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

    candidates = load_candidates()

    results = []

    for i, idx in enumerate(indices[0]):

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
            "final_score": ranking_result["final_score"],
            "skill_score": ranking_result["skill_score"],
            "title_score": ranking_result["title_score"],
            "experience_score": ranking_result["experience_score"],
            "behavior_score": ranking_result["behavior_score"],
            "career_score": ranking_result["career_score"],
            "evaluation_score": ranking_result["evaluation_score"],
            "company_score": ranking_result["company_score"]
        })

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    print("\nHYBRID RANKING RESULTS\n")

    for rank, result in enumerate(
        results,
        start=1
    ):

        candidate = result["candidate"]

        skills = ", ".join([
            skill.get("name", "")
            for skill in candidate.get("skills", [])[:5]
        ])

        print(
            f"{rank}. "
            f"{candidate['candidate_id']} | "
            f"{candidate['profile']['current_title']} | "
            f"{candidate['profile']['years_of_experience']} years"
        )

        print(
            f"Final Score: "
            f"{result['final_score']:.4f}"
        )

        print(
            f"Semantic: "
            f"{result['semantic_score']:.4f}"
        )

        print(
            f"Skills: "
            f"{result['skill_score']:.4f}"
        )

        print(
            f"Title: "
            f"{result['title_score']:.4f}"
        )

        print(
            f"Experience: "
            f"{result['experience_score']:.4f}"
        )

        print(
            f"Behavior: "
            f"{result['behavior_score']:.4f}"
        )

        print(
            f"Career: "
            f"{result['career_score']:.4f}"
        )

        print(
            f"Evaluation: "
            f"{result['evaluation_score']:.4f}"
        )

        print(
            f"Company: "
            f"{result['company_score']:.4f}"
        )

        print(
            f"Top Skills: {skills}"
        )

        print("-" * 80)

    return results


if __name__ == "__main__":

    build_faiss_index()

    query = """
    Senior AI Engineer

    Strong Python

    Embeddings-based Retrieval Systems

    Ranking Systems

    Recommendation Systems

    Search Systems

    Information Retrieval

    Vector Databases

    Pinecone

    Weaviate

    Qdrant

    Milvus

    FAISS

    Evaluation Frameworks

    NDCG

    MRR

    MAP

    A/B Testing

    Production ML

    Machine Learning

    NLP

    Fine-tuning

    LLMs

    Product Engineering

    Candidate Matching

    Recruiter Search
    """

    search_candidates(
        query=query,
        top_k=20
    )