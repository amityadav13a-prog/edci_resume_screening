from pathlib import Path

from src.ingestion.pdf_loader import load_pdf


# ---------------------------------------------------------
# Location of the real PDF resumes
# ---------------------------------------------------------

RESUME_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "resumes"
)


# ---------------------------------------------------------
# Real PDF resumes
# ---------------------------------------------------------

PDF_RESUMES = [
    RESUME_DIR / "test_resume.pdf",
    # RESUME_DIR / "test_resume3.pdf",
    # RESUME_DIR / "test_resume4.pdf",
    # RESUME_DIR / "test_resume_5.pdf",
]


# ---------------------------------------------------------
# Inspect the actual resumes
# ---------------------------------------------------------

def test_inspect_real_pdf_resumes():

    for resume_path in PDF_RESUMES:

        print("\n")
        print("=" * 80)
        print(f"RESUME: {resume_path.name}")
        print("=" * 80)

        # Make sure the actual file exists
        assert resume_path.exists(), (
            f"Resume file not found: {resume_path}"
        )

        # Load the actual PDF
        document = load_pdf(str(resume_path))

        # -------------------------------------------------
        # Basic document information
        # -------------------------------------------------

        print(f"\nFile type : {document.file_type}")
        print(f"Pages    : {len(document.pages)}")

        # -------------------------------------------------
        # Extracted text
        # -------------------------------------------------

        print("\n")
        print("-" * 80)
        print("EXTRACTED TEXT")
        print("-" * 80)

        print(document.full_text)

        # -------------------------------------------------
        # Individual text blocks
        # -------------------------------------------------

        print("\n")
        print("-" * 80)
        print("TEXT BLOCKS + LAYOUT INFORMATION")
        print("-" * 80)

        total_blocks = 0

        for page in document.pages:

            print(f"\n--- PAGE {page.page_number} ---")

            for block in page.blocks:

                total_blocks += 1

                print(
                    f"\nText       : {block.text!r}"
                    f"\nPosition   : "
                    f"x0={block.x0:.1f}, "
                    f"y0={block.y0:.1f}, "
                    f"x1={block.x1:.1f}, "
                    f"y1={block.y1:.1f}"
                    f"\nFont size  : {block.font_size}"
                    f"\nFont name  : {block.font_name}"
                    f"\nBold       : {block.is_bold}"
                )

        print("\n")
        print("-" * 80)
        print(f"TOTAL TEXT BLOCKS: {total_blocks}")
        print("-" * 80)

        # -------------------------------------------------
        # Sanity checks
        # -------------------------------------------------

        assert len(document.pages) > 0
        assert len(document.full_text.strip()) > 0
        assert total_blocks > 0