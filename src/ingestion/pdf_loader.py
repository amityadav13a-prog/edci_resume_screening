
from pathlib import Path

import pymupdf

from .document import ParsedDocument, DocumentPage, TextBlock


def load_pdf(file_path: str) -> ParsedDocument:

    path = Path(file_path)

    document = pymupdf.open(file_path)

    parsed_pages = []

    for page_index, page in enumerate(document):

        page_width = page.rect.width
        page_height = page.rect.height

        blocks = []

        raw_blocks = page.get_text("dict")["blocks"]

        for raw_block in raw_blocks:

            # Ignore image blocks for now.
            # We only process blocks containing text.
            if raw_block.get("type") != 0:
                continue

            for line in raw_block.get("lines", []):

                line_text_parts = []

                font_sizes = []
                font_names = []
                bold_flags = []

                for span in line.get("spans", []):

                    text = span.get("text", "")

                    # Ignore empty/whitespace-only spans
                    if not text.strip():
                        continue

                    line_text_parts.append(text)

                    font_size = span.get("size")
                    font_name = span.get("font", "")

                    if font_size is not None:
                        font_sizes.append(font_size)

                    if font_name:
                        font_names.append(font_name)

                    bold_flags.append(
                        "bold" in font_name.lower()
                    )

                # Combine all spans belonging to this line
                text = "".join(line_text_parts).strip()

                if not text:
                    continue

                # Bounding box of the complete line
                bbox = line.get(
                    "bbox",
                    [0.0, 0.0, 0.0, 0.0]
                )

                text_block = TextBlock(
                    text=text,
                    page=page_index + 1,

                    x0=bbox[0],
                    y0=bbox[1],
                    x1=bbox[2],
                    y1=bbox[3],

                    font_size=(
                        sum(font_sizes) / len(font_sizes)
                        if font_sizes
                        else None
                    ),

                    font_name=(
                        font_names[0]
                        if font_names
                        else None
                    ),

                    is_bold=(
                        any(bold_flags)
                        if bold_flags
                        else None
                    ),
                )

                blocks.append(text_block)

        parsed_page = DocumentPage(
            page_number=page_index + 1,
            width=page_width,
            height=page_height,
            blocks=blocks,
        )

        parsed_pages.append(parsed_page)

    document.close()

    return ParsedDocument(
        source_file=str(path),
        file_type="pdf",
        pages=parsed_pages,
    )
# =======================================================================================
# This function (load_pdf) reads a PDF file using PyMuPDF (fitz) and 
# converts its contents into a structured ParsedDocument object. It iterates through each page,
# extracts dimensions, and processes text line-by-line while filtering out image blocks.
# For each line, it collects text spans, calculates average font size, detects font name 
# and bold styling, and extracts bounding box coordinates (bbox). Finally, it packages each 
# line into a TextBlock, groups them under DocumentPage objects, and returns the fully parsed document structure.
