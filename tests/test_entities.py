from src.extraction.entities import extract_entities


def test_email_extraction():

    text = """
    Rahul Sharma
    Contact: rahul.sharma@example.com
    """

    entities = extract_entities(text)

    emails = [
        e for e in entities
        if e.entity_type == "EMAIL"
    ]

    assert len(emails) == 1
    assert emails[0].text == "rahul.sharma@example.com"