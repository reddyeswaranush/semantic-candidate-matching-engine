# Semantic Candidate Matching Engine

AI-powered talent intelligence platform for semantic candidate discovery, hybrid ranking, and explainable hiring recommendations.

## Live Demo

Streamlit App:
https://semantic-candidate-matching-engine-uxggpfryj2kq3kta4bxawr.streamlit.app/

GitHub Repository:
https://github.com/reddyeswaranush/semantic-candidate-matching-engine

---

## Problem Statement

Traditional resume filtering systems rely heavily on keyword matching, causing highly relevant candidates to be overlooked when their resumes use different terminology.

This project uses semantic search and hybrid ranking to identify the most relevant candidates based on meaning rather than exact keyword matches.

---

## Features

* Semantic candidate search using BGE embeddings
* FAISS vector similarity retrieval
* Hybrid 11-signal ranking engine
* Query-aware role detection
* Explainable candidate reasoning
* Candidate upload through CSV or Excel
* Automatic embedding generation and index rebuilding
* Recruiter-friendly Streamlit dashboard
* CSV export for shortlisted candidates

---

## System Architecture

Job Description
→ BGE Embedding Generation
→ FAISS Vector Search
→ Top Semantic Matches
→ Hybrid 11-Signal Ranking Engine
→ Explainable Candidate Recommendations

---

## Tech Stack

### Machine Learning

* BAAI/bge-small-en-v1.5
* Sentence Transformers
* NumPy

### Vector Search

* FAISS IndexFlatIP
* Cosine Similarity Retrieval

### Backend

* Python
* JSON Storage Layer

### Frontend

* Streamlit

### Data Processing

* Pandas
* OpenPyXL

---

## Candidate Search Pipeline

### Step 1: Candidate Upload

Recruiters upload candidate data in CSV or Excel format.

Required fields:

* candidate_id
* current_title
* years_of_experience
* current_company
* skills

### Step 2: Embedding Generation

Each candidate profile is converted into a semantic representation using BGE embeddings.

Output:

* 384-dimensional embedding vector

### Step 3: Vector Indexing

Candidate embeddings are stored inside a FAISS vector index for efficient similarity search.

### Step 4: Semantic Retrieval

The job description is embedded and matched against all candidate embeddings using cosine similarity.

### Step 5: Hybrid Ranking

Retrieved candidates are ranked using multiple signals:

* Semantic Score
* Skill Match Score
* Experience Score
* Career Score
* Title Match Score
* Behavior Score
* Seniority Score
* Company Score
* Role Profile Matching
* Query-Aware Skill Alignment
* Final Weighted Ranking

### Step 6: Explainable Results

Each recommendation includes recruiter-friendly reasoning explaining why the candidate was selected.

---

## Example Use Cases

### Machine Learning Hiring

Find candidates with:

* Python
* Machine Learning
* NLP
* FAISS
* RAG
* PyTorch

### Data Analytics Hiring

Find candidates with:

* SQL
* Power BI
* Tableau
* Excel

### Frontend Hiring

Find candidates with:

* React
* TypeScript
* JavaScript
* Next.js

### Backend Hiring

Find candidates with:

* Python
* Java
* Docker
* Kubernetes
* PostgreSQL

---

## Deployment

The application is deployed using Streamlit Cloud.

The system supports:

* Candidate upload
* Semantic retrieval
* FAISS indexing
* Explainable ranking
* CSV export

---

## Future Improvements

* Multi-company workspaces
* PostgreSQL storage backend
* Candidate profile enrichment
* LLM-powered recruiter summaries
* Advanced analytics dashboard
* API-based integrations
* Authentication and role-based access

---

## Author

Reddy Eswar Anush

B.Tech Computer Science & Engineering

National Institute of Technology Agartala

GitHub:
https://github.com/reddyeswaranush

LinkedIn:
[www.linkedin.com/in/reddy-eswar-anush](http://www.linkedin.com/in/reddy-eswar-anush)
