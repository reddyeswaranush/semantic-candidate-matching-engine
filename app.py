import streamlit as st

from src.full_retrieval import search_candidates
from src.reasoning import (
    generate_reasoning
)

st.set_page_config(
    page_title="Candidate Discovery System",
    layout="wide"
)

st.title(
    "Intelligent Candidate Discovery & Ranking System"
)

st.write(
    "Paste a Job Description and retrieve the most relevant candidates."
)

query = st.text_area(
    "Job Description",
    height=250
)

top_k = st.slider(
    "Number of Candidates",
    min_value=5,
    max_value=50,
    value=10
)

if st.button("Find Candidates"):

    if not query.strip():

        st.warning(
            "Please enter a job description."
        )

    else:

        with st.spinner(
            "Searching candidates..."
        ):

            results = search_candidates(
                query=query,
                limit=None,
                top_k=top_k
            )

        st.success(
            f"Found {len(results)} candidates"
        )

        for rank, result in enumerate(
            results,
            start=1
        ):

            candidate = result[
                "candidate"
            ]

            with st.expander(
                f"{rank}. {candidate['candidate_id']} | "
                f"{candidate['profile']['current_title']}"
            ):

                st.write(
                    f"### Final Score: "
                    f"{result['final_score']:.4f}"
                )
                st.write(
                    f"**Semantic Score:** "
                    f"{result['semantic_score']:.4f}"
                )

                st.write(
                    f"**Experience:** "
                    f"{candidate['profile']['years_of_experience']} years"
                )

                st.write(
                    f"**Current Role:** "
                    f"{candidate['profile']['current_title']}"
                )

                skills = ", ".join(
                    skill.get("name", "")
                    for skill in candidate.get(
                        "skills",
                        []
                    )[:10]
                )

                st.write(
                    f"**Skills:** {skills}"
                )
                st.write(
                    f"**Reasoning:** "
                    f"{generate_reasoning(candidate)}"
                )