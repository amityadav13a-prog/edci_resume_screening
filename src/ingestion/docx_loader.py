from pathlib import Path

from docx import Document

from .document import ParsedDocument, DocumentPage, TextBlock


def load_docx(file_path: str) -> ParsedDocument:

    path = Path(file_path)

    document = Document(file_path)

    blocks = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if not text:
            continue

        font_sizes = []
        font_names = []
        bold_flags = []

        for run in paragraph.runs:

            if run.font.size:
                font_sizes.append(
                    run.font.size.pt
                )

            if run.font.name:
                font_names.append(
                    run.font.name
                )

            if run.bold is not None:
                bold_flags.append(
                    run.bold
                )

        block = TextBlock(
            text=text,
            page=1,
            font_size=(
                sum(font_sizes) / len(font_sizes)
                if font_sizes else None
            ),
            font_name=(
                font_names[0]
                if font_names else None
            ),
            is_bold=(
                any(bold_flags)
                if bold_flags else None
            )
        )

        blocks.append(block)

    page = DocumentPage(
        page_number=1,
        width=0,
        height=0,
        blocks=blocks
    )

    return ParsedDocument(
        source_file=str(path),
        file_type="docx",
        pages=[page]
    )

