import json

from rec.src.config import SAMPLE_CANDIDATES_FILE


AI_SKILLS = {
    "python",
    "nlp",
    "llm",
    "faiss",
    "pinecone",
    "milvus",
    "qdrant",
    "retrieval",
    "ranking",
    "embeddings",
    "rag",
    "machine learning",
    "deep learning",
    "recommendation systems",
    "mlflow",
    "kubeflow"
}

GOOD_DEGREES = {
    "computer science",
    "artificial intelligence",
    "machine learning",
    "data science",
    "information technology",
    "software engineering"
}

GOOD_TITLES = {
    "ai engineer",
    "ml engineer",
    "machine learning engineer",
    "data scientist",
    "recommendation systems engineer",
    "search engineer",
    "nlp engineer",
    "software engineer",
    "backend engineer",
    "data engineer",
    "ai specialist",
    "ai research engineer"
}

BAD_TITLES = {
    "hr manager",
    "marketing manager",
    "graphic designer",
    "customer support",
    "civil engineer",
    "mechanical engineer",
    "frontend engineer"
}

CAREER_KEYWORDS = {
    "retrieval",
    "search",
    "recommendation",
    "ranking",
    "matching",
    "relevance",
    "personalization",
    "candidate matching",
    "information retrieval",
    "embedding",
    "vector search",
    "recommender",

    "machine learning",
    "ml",
    "model",
    "models",
    "feature pipeline",
    "feature engineering",
    "data pipeline",
    "data pipelines",
    "spark",
    "pyspark",
    "airflow",
    "training",
    "inference",
    "analytics",
    "prediction"
}

EVAL_KEYWORDS = {
    "ndcg",
    "mrr",
    "map",
    "evaluation",
    "benchmark",
    "benchmarking",
    "a/b testing",
    "ab testing",
    "ranking metrics"
}

CONSULTING_COMPANIES = {
    "tcs",
    "infosys",
    "wipro",
    "accenture",
    "cognizant",
    "capgemini"
}

CERT_KEYWORDS = {
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "tensorflow",
    "deep learning"
}


def compute_skill_score(candidate):

    candidate_skills = {
        skill.get("name", "").lower()
        for skill in candidate.get("skills", [])
    }

    matches = len(
        candidate_skills.intersection(
            AI_SKILLS
        )
    )

    return min(matches / 5, 1.0)


def compute_title_score(candidate):

    title = (
        candidate["profile"]
        .get("current_title", "")
        .lower()
    )

    if title in GOOD_TITLES:
        return 1.0

    if title in BAD_TITLES:
        return 0.0

    if any(
        word in title
        for word in [
            "manager",
            "analyst",
            "consultant",
            "coordinator",
            "sales",
            "marketing",
            "writer",
            "operations",
            "devops"
        ]
    ):
        return 0.0

    return 0.3


def compute_education_score(candidate):

    education_text = ""

    for edu in candidate.get(
        "education",
        []
    ):

        education_text += (
            edu.get("degree", "")
            .lower()
            + " "
        )

    for degree in GOOD_DEGREES:

        if degree in education_text:
            return 1.0

    return 0.3


def compute_experience_score(candidate):

    years = (
        candidate["profile"]
        .get("years_of_experience", 0)
    )

    try:
        years = float(years)
    except Exception:
        years = 0

    if 5 <= years <= 9:
        return 1.0

    if 3 <= years <= 12:
        return 0.7

    return 0.3


def compute_behavior_score(candidate):

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    github_score = signals.get(
        "github_activity_score",
        0
    )

    response_rate = signals.get(
        "recruiter_response_rate",
        0
    )

    open_to_work = signals.get(
        "open_to_work_flag",
        False
    )

    github_score = github_score / 10

    score = (
        0.4 * github_score +
        0.4 * response_rate +
        0.2 * int(open_to_work)
    )

    return min(score, 1.0)


def compute_career_signal_score(candidate):

    career_text = ""

    for job in candidate.get(
        "career_history",
        []
    ):

        career_text += (
            job.get(
                "description",
                ""
            ).lower()
            + " "
        )

    matches = 0

    for keyword in CAREER_KEYWORDS:

        if keyword in career_text:
            matches += 1

    return min(
        matches / 8,
        1.0
    )


def compute_evaluation_score(candidate):

    career_text = ""

    for job in candidate.get(
        "career_history",
        []
    ):
        career_text += (
            job.get(
                "description",
                ""
            ).lower()
            + " "
        )

    matches = sum(
        1
        for keyword in EVAL_KEYWORDS
        if keyword in career_text
    )

    return min(matches / 3, 1.0)


def compute_company_score(candidate):

    company = (
        candidate["profile"]
        .get(
            "current_company",
            ""
        )
        .lower()
    )

    if company in CONSULTING_COMPANIES:
        return 0.0

    return 1.0

def compute_seniority_score(candidate):

    title = (
        candidate["profile"]
        .get("current_title", "")
        .lower()
    )

    if "senior" in title:
        return 1.0

    if "staff" in title:
        return 1.0

    if "lead" in title:
        return 1.0

    return 0.5


def compute_certification_score(candidate):

    certs = candidate.get(
        "certifications",
        []
    )

    cert_text = " ".join(
        str(c).lower()
        for c in certs
    )

    matches = sum(
        1
        for cert in CERT_KEYWORDS
        if cert in cert_text
    )

    return min(matches / 3, 1.0)


def compute_final_score(
    candidate,
    semantic_score
):

    skill_score = (
        compute_skill_score(
            candidate
        )
    )

    title_score = (
        compute_title_score(
            candidate
        )
    )

    experience_score = (
        compute_experience_score(
            candidate
        )
    )

    behavior_score = (
        compute_behavior_score(
            candidate
        )
    )

    career_score = (
        compute_career_signal_score(
            candidate
        )
    )

    evaluation_score = (
        compute_evaluation_score(
            candidate
        )
    )

    company_score = (
        compute_company_score(
            candidate
        )
    )
    education_score = (
        compute_education_score(
            candidate
        )
    )
    certification_score = (
        compute_certification_score(
            candidate
        )
    )
    title = (
        candidate["profile"]
        .get("current_title", "")
        .lower()
    )

    seniority_score = compute_seniority_score(candidate)

    bad_title_penalty = 1.0

    if title in BAD_TITLES:
        bad_title_penalty = 0.3

    final_score = (
        (
            0.30 * semantic_score +
            0.15 * skill_score +
            0.15 * title_score +
            0.10 * experience_score +
            0.05 * behavior_score +
            0.10 * career_score +
            0.05 * evaluation_score +
            0.03 * company_score +
            0.03 * education_score +
            0.02 * certification_score +
            0.02 * seniority_score
        )
        * bad_title_penalty
    )

    return {
        "final_score": final_score,
        "skill_score": skill_score,
        "title_score": title_score,
        "experience_score": experience_score,
        "behavior_score": behavior_score,
        "career_score": career_score,
        "evaluation_score": evaluation_score,
        "company_score": company_score,
        "education_score": education_score,
        "certification_score": certification_score,
        "seniority_score": seniority_score
    }



if __name__ == "__main__":

    with open(
        SAMPLE_CANDIDATES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        candidates = json.load(f)

    candidate = candidates[0]

    result = compute_final_score(
        candidate,
        semantic_score=0.50
    )

    print("\nCandidate:")
    print(candidate["candidate_id"])
    print(candidate["profile"]["current_title"])

    print("\nScores:")

    for key, value in result.items():
        print(
            f"{key}: {value:.4f}"
        )