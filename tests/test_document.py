from src.ingestion.document import (
    TextBlock,
    DocumentPage,
    ParsedDocument,
)


def test_text_block_creation():

    block = TextBlock(
        text="Software Engineer",
        page=1,
        x0=10,
        y0=20,
        x1=150,
        y1=40,
        font_size=12,
        font_name="Arial",
        is_bold=True,
    )

    assert block.text == "Software Engineer"
    assert block.page == 1
    assert block.x0 == 10
    assert block.y0 == 20
    assert block.x1 == 150
    assert block.y1 == 40
    assert block.font_size == 12
    assert block.font_name == "Arial"
    assert block.is_bold is True


def test_document_page_creation():

    block = TextBlock(
        text="Python",
        page=1,
    )

    page = DocumentPage(
        page_number=1,
        width=595,
        height=842,
        blocks=[block],
    )

    assert page.page_number == 1
    assert page.width == 595
    assert page.height == 842
    assert len(page.blocks) == 1
    assert page.blocks[0].text == "Python"


def test_parsed_document_full_text():

    page1 = DocumentPage(
        page_number=1,
        width=595,
        height=842,
        blocks=[
            TextBlock(text="Rahul Sharma", page=1),
            TextBlock(text="Python AWS", page=1),
        ],
    )

    page2 = DocumentPage(
        page_number=2,
        width=595,
        height=842,
        blocks=[
            TextBlock(text="Amazon", page=2),
        ],
    )

    document = ParsedDocument(
        source_file="test.pdf",
        file_type="pdf",
        pages=[page1, page2],
    )

    assert "Rahul Sharma" in document.full_text
    assert "Python AWS" in document.full_text
    assert "Amazon" in document.full_text