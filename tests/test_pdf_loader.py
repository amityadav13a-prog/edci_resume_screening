
from pathlib import Path

import pytest

from src.ingestion.pdf_loader import load_pdf


RESUME_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "resumes"
)


PDF_RESUMES = [
    RESUME_DIR / "test_resume.pdf",
    # RESUME_DIR / "test_resume3.pdf",
    # RESUME_DIR / "test_resume4.pdf",
    # RESUME_DIR / "test_resume_5.pdf",
]


@pytest.mark.parametrize("resume_path", PDF_RESUMES)
def test_pdf_resume_exists(resume_path):

    print("\n")
    print("=" * 80)
    print(f"CHECKING FILE: {resume_path.name}")
    print("=" * 80)

    print(f"Full path: {resume_path}")

    assert resume_path.exists(), (
        f"Resume file not found: {resume_path}"
    )

    print("RESULT: File exists")


@pytest.mark.parametrize("resume_path", PDF_RESUMES)
def test_pdf_can_be_loaded(resume_path):

    print("\n")
    print("=" * 80)
    print(f"LOADING: {resume_path.name}")
    print("=" * 80)

    document = load_pdf(str(resume_path))

    print(f"File type: {document.file_type}")
    print(f"Pages: {len(document.pages)}")

    assert document is not None
    assert document.file_type == "pdf"

    print("RESULT: PDF loaded successfully")


@pytest.mark.parametrize("resume_path", PDF_RESUMES)
def test_pdf_has_pages(resume_path):

    print("\n")
    print("=" * 80)
    print(f"PAGE CHECK: {resume_path.name}")
    print("=" * 80)

    document = load_pdf(str(resume_path))

    print(f"Number of pages: {len(document.pages)}")

    for page in document.pages:
        print(
            f"Page {page.page_number}: "
            f"width={page.width:.2f}, "
            f"height={page.height:.2f}, "
            f"blocks={len(page.blocks)}"
        )

    assert len(document.pages) > 0

    print("RESULT: Pages detected successfully")


@pytest.mark.parametrize("resume_path", PDF_RESUMES)
def test_pdf_contains_text(resume_path):

    print("\n")
    print("=" * 80)
    print(f"TEXT EXTRACTION: {resume_path.name}")
    print("=" * 80)

    document = load_pdf(str(resume_path))

    extracted_text = document.full_text

    print("\n--- EXTRACTED RESUME TEXT ---")
    print(extracted_text)
    print("--- END EXTRACTED TEXT ---")

    print(
        f"\nCharacters extracted: {len(extracted_text)}"
    )

    assert len(extracted_text.strip()) > 0

    print("RESULT: Text extracted successfully")


@pytest.mark.parametrize("resume_path", PDF_RESUMES)
def test_pdf_contains_text_blocks(resume_path):

    print("\n")
    print("=" * 80)
    print(f"TEXT BLOCK CHECK: {resume_path.name}")
    print("=" * 80)

    document = load_pdf(str(resume_path))

    total_blocks = sum(
        len(page.blocks)
        for page in document.pages
    )

    print(f"Total text blocks: {total_blocks}")

    for page in document.pages:

        print(f"\n--- PAGE {page.page_number} ---")

        for index, block in enumerate(page.blocks, start=1):

            print(
                f"\nBlock {index}"
                f"\n  Text      : {block.text!r}"
                f"\n  Position  : "
                f"x0={block.x0:.2f}, "
                f"y0={block.y0:.2f}, "
                f"x1={block.x1:.2f}, "
                f"y1={block.y1:.2f}"
                f"\n  Font size : {block.font_size}"
                f"\n  Font name : {block.font_name}"
                f"\n  Bold      : {block.is_bold}"
            )

    assert total_blocks > 0

    print(
        f"\nRESULT: {total_blocks} text blocks detected"
    )


@pytest.mark.parametrize("resume_path", PDF_RESUMES)
def test_pdf_preserves_layout_information(resume_path):

    print("\n")
    print("=" * 80)
    print(f"LAYOUT CHECK: {resume_path.name}")
    print("=" * 80)

    document = load_pdf(str(resume_path))

    blocks = [
        block
        for page in document.pages
        for block in page.blocks
    ]

    print(f"Checking {len(blocks)} blocks...")

    for block in blocks:

        print(
            f"\nText: {block.text!r}"
            f"\n  x0={block.x0:.2f}"
            f"\n  y0={block.y0:.2f}"
            f"\n  x1={block.x1:.2f}"
            f"\n  y1={block.y1:.2f}"
        )

        assert block.x0 is not None
        assert block.y0 is not None
        assert block.x1 is not None
        assert block.y1 is not None

    print("RESULT: Layout information preserved successfully")
