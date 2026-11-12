
from pathlib import Path
import inspect

import pytest

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.docx_loader import load_docx
from src.extraction.pipeline import EntityExtractionPipeline
import src.profiles.student_profile as student_profile_module


# ============================================================
# RESUME DIRECTORY
# ============================================================

RESUME_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "resumes"
)


# ============================================================
# REAL RESUMES
# ============================================================

RESUMES = [
    RESUME_DIR / "test_resume.pdf",
    # RESUME_DIR / "test_resume2.docx",
    # RESUME_DIR / "test_resume3.pdf",
    # RESUME_DIR / "test_resume4.pdf",
    # RESUME_DIR / "test_resume_5.pdf",
]


# ============================================================
# LOAD DOCUMENT
# ============================================================

def load_resume(resume_path):

    extension = resume_path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(str(resume_path))

    if extension == ".docx":
        return load_docx(str(resume_path))

    raise ValueError(
        f"Unsupported resume format: {extension}"
    )


# ============================================================
# PRINT ENTITY
# ============================================================

def print_entity(entity, index):

    print(f"\nEntity {index}")
    print(f"  Text       : {getattr(entity, 'text', None)}")
    print(
        f"  Type       : "
        f"{getattr(entity, 'entity_type', None)}"
    )
    print(
        f"  Page       : "
        f"{getattr(entity, 'page', None)}"
    )

    if hasattr(entity, "confidence"):
        print(
            f"  Confidence : "
            f"{entity.confidence}"
        )

    if hasattr(entity, "source"):
        print(
            f"  Source     : "
            f"{entity.source}"
        )


# ============================================================
# TEST — COMPLETE EXTRACTION PIPELINE
# ============================================================

@pytest.mark.parametrize("resume_path", RESUMES)
def test_student_profile_pipeline(resume_path):

    print("\n")
    print("=" * 90)
    print("STUDENT PROFILE PIPELINE")
    print("=" * 90)

    print(f"Resume: {resume_path.name}")

    # ========================================================
    # 1. FILE
    # ========================================================

    print("\n")
    print("1. RESUME FILE")
    print("-" * 90)

    assert resume_path.exists()

    print(f"Path   : {resume_path}")
    print(f"Format : {resume_path.suffix.lower()}")
    print("Status : EXISTS")

    # ========================================================
    # 2. DOCUMENT INGESTION
    # ========================================================

    print("\n")
    print("2. DOCUMENT INGESTION")
    print("-" * 90)

    document = load_resume(resume_path)

    assert document is not None
    assert document.full_text.strip()

    print(f"File type       : {document.file_type}")
    print(f"Pages           : {len(document.pages)}")
    print(
        f"Characters      : "
        f"{len(document.full_text)}"
    )

    # ========================================================
    # 3. EXTRACTED TEXT
    # ========================================================

    print("\n")
    print("3. EXTRACTED RESUME TEXT")
    print("-" * 90)

    print(document.full_text)

    # ========================================================
    # 4. ENTITY EXTRACTION
    # ========================================================

    print("\n")
    print("4. ENTITY EXTRACTION")
    print("-" * 90)

    pipeline = EntityExtractionPipeline()

    entities = pipeline.extract(document)

    assert entities is not None
    assert isinstance(entities, list)

    print(
        f"Total entities found: "
        f"{len(entities)}"
    )

    for index, entity in enumerate(
        entities,
        start=1
    ):
        print_entity(entity, index)

    # ========================================================
    # 5. GROUP ENTITIES
    # ========================================================

    print("\n")
    print("5. ENTITIES GROUPED BY TYPE")
    print("-" * 90)

    grouped = {}

    for entity in entities:

        entity_type = getattr(
            entity,
            "entity_type",
            "UNKNOWN"
        )

        grouped.setdefault(
            entity_type,
            []
        )

        grouped[entity_type].append(
            entity
        )

    for entity_type in sorted(grouped):

        print(f"\n{entity_type}")

        for entity in grouped[entity_type]:

            print(
                f"  - {entity.text}"
            )

    # ========================================================
    # 6. STUDENT PROFILE MODULE
    # ========================================================

    print("\n")
    print("6. STUDENT PROFILE MODULE")
    print("-" * 90)

    print(
        f"Module: "
        f"{student_profile_module.__file__}"
    )

    print("\nAvailable classes/functions:")

    members = inspect.getmembers(
        student_profile_module
    )

    callable_members = [
        name
        for name, obj in members
        if (
            not name.startswith("_")
            and (
                inspect.isfunction(obj)
                or inspect.isclass(obj)
            )
        )
    ]

    if callable_members:

        for name in callable_members:
            print(f"  - {name}")

    else:

        print(
            "  No public classes/functions found."
        )

    # ========================================================
    # 7. CHECK PROFILE MODULE
    # ========================================================

    assert student_profile_module is not None

    print("\n")
    print("7. PROFILE MODULE STATUS")
    print("-" * 90)

    print(
        "Student profile module imported successfully."
    )

    # ========================================================
    # 8. PROFILE OBJECTS
    # ========================================================

    print("\n")
    print("8. STUDENT PROFILE OBJECTS")
    print("-" * 90)

    profile_classes = [
        obj
        for name, obj in members
        if (
            not name.startswith("_")
            and inspect.isclass(obj)
        )
    ]

    if profile_classes:

        for cls in profile_classes:

            print(
                f"\nClass: {cls.__name__}"
            )

            print(
                f"Module: {cls.__module__}"
            )

            try:

                print(
                    "Constructor:"
                )

                print(
                    f"  {inspect.signature(cls)}"
                )

            except (TypeError, ValueError):

                print(
                    "  Signature unavailable"
                )

    else:

        print(
            "No public profile classes found."
        )

    # ========================================================
    # 9. FINAL PIPELINE SUMMARY
    # ========================================================

    print("\n")
    print("=" * 90)
    print("PIPELINE SUMMARY")
    print("=" * 90)

    print(f"Resume             : {resume_path.name}")
    print(f"Document type      : {document.file_type}")
    print(f"Pages              : {len(document.pages)}")
    print(
        f"Extracted chars    : "
        f"{len(document.full_text)}"
    )
    print(
        f"Entities extracted : "
        f"{len(entities)}"
    )
    print(
        f"Entity types       : "
        f"{len(grouped)}"
    )

    print("\nEntity types detected:")

    for entity_type in sorted(grouped):

        print(
            f"  - {entity_type}"
        )

    print("\n")
    print("=" * 90)
    print("RESULT: RESUME → ENTITY PIPELINE SUCCESSFUL")
    print("=" * 90)

    assert len(entities) > 0
