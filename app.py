import io
import csv
import streamlit as st
import os
from src.config import FULL_INDEX_FILE

from src.full_retrieval import search_candidates, build_full_index
from src.full_embeddings import generate_full_embeddings
from src.candidate_upload import load_csv, load_excel
from src.storage_manager import (replace_candidates,total_candidates)
from src.reasoning import generate_reasoning

# --- page config ---

st.set_page_config(
    page_title="Candidate Discovery System",
    page_icon="🔍",
    layout="wide"
)

# --- cached model (fixes reload on every search) ---

@st.cache_resource
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("BAAI/bge-small-en-v1.5")

load_model()  # warm up on app start

index_exists = os.path.exists(
    FULL_INDEX_FILE
)

# --- header ---

st.title("AI-Powered Talent Intelligence Platform")
st.caption("Semantic candidate discovery using BGE embeddings, "
    "FAISS retrieval, and explainable AI ranking.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Candidates Indexed",
        f"{total_candidates():,}"
    )

with col2:
    st.metric(
        "Embedding Model",
        "BGE"
    )

with col3:
    st.metric(
        "Search Engine",
        "FAISS"
    )

with col4:
    st.metric(
        "Ranking Engine",
        "11 Signals"
    )

# --- tabs ---

tab_search, tab_upload = st.tabs([
    "Search Candidates",
    "Upload Candidates"
])


# ── SEARCH TAB ──────────────────────────────────────────────

with tab_search:

    st.subheader("Find the Best Candidates")

    col1, col2 = st.columns([3, 1])

    with col1:
        query = st.text_area(
            "Paste Job Description",
            height=250,
            placeholder="e.g. Senior ML Engineer with experience in RAG, FAISS, Python..."
        )

    with col2:
        st.metric("Candidates in System", total_candidates())
        top_k = st.slider(
            "Number of Results",
            min_value=5,
            max_value=100,
            value=10
        )
        search_btn = st.button(
            "Find Candidates",
            use_container_width=True
        )

    if search_btn:

        if not query.strip():
            st.warning("Please enter a job description.")

        elif (total_candidates() == 0 or not os.path.exists(FULL_INDEX_FILE)):
            st.error(
                "No indexed candidates available. Upload candidates first."
            )

        else:
            with st.spinner("Searching candidates..."):
                results = search_candidates(
                    query=query,
                    top_k=top_k
                )

            st.success(f"Found {len(results)} candidates")

            # --- CSV download ---
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow([
                "rank", "candidate_id", "current_title",
                "years_experience", "final_score",
                "semantic_score", "skill_score", "reasoning"
            ])
            for rank, result in enumerate(results, start=1):
                c = result["candidate"]
                writer.writerow([
                    rank,
                    c["candidate_id"],
                    c["profile"]["current_title"],
                    c["profile"]["years_of_experience"],
                    round(result["final_score"], 4),
                    round(result["semantic_score"], 4),
                    round(result["skill_score"], 4),
                    generate_reasoning(c, query)
                ])

            st.download_button(
                label="Download Results as CSV",
                data=csv_buffer.getvalue(),
                file_name="shortlisted_candidates.csv",
                mime="text/csv"
            )

            st.divider()

            # --- results display ---
            for rank, result in enumerate(results, start=1):
                c = result["candidate"]
                skills = ", ".join(
                    s.get("name", "")
                    for s in c.get("skills", [])[:8]
                )

                with st.expander(
                    f"#{rank} — {c['profile']['current_title']} "
                    f"| {c['candidate_id']} "
                    f"| Score: {result['final_score']:.4f}"
                ):
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        st.metric("Final Score", f"{result['final_score']:.4f}")
                        st.metric("Semantic Score", f"{result['semantic_score']:.4f}")
                        st.metric("Skill Score", f"{result['skill_score']:.4f}")

                    with col_b:
                        st.metric("Experience Score", f"{result['experience_score']:.4f}")
                        st.metric("Career Score", f"{result['career_score']:.4f}")
                        st.metric("Title Score", f"{result['title_score']:.4f}")

                    with col_c:
                        st.metric("Behavior Score", f"{result['behavior_score']:.4f}")
                        st.metric("Seniority Score", f"{result['seniority_score']:.4f}")
                        st.metric("Company Score", f"{result['company_score']:.4f}")

                    st.markdown(f"**Experience:** {c['profile']['years_of_experience']} years")
                    st.markdown(f"**Current Company:** {c['profile'].get('current_company', 'N/A')}")
                    st.markdown(f"**Skills:** {skills}")
                    st.markdown(f"**Reasoning:** {generate_reasoning(c, query)}")


# ── UPLOAD TAB ──────────────────────────────────────────────

with tab_upload:

    st.subheader("Upload Candidate Data")
    st.info(
        "Upload a CSV or Excel file. "
        "Required columns: `candidate_id`, `current_title`, "
        "`years_of_experience`, `current_company`, `skills` (comma-separated)."
    )

    template_csv = """candidate_id,current_title,years_of_experience,current_company,skills
TEST001,ML Engineer,3,OpenAI,"Python,PyTorch,NLP"
TEST002,Data Scientist,4,Google,"Python,SQL,TensorFlow"
TEST003,AI Engineer,5,Microsoft,"FAISS,RAG,LangChain,Python"
"""

    st.download_button(
        label="📥 Download Candidate Template",
        data=template_csv,
        file_name="candidate_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader(
        "Choose file",
        type=["csv", "xlsx"]
    )

    if uploaded_file:

        file_name = uploaded_file.name

        with st.spinner("Parsing file..."):
            try:
                if file_name.endswith(".csv"):
                    candidates = load_csv(uploaded_file)
                else:
                    candidates = load_excel(uploaded_file)

                st.success(f"Parsed {len(candidates)} candidates from file.")

            except Exception as e:
                st.error(f"Failed to parse file: {e}")
                candidates = []

        if candidates:
            if st.button("Add to System & Rebuild Index", use_container_width=True):

                with st.spinner("Saving candidates..."):
                    replace_candidates(candidates)
                    total = len(candidates)

                with st.spinner("Generating embeddings..."):
                    generate_full_embeddings()

                with st.spinner("Rebuilding FAISS index..."):
                    build_full_index()

                st.success(
                    f"Done! Loaded {total} candidates into the system."
                )
                st.rerun()

    st.divider()
    st.metric("Total Candidates in System", total_candidates())