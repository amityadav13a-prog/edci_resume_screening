from pathlib import Path


RESUME_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "resumes"
)


def test_resume_directory_exists():

    assert RESUME_DIR.exists()
    assert RESUME_DIR.is_dir()


def test_expected_test_resumes_exist():

    expected_files = {
        "test_resume.pdf",
        # "test_resume3.pdf",
        # "test_resume4.pdf",
        # "test_resume_5.pdf",
        # "test_resume2.docx",
    }

    actual_files = {
        file.name
        for file in RESUME_DIR.iterdir()
        if file.is_file()
    }

    missing_files = expected_files - actual_files

    assert not missing_files, (
        f"Missing test resume files: {missing_files}"
    )