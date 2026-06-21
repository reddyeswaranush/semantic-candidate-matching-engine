import re

ROLE_PROFILES = {
    "ai_ml": {
        "skills": {
            "python", "nlp", "llm", "faiss", "pinecone", "milvus",
            "qdrant", "retrieval", "ranking", "embeddings", "rag",
            "machine learning", "deep learning", "recommendation systems",
            "mlflow", "kubeflow", "pytorch", "tensorflow"
        },
        "good_titles": {
            "ai engineer", "ml engineer", "machine learning engineer",
            "data scientist", "nlp engineer", "ai specialist",
            "ai research engineer", "recommendation systems engineer",
            "search engineer"
        },
        "career_keywords": {
            "retrieval", "search", "recommendation", "ranking", "matching",
            "relevance", "embedding", "vector search", "machine learning",
            "model", "feature engineering", "inference", "training"
        },
        "exp_sweet_spot": (5, 9),
        "exp_acceptable": (3, 12),
    },
    "data_analytics": {
        "skills": {
            "sql", "python", "excel", "tableau", "power bi", "statistics",
            "data analysis", "pandas", "numpy", "looker", "spark",
            "data visualization", "a/b testing", "hypothesis testing"
        },
        "good_titles": {
            "data analyst", "business analyst", "analytics engineer",
            "data engineer", "bi developer", "reporting analyst"
        },
        "career_keywords": {
            "analytics", "dashboard", "reporting", "insights", "kpi",
            "metrics", "sql", "visualization", "forecast", "trend analysis"
        },
        "exp_sweet_spot": (2, 6),
        "exp_acceptable": (1, 10),
    },
    "frontend": {
        "skills": {
            "react", "javascript", "typescript", "html", "css", "vue",
            "angular", "next.js", "tailwind", "redux", "webpack", "figma"
        },
        "good_titles": {
            "frontend engineer", "ui engineer", "web developer",
            "react developer", "javascript developer", "ui/ux engineer"
        },
        "career_keywords": {
            "frontend", "ui", "react", "javascript", "responsive",
            "web", "component", "dom", "browser", "performance"
        },
        "exp_sweet_spot": (2, 6),
        "exp_acceptable": (1, 10),
    },
    "backend": {
        "skills": {
            "python", "java", "go", "node.js", "sql", "postgresql",
            "mongodb", "redis", "kafka", "docker", "kubernetes",
            "rest api", "microservices", "aws", "system design"
        },
        "good_titles": {
            "backend engineer", "software engineer", "sde", "sde-2",
            "platform engineer", "api engineer", "server-side engineer"
        },
        "career_keywords": {
            "api", "backend", "microservices", "database", "server",
            "scalability", "latency", "throughput", "system design"
        },
        "exp_sweet_spot": (3, 8),
        "exp_acceptable": (1, 12),
    },
    "generic": {
        "skills": set(),
        "good_titles": set(),
        "career_keywords": set(),
        "exp_sweet_spot": (3, 8),
        "exp_acceptable": (1, 15),
    }
}

GOOD_DEGREES = {
    "computer science", "artificial intelligence", "machine learning",
    "data science", "information technology", "software engineering",
    "electronics", "mathematics", "statistics"
}

BAD_TITLES = {
    "hr manager", "marketing manager", "graphic designer",
    "customer support", "civil engineer", "mechanical engineer",
    "content writer", "sales executive", "operations manager"
}

CONSULTING_COMPANIES = {
    "tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini"
}

CERT_KEYWORDS = {
    "aws", "azure", "gcp", "machine learning", "tensorflow", "deep learning"
}

EVAL_KEYWORDS = {
    "ndcg", "mrr", "map", "evaluation", "benchmark",
    "a/b testing", "ab testing", "ranking metrics"
}


# --- query context detection ---

