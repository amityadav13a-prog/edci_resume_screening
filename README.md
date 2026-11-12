# Resume Matching & Screening Engine

An intelligent, end-to-end resume parsing, relationship extraction, and machine learning-powered candidate ranking engine designed to match candidates to Job Descriptions (JDs) with explainable evidence.

---

## System Architecture & Pipeline Flowchart

The system is designed around a multi-stage NLP and machine learning pipeline that progresses from raw multimodal document ingestion to structured profiles and Learning-to-Rank (LTR) scoring:

```text
                    ┌──────────────────────────┐
                    │      STUDENT RESUMES     │
                    │  PDF / DOCX / IMAGE etc. │
                    └────────────┬─────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│ 1. DOCUMENT INGESTION                                   │
│                                                         │
│ PDF / DOCX / Image → common ParsedDocument              │
│                                                         │
│ Text + Page + Position + Font + Bold + Layout           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. ENTITY EXTRACTION                                    │
│                                                         │
│ Resume text → entities                                  │
│                                                         │
│ PERSON        Google                                    │
│ COMPANY       Software Engineer                         │
│ JOB_TITLE     Python                                    │
│ TECHNOLOGY    AWS                                       │
│ DEGREE        B.Tech                                    │
│ PROJECT       ...                                       │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. RELATIONSHIP EXTRACTION                              │
│                                                         │
│ "Software Engineer" ──WORKED_AT──> Google               │
│ "Engineer" ──USED_TECHNOLOGY──> Python                  │
│ "Project X" ──PROJECT_USES──> React                     │
│                                                         │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. NORMALIZATION                                        │
│                                                         │
│ AWS                  → AWS                              │
│ Amazon Web Services  → AWS                              │
│ K8s                  → Kubernetes                       │
│ Kubernetes           → Kubernetes                       │
│ ReactJS              → React                            │
│                                                         │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 5. STUDENT PROFILE                                      │
│                                                         │
│ StudentProfile                                          │
│   ├── Personal information                              │
│   ├── Skills                                            │
│   ├── Employment                                        │
│   ├── Education                                         │
│   ├── Projects                                          │
│   ├── Certifications                                    │
│   └── Achievements                                      │
│                                                         │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │   DATABASE   │
                    │  PostgreSQL  │
                    │  + pgvector  │
                    └──────┬───────┘
                           │
                           │ COMPANY POSTS JD
                           ▼
┌─────────────────────────────────────────────────────────┐
│ 6. JOB DESCRIPTION INGESTION                            │
│                                                         │
│ JD text → JD entities + requirements                    │
│                                                         │
│ Required Skill                                          │
│ Preferred Skill                                         │
│ Experience                                              │
│ Education                                               │
│ Certification                                           │
│ Responsibilities                                        │
│ Domain                                                  │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 7. RESUME ↔ JD FEATURE GENERATION                       │
│                                                         │
│ Student + JD                                            │
│        ↓                                                │
│ Matching features                                       │
│                                                         │
│ Skill match                                             │
│ Experience match                                        │
│ Education match                                         │
│ Domain match                                            │
│ Technology match                                        │
│ Semantic similarity                                     │
│ Experience gap                                          │
│ etc.                                                    │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 8. LEARNING-TO-RANK MODEL                               │
│                                                         │
│ LightGBM LambdaMART                                     │
│                                                         │
│ Input: matching features                                │
│ Output: candidate relevance score                       │
│                                                         │
│ (No arbitrary manual weights like 40% skills + 30% exp) │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 9. RANKING                                              │
│                                                         │
│ Candidate A → 0.91 → Rank #1                            │
│ Candidate B → 0.86 → Rank #2                            │
│ Candidate C → 0.79 → Rank #3                            │
│ ...                                                     │
│                                                         │
│ → Top 10 / Top 20 Candidates                            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 10. EXPLANATION                                         │
│                                                         │
│ Why Candidate A ranked highly                           │
│                                                         │
│ ✓ Python                                                │
│ ✓ AWS                                                   │
│ ✓ 3 years relevant experience                           │
│ ✓ Required degree                                       │
│ ✓ Relevant project                                      │
│                                                         │
│ + Evidence extracted from actual resume text            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │   BACKEND    │
                    │     API      │
                    │   FastAPI    │
                    └──────┬───────┘
                           │
                           ▼
                   COMPANY DASHBOARD
```

---

## Pipeline Overview

