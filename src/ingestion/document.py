from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TextBlock:
    text: str
    page: int

    # Position on page
    x0: float = 0.0
    y0: float = 0.0
    x1: float = 0.0
    y1: float = 0.0

    # Optional layout information
    font_size: Optional[float] = None
    font_name: Optional[str] = None
    is_bold: Optional[bool] = None


@dataclass
class DocumentPage:
    page_number: int
    width: float
    height: float
    blocks: List[TextBlock] = field(default_factory=list)


@dataclass
class ParsedDocument:
    source_file: str
    file_type: str
    pages: List[DocumentPage] = field(default_factory=list)

    @property
    def full_text(self) -> str:
        page_text = []

        for page in self.pages:
            blocks = sorted(
                page.blocks,
                key=lambda b: (b.y0, b.x0)
            )

            text = "\n".join(
                block.text for block in blocks
                if block.text.strip()
            )

            page_text.append(text)

        return "\n\n".join(page_text)
#====================================================================================================
#  This is our first important abstraction.

# We're not saying:
#     this block = skill
#     this block = company

# We're simply saying:
#     This piece of text appeared here, on this page, at this position, with these visual properties
# ====================================
# This code defines data structures using Python dataclasses to represent
# and organize text extracted from structured documents like PDFs. 
# It breaks a document down into individual TextBlock elements that hold raw text, 
# page numbers, precise layout coordinates (x0, y0, x1, y1), and optional font styling. 
# These blocks are grouped into DocumentPage objects containing page dimensions, which are then collected under
# ParsedDocument along with file metadata. Finally, it provides a full_text property that sorts all text blocks
#  in natural reading order—top-to-bottom then left-to-right—and joins them into a clean, multi-page text string.


#====================================================================================================
"""
FILE PURPOSE:
Defines the common document data structures used throughout the system.

TextBlock stores extracted text along with page/layout information.
DocumentPage groups text blocks for a page.
ParsedDocument represents the complete parsed file and provides full_text.

All PDF, DOCX, and image loaders convert their input into these structures
so the rest of the pipeline can work with one common format.
"""