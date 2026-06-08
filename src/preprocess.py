import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def candidate_to_text(candidate):
    """
    Convert a candidate JSON record into a single text document
    suitable for embeddings and semantic search.
    """

    profile = candidate.get("profile", {})

    title = profile.get("current_title", "")
    headline = profile.get("headline", "")
    summary = profile.get("summary", "")
    years_exp = profile.get("years_of_experience", "")
    current_company = profile.get("current_company", "")
    industry = profile.get("current_industry", "")

    # Skills
    skills = [
        skill.get("name", "")
        for skill in candidate.get("skills", [])
    ]
    skills_text = " ".join(skills)

    # Career History
    experiences = []

    for job in candidate.get("career_history", []):
        experiences.append(job.get("description", ""))

    experience_text = " ".join(experiences)

    # Education
    education = []

    for edu in candidate.get("education", []):
        degree = edu.get("degree", "")
        field = edu.get("field_of_study", "")

        education.append(
            f"{degree} in {field}"
        )

    education_text = " ".join(education)

    # Certifications
    certifications = []

    for cert in candidate.get("certifications", []):
        certifications.append(
            cert.get("name", "")
        )

    certifications_text = " ".join(certifications)

    # Redrob Signals
    signals = candidate.get("redrob_signals", {})

    github_score = signals.get(
        "github_activity_score",
        -1
    )

    open_to_work = signals.get(
        "open_to_work_flag",
        False
    )

    response_rate = signals.get(
        "recruiter_response_rate",
        0
    )

    candidate_text = f"""
Title: {title}

Headline:
{headline}

Years of Experience:
{years_exp}

Company:
{current_company}

Industry:
{industry}

Summary:
{summary}

Skills:
{skills_text}

Education:
{education_text}

Certifications:
{certifications_text}

Open To Work:
{open_to_work}

Github Activity:
{github_score}

Recruiter Response Rate:
{response_rate}

Experience:
{experience_text}
"""

    return candidate_text.strip()


if __name__ == "__main__":

    with open(
        DATA_DIR / "sample_candidates.json",
        "r",
        encoding="utf-8"
    ) as f:

        candidates = json.load(f)

    print(f"Loaded {len(candidates)} candidates\n")

    first_candidate = candidates[0]

    text = candidate_to_text(first_candidate)

    print("=" * 80)
    print(text)
    print("=" * 80)