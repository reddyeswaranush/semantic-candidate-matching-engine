def generate_reasoning(candidate, query=""):

    profile = candidate.get("profile", {})

    title = profile.get(
        "current_title",
        "Professional"
    )

    years = profile.get(
        "years_of_experience",
        0
    )

    skills = [
        skill.get("name", "")
        for skill in candidate.get("skills", [])
        if skill.get("name")
    ]

    top_skills = skills[:5]

    skills_text = (
        ", ".join(top_skills)
        if top_skills
        else "relevant technologies"
    )

    query_lower = query.lower()

    matched_skills = []

    for skill in skills:

        if skill.lower() in query_lower:
            matched_skills.append(
                skill
            )

    matched_skills = matched_skills[:5]

    if matched_skills:

        matched_text = ", ".join(
            matched_skills
        )

        return (
            f"Candidate brings {years:.1f} years of experience as "
            f"{title}. Demonstrates expertise in {skills_text}. "
            f"Strong alignment with the role requirements through "
            f"experience in {matched_text}."
        )

    return (
        f"Candidate has {years:.1f} years of experience as "
        f"{title}. Strong expertise in {skills_text}. "
        f"Profile shows relevant technical capabilities "
        f"for the target role."
    )

if __name__ == "__main__":

    import json
    from src.config import SAMPLE_CANDIDATES_FILE

    with open(
        SAMPLE_CANDIDATES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        candidates = json.load(f)

    print(
        generate_reasoning(
            candidates[0]
        )
    )