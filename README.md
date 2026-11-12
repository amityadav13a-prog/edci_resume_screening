# Resume Matching Engine

An intelligent resume parsing and job description matching pipeline.

## Project Structure

```text
resume_matching_engine/
│
├── data/
│   ├── resumes/            # Directory to store candidate resumes (PDF, DOCX, images)
│   └── jds/                # Directory to store Job Descriptions (PDF, DOCX, etc.)
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Project configurations and path management
│   ├── ingestion/          # Document loading & text extraction module
│   │   ├── __init__.py     # Unified document loader dispatcher
│   │   ├── document.py     # Document data model
│   │   ├── pdf_loader.py   # PDF text extraction
│   │   ├── docx_loader.py  # DOCX/Word text extraction
│   │   └── image_loader.py # Image OCR text extraction
│   │
│   └── main.py             # Entry point / CLI pipeline
│
├── tests/
│   ├── __init__.py
│   └── test_ingestion.py   # Unit tests for ingestion and models
│
├── requirements.txt        # Python package dependencies
├── .gitignore              # Git ignore rules for Python & data
└── README.md               # Project documentation
```

## Getting Started

### 1. Prerequisites

- Python 3.10+ recommended
- (Optional for OCR) [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system if extracting text from scanned resume images.

### 2. Setup Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Or on Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Running the Engine

Drop resume files into `data/resumes/` and job descriptions into `data/jds/`.

```bash
# Scan and inspect loaded documents in data/
python -m src.main --scan

# Or load and preview an individual file
python -m src.main --file path/to/resume.pdf
```

### 5. Running Tests

```bash
pytest
```

