def generate_reasoning(candidate):

    title = candidate["profile"].get(
        "current_title",
        "Unknown"
    )

    years = candidate["profile"].get(
        "years_of_experience",
        0
    )

    skills = [
        skill.get("name", "")
        for skill in candidate.get("skills", [])[:5]
    ]

    skills_text = ", ".join(skills)

    return (
        f"{years} years of experience as {title}. "
        f"Strong technical skills including {skills_text}. "
        f"Profile demonstrates relevant experience for "
        f"AI, machine learning, retrieval, and ranking systems."
    )


if __name__ == "__main__":

    import json
    from rec.src.config import SAMPLE_CANDIDATES_FILE

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