1. **Document Ingestion (`src/ingestion`)**: Converts multimodal files (PDF, DOCX, scanned images) into unified parsed documents preserving textual content, structure, and metadata.
2. **Entity Extraction / NER (`src/extraction`)**: Identifies core resume entities (`PERSON`, `COMPANY`, `JOB_TITLE`, `TECHNOLOGY`, `DEGREE`, `PROJECT`, `SKILLS`, etc.) using custom GPU-accelerated spaCy NER models and deterministic extractors.
3. **Relationship Extraction (`src/extraction`)**: Links entities contextually (e.g., `WORKED_AT`, `USED_TECHNOLOGY`, `PROJECT_USES`) using proximity analysis and syntactic dependency patterns.
4. **Technology Normalization (`src/normalization`)**: Maps synonyms, acronyms, and aliases to canonical standards (e.g., `K8s` $\rightarrow$ `Kubernetes`, `AWS` $\rightarrow$ `Amazon Web Services`).
5. **Student Profile Modeling (`src/profiles`)**: Assembles normalized entities and relationships into an immutable, structured candidate profile stored in PostgreSQL with `pgvector` embeddings.
6. **Job Description Ingestion**: Parses incoming JDs to extract required/preferred skills, required experience levels, education constraints, and responsibilities.
7. **Feature Generation**: Computes comprehensive matching vectors between candidate profiles and job requirements (semantic embeddings similarity, hard-skill coverage, experience overlap, degree matches).
8. **Learning-to-Rank (LTR)**: Trains and evaluates a **LightGBM LambdaMART** ranking model to dynamically score candidate relevance instead of using arbitrary manual heuristics.
9. **Candidate Ranking**: Generates calibrated relevance scores and presents ranked shortlists (Top 10 / Top 20).
10. **Explainable AI & Dashboard**: Produces human-interpretable justifications and verbatim resume evidence for recruiters via a **FastAPI** backend and responsive frontend dashboard.

---

## Project Structure

```text
resume_matching_engine/
│
├── data/
│   ├── resumes/            # Candidate resumes (PDF, DOCX, images)
│   ├── jds/                # Job Descriptions
│   └── ner/                # NER annotation & training datasets (git-ignored)
│
├── models/
│   └── resume_ner/         # Trained spaCy NER model artifacts (git-ignored)
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Central configuration and paths
│   ├── main.py             # CLI entry point
│   │
│   ├── ingestion/          # Document loading & parsing
│   │   ├── __init__.py     # Unified dispatcher (load_document)
│   │   ├── document.py     # Document data model
│   │   ├── pdf_loader.py   # PDF text extraction
│   │   ├── docx_loader.py  # Word (.docx) text & table extraction
│   │   └── image_loader.py # Image OCR (pytesseract / PIL)
│   │
│   ├── extraction/         # Entity & relationship extraction
│   │   ├── entities.py
│   │   ├── ontology.py
│   │   ├── general_ner.py
│   │   ├── deterministic.py
│   │   ├── technology.py
│   │   ├── proximity.py
│   │   ├── relationships.py
│   │   ├── relationship_types.py
│   │   ├── context.py
│   │   ├── context_classifier.py
│   │   ├── resume_classifier.py
│   │   ├── ner_data.py
│   │   ├── ner_labels.py
│   │   └── pipeline.py
│   │
│   ├── normalization/      # Canonical synonym mapping
│   │   └── technology.py
│   │
│   ├── profiles/           # Structured candidate representations
│   │   └── student_profile.py
│   │
│   └── ner_training/       # NER model training & evaluation
│       ├── train_ner.py    # GPU-accelerated spaCy training script
│       └── test_ner.py     # Evaluation & inference checks
│
├── tests/                  # Unit and integration test suite
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation & roadmap
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+ (Python 3.11 recommended)
- (Optional for OCR) [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for scanned resume images
- (Optional for GPU Acceleration) NVIDIA CUDA 12+ capable GPU

### 2. Setup Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate on Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Or on Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*(For GPU acceleration with spaCy/CuPy on NVIDIA hardware, install `spacy[cuda12x]` and `nvidia-cublas-cu12`, `nvidia-curand-cu12`, etc.)*

### 4. Running the Engine

Drop resume files into `data/resumes/` and job descriptions into `data/jds/`.

```bash
# Scan and inspect loaded documents in data/
python -m src.main --scan

# Or load and inspect an individual file
python -m src.main --file path/to/resume.pdf
```

### 5. Training the Custom NER Model (GPU / CPU)

```bash
python -m src.ner_training.train_ner
```

The script automatically detects and utilizes your NVIDIA GPU via `spacy.prefer_gpu()` with CuPy ops.

### 6. Running Tests

```bash
pytest
```
