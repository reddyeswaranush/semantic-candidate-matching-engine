from src.full_retrieval import search_candidates
from src.submission_generator import save_submission


def main():

    print("\n" + "=" * 60)
    print("INTELLIGENT CANDIDATE DISCOVERY PIPELINE")
    print("=" * 60)

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

    print("\nSearching candidates...")

    results = search_candidates(
        query=query,
        limit=None,
        top_k=50
    )

    print("\nGenerating submission file...")

    save_submission(
        results
    )

    print("\nPipeline completed successfully.")
    print(
        "\nOutput File:"
        "\noutputs/submission.csv"
    )


if __name__ == "__main__":
    main()