def detect_role_profile(query: str) -> dict:
    q = query.lower()

    scores = {
        "ai_ml": sum([
            "machine learning" in q, "ml" in q, "nlp" in q,
            "embedding" in q, "llm" in q, "retrieval" in q,
            "faiss" in q, "rag" in q, "ai engineer" in q
        ]),
        "data_analytics": sum([
            "analyst" in q, "analytics" in q, "sql" in q,
            "tableau" in q, "power bi" in q, "dashboard" in q,
            "business intelligence" in q
        ]),
        "frontend": sum([
            "frontend" in q, "react" in q, "javascript" in q,
            "ui engineer" in q, "css" in q, "next.js" in q
        ]),
        "backend": sum([
            "backend" in q, "api" in q, "microservices" in q,
            "java" in q, "node" in q, "system design" in q,
            "sde" in q
        ]),
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return ROLE_PROFILES["generic"]

    return ROLE_PROFILES[best]


def extract_query_skills(query: str) -> set:
    stopwords = {
        "a", "an", "the", "and", "or", "for", "with",
        "in", "of", "to", "is", "are", "senior", "junior",
        "strong", "good", "looking", "experience", "years"
    }
    words = re.findall(r"[a-zA-Z0-9.+#/-]+", query.lower())
    return {w for w in words if len(w) > 2 and w not in stopwords}


# --- individual scorers ---

def compute_skill_score(candidate, profile, query_skills=None):
    candidate_skills = {
        skill.get("name", "").lower()
        for skill in candidate.get("skills", [])
    }
    target_skills = profile["skills"] | (query_skills or set())
    if not target_skills:
        return 0.5
    matches = len(candidate_skills.intersection(target_skills))
    return min(matches / 5, 1.0)


def compute_title_score(candidate):
    title = candidate["profile"].get("current_title", "").lower()
    if title in BAD_TITLES:
        return 0.0
    return 0.3  # neutral default; boosted by profile match in final score


def compute_profile_title_score(candidate, profile):
    title = candidate["profile"].get("current_title", "").lower()
    if title in BAD_TITLES:
        return 0.0
    if title in profile["good_titles"]:
        return 1.0
    for good in profile["good_titles"]:
        if good in title or title in good:
            return 0.7
    return 0.3


def compute_education_score(candidate):
    education_text = " ".join(
        edu.get("degree", "").lower()
        for edu in candidate.get("education", [])
    )
    for degree in GOOD_DEGREES:
        if degree in education_text:
            return 1.0
    return 0.3


def compute_experience_score(candidate, profile):
    years = candidate["profile"].get("years_of_experience", 0)
    try:
        years = float(years)
    except Exception:
        years = 0
    lo, hi = profile["exp_sweet_spot"]
    alo, ahi = profile["exp_acceptable"]
    if lo <= years <= hi:
        return 1.0
    if alo <= years <= ahi:
        return 0.7
    return 0.3


def compute_behavior_score(candidate):
    signals = candidate.get("redrob_signals", {})
    github_score = signals.get("github_activity_score", 0) / 10
    response_rate = signals.get("recruiter_response_rate", 0)
    open_to_work = int(signals.get("open_to_work_flag", False))
    return min(0.4 * github_score + 0.4 * response_rate + 0.2 * open_to_work, 1.0)


def compute_career_signal_score(candidate, profile):
    career_text = " ".join(
        job.get("description", "").lower()
        for job in candidate.get("career_history", [])
    )
    keywords = profile["career_keywords"]
    if not keywords:
        return 0.5
    matches = sum(1 for kw in keywords if kw in career_text)
    return min(matches / 8, 1.0)


def compute_evaluation_score(candidate):
    career_text = " ".join(
        job.get("description", "").lower()
        for job in candidate.get("career_history", [])
    )
    matches = sum(1 for kw in EVAL_KEYWORDS if kw in career_text)
    return min(matches / 3, 1.0)


def compute_company_score(candidate):
    company = candidate["profile"].get("current_company", "").lower()
    return 0.0 if company in CONSULTING_COMPANIES else 1.0


def compute_seniority_score(candidate):
    title = candidate["profile"].get("current_title", "").lower()
    if any(w in title for w in ["senior", "staff", "lead", "principal", "head"]):
        return 1.0
    return 0.5


def compute_certification_score(candidate):
    certs = candidate.get("certifications", [])
    cert_text = " ".join(str(c).lower() for c in certs)
    matches = sum(1 for c in CERT_KEYWORDS if c in cert_text)
    return min(matches / 3, 1.0)


# --- final scorer ---

def compute_final_score(candidate, semantic_score, query=""):

    profile = detect_role_profile(query)
    query_skills = extract_query_skills(query)

    skill_score       = compute_skill_score(candidate, profile, query_skills)
    title_score       = compute_profile_title_score(candidate, profile)
    experience_score  = compute_experience_score(candidate, profile)
    behavior_score    = compute_behavior_score(candidate)
    career_score      = compute_career_signal_score(candidate, profile)
    evaluation_score  = compute_evaluation_score(candidate)
    company_score     = compute_company_score(candidate)
    education_score   = compute_education_score(candidate)
    certification_score = compute_certification_score(candidate)
    seniority_score   = compute_seniority_score(candidate)

    bad_title_penalty = 0.3 if title_score == 0.0 else 1.0

    final_score = (
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
    ) * bad_title_penalty

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