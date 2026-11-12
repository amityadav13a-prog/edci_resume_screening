from pathlib import Path

from .pdf_loader import load_pdf
from .docx_loader import load_docx


def load_document(file_path: str):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )