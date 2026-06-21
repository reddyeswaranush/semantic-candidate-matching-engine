import uuid


def csv_row_to_candidate(row):

    skills = []

    raw_skills = str(
        row.get(
            "skills",
            ""
        )
    )

    for skill in raw_skills.split(","):

        skill = skill.strip()

        if skill:

            skills.append(
                {
                    "name": skill
                }
            )

    candidate = {

        "candidate_id":
        row.get(
            "candidate_id",
            str(uuid.uuid4())
        ),

        "profile": {

            "current_title":
            row.get(
                "current_title",
                ""
            ),

            "headline": "",

            "summary": "",

            "years_of_experience":
            float(
                row.get(
                    "years_of_experience",
                    0
                )
            ),

            "current_company":
            row.get(
                "current_company",
                ""
            ),

            "current_industry":
            ""
        },

        "skills":
        skills,

        "career_history":
        [],

        "education":
        [],

        "certifications":
        [],

        "redrob_signals": {

            "github_activity_score":
            0,

            "open_to_work_flag":
            False,

            "recruiter_response_rate":
            0
        }
    }

    return candidate