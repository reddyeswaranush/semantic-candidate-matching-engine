import csv

from src.full_retrieval import search_candidates
from src.reasoning import generate_reasoning

EXCLUDED_TITLES = {
    "sales executive",
    "operations manager",
    "content writer",
    "hr manager",
    "marketing manager",
    "mechanical engineer",
    "civil engineer",
    "customer support"
}


def save_submission(
    results,
    query="",
    output_file="outputs/submission.csv"
):

    filtered_results = []

    for result in results:

        title = (
            result["candidate"]["profile"]
            .get("current_title", "")
            .lower()
        )

        if title not in EXCLUDED_TITLES:
            filtered_results.append(
                result
            )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "rank",
            "candidate_id",
            "score",
            "reasoning"
        ])

        for rank, result in enumerate(
            filtered_results,
            start=1
        ):

            candidate = result[
                "candidate"
            ]

            writer.writerow([
                rank,
                candidate[
                    "candidate_id"
                ],
                round(
                    result[
                        "final_score"
                    ],
                    4
                ),
                generate_reasoning(candidate, query)
            ])

    print(
        f"\nSubmission saved:\n"
        f"{output_file}"
    )

    print(
        f"\nTotal shortlisted candidates: "
        f"{len(filtered_results)}"
    )


if __name__ == "__main__":

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

    results = search_candidates(
        query=query,
        limit=None,
        top_k=500
    )

    save_submission(
        results,
        query=query
    )