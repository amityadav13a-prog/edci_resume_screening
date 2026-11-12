
from pathlib import Path

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.docx_loader import load_docx


# ============================================================
# PATHS
# ============================================================

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


DOCX_RESUMES = [
    RESUME_DIR / "test_resume2.docx",
]


# ============================================================
# PDF INGESTION
# ============================================================

def test_pdf_ingestion():

    print("\n")
    print("=" * 80)
    print("PDF INGESTION TEST")
    print("=" * 80)

    for resume_path in PDF_RESUMES:

        print("\n")
        print("-" * 80)
        print(f"PROCESSING PDF: {resume_path.name}")
        print("-" * 80)

        # ----------------------------------------------------
        # Check file
        # ----------------------------------------------------

        assert resume_path.exists()

        print(f"File exists       : YES")
        print(f"File path         : {resume_path}")

        # ----------------------------------------------------
        # Load PDF
        # ----------------------------------------------------

        document = load_pdf(str(resume_path))

        assert document is not None
        assert document.file_type == "pdf"

        print(f"File type         : {document.file_type}")
        print(f"Pages             : {len(document.pages)}")

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        text = document.full_text

        assert text.strip()

        print(f"Characters        : {len(text)}")

        print("\n")
        print("EXTRACTED TEXT")
        print("-" * 80)
        print(text)

        # ----------------------------------------------------
        # Text blocks
        # ----------------------------------------------------

        total_blocks = sum(
            len(page.blocks)
            for page in document.pages
        )

        assert total_blocks > 0

        print("\n")
        print("TEXT BLOCK SUMMARY")
        print("-" * 80)
        print(f"Total text blocks : {total_blocks}")

        # ----------------------------------------------------
        # Layout information
        # ----------------------------------------------------

        print("\n")
        print("LAYOUT INFORMATION")
        print("-" * 80)

        for page in document.pages:

            print(
                f"\nPAGE {page.page_number}"
            )

            print(
                f"Size: "
                f"{page.width:.1f} x "
                f"{page.height:.1f}"
            )

            for index, block in enumerate(
                page.blocks,
                start=1
            ):

                print(
                    f"\nBlock {index}"
                )

                print(
                    f"  Text      : {block.text!r}"
                )

                print(
                    f"  Position  : "
                    f"x0={block.x0:.1f}, "
                    f"y0={block.y0:.1f}, "
                    f"x1={block.x1:.1f}, "
                    f"y1={block.y1:.1f}"
                )

                print(
                    f"  Font size : {block.font_size}"
                )

                print(
                    f"  Font name : {block.font_name}"
                )

                print(
                    f"  Bold      : {block.is_bold}"
                )

        print("\nRESULT: PDF ingestion successful")


# ============================================================
# DOCX INGESTION
# ============================================================

def test_docx_ingestion():

    print("\n")
    print("=" * 80)
    print("DOCX INGESTION TEST")
    print("=" * 80)

    for resume_path in DOCX_RESUMES:

        print("\n")
        print("-" * 80)
        print(f"PROCESSING DOCX: {resume_path.name}")
        print("-" * 80)

        # ----------------------------------------------------
        # Check file
        # ----------------------------------------------------

        assert resume_path.exists()

        print(f"File exists       : YES")
        print(f"File path         : {resume_path}")

        # ----------------------------------------------------
        # Load DOCX
        # ----------------------------------------------------

        document = load_docx(str(resume_path))

        assert document is not None
        assert document.file_type == "docx"

        print(f"File type         : {document.file_type}")
        print(f"Pages             : {len(document.pages)}")

        # ----------------------------------------------------
        # Extract text
        # ----------------------------------------------------

        text = document.full_text

        assert text.strip()

        print(f"Characters        : {len(text)}")

        print("\n")
        print("EXTRACTED TEXT")
        print("-" * 80)
        print(text)

        # ----------------------------------------------------
        # Text blocks
        # ----------------------------------------------------

        total_blocks = sum(
            len(page.blocks)
            for page in document.pages
        )

        assert total_blocks > 0

        print("\n")
        print("TEXT BLOCK SUMMARY")
        print("-" * 80)
        print(f"Total text blocks : {total_blocks}")

        # ----------------------------------------------------
        # Layout information
        # ----------------------------------------------------

        print("\n")
        print("LAYOUT INFORMATION")
        print("-" * 80)

        for page in document.pages:

            print(
                f"\nPAGE {page.page_number}"
            )

            print(
                f"Size: "
                f"{page.width:.1f} x "
                f"{page.height:.1f}"
            )

            for index, block in enumerate(
                page.blocks,
                start=1
            ):

                print(
                    f"\nBlock {index}"
                )

                print(
                    f"  Text      : {block.text!r}"
                )

                print(
                    f"  Position  : "
                    f"x0={block.x0:.1f}, "
                    f"y0={block.y0:.1f}, "
                    f"x1={block.x1:.1f}, "
                    f"y1={block.y1:.1f}"
                )

                print(
                    f"  Font size : {block.font_size}"
                )

                print(
                    f"  Font name : {block.font_name}"
                )

                print(
                    f"  Bold      : {block.is_bold}"
                )

        print("\nRESULT: DOCX ingestion successful")
