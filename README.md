# Intelligent Candidate Discovery & Ranking System

## Overview

This project implements an AI-powered candidate discovery and ranking platform capable of identifying highly relevant candidates from a dataset containing 100,000+ profiles. The solution combines semantic retrieval using transformer-based embeddings with a hybrid ranking framework to generate accurate, scalable, and explainable candidate recommendations.

## Problem Statement

Traditional Applicant Tracking Systems (ATS) rely heavily on keyword matching, often failing to identify qualified candidates when terminology differs across resumes and job descriptions. This project addresses that challenge through semantic search and multi-signal ranking.

## Solution Architecture

Job Description

↓

Requirement Extraction

↓

BGE Embedding Generation

↓

FAISS Vector Search

↓

Top-K Candidate Retrieval

↓

Hybrid Ranking Engine

↓

Explainability Layer

↓

Final Candidate Recommendations

## Key Features

* Semantic candidate matching using transformer embeddings
* High-speed retrieval using FAISS vector indexing
* Hybrid multi-signal ranking framework
* Explainable candidate recommendations
* Scalable processing for 100K+ candidate profiles
* Automated submission generation pipeline

## Technology Stack

### AI & Retrieval

* BAAI/bge-small-en-v1.5
* Sentence Transformers
* FAISS

### Development

* Python
* NumPy
* JSON
* CSV

## Ranking Methodology

Candidates are evaluated using a weighted hybrid scoring framework combining:

* Semantic Similarity
* Technical Skills
* Current Role Relevance
* Experience Level
* Career History Signals
* Education
* Certifications
* Behavioral Signals
* Seniority Indicators

## Scalability Features

* Offline embedding generation
* Batch processing pipeline
* Chunk-based dataset processing
* FAISS vector indexing
* Efficient retrieval for large candidate datasets
* Support for 100,000+ profiles

## Repository Structure

```text
src/
├── preprocess.py
├── full_dataset.py
├── full_embeddings.py
├── full_retrieval.py
├── ranking.py
├── reasoning.py
├── submission_generator.py
└── run_pipeline.py

data/
├── sample_candidates.json
├── candidate_schema.json
├── sample_submission.csv
└── challenge documents
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Generate Embeddings

```bash
python src/full_embeddings.py
```

### Build Retrieval Index

```bash
python src/full_retrieval.py
```

### Generate Submission

```bash
python src/submission_generator.py
```

### Run Complete Pipeline

```bash
python src/run_pipeline.py
```

## Results

* Dataset Size: 100,000+ Candidates
* Embedding Model: BGE Small v1.5
* Vector Search: FAISS
* Retrieval Strategy: Semantic Search
* Ranking Strategy: Hybrid Multi-Signal Ranking
* Output: Explainable Candidate Recommendations

## Note

Large datasets, generated embeddings, and FAISS index files are excluded from the repository to reduce storage requirements. These artifacts can be regenerated using the provided pipeline scripts.
