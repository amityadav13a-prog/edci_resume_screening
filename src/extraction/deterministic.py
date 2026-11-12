import re

from .entities import Entity


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\+?\d{1,3}[\s.-]?)?"
    r"(?:\(?\d{2,4}\)?[\s.-]?)?"
    r"\d{3,4}[\s.-]?\d{3,4}"
    r"(?!\d)"
)

DATE_PATTERN = re.compile(
    r"\b("
    r"(?:19|20)\d{2}"
    r"(?:\s*[-–]\s*(?:19|20)\d{2})?"
    r")\b"
)


def extract_deterministic(parsed_document):

    entities = []

    for page in parsed_document.pages:

        for block in page.blocks:

            text = block.text

            # Email
            for match in EMAIL_PATTERN.finditer(text):

                entities.append(
                    Entity(
                        text=match.group(),
                        entity_type="EMAIL",
                        confidence=0.99,
                        page=page.page_number,
                        source_text=text
                    )
                )

            # Phone
            for match in PHONE_PATTERN.finditer(text):

                entities.append(
                    Entity(
                        text=match.group(),
                        entity_type="PHONE",
                        confidence=0.90,
                        page=page.page_number,
                        source_text=text
                    )
                )

            # Dates
            for match in DATE_PATTERN.finditer(text):

                entities.append(
                    Entity(
                        text=match.group(),
                        entity_type="DATE",
                        confidence=0.95,
                        page=page.page_number,
                        source_text=text
                    )
                )

    return entities

"""
FILE PURPOSE:
Extracts highly structured information using deterministic rules
and regular expressions.

Currently used for information such as email addresses, phone numbers,
and dates where pattern-based extraction is reliable.

The extracted values are converted into Entity objects.

LIMITATION:
Rules identify patterns but cannot reliably determine the semantic
meaning of ambiguous values such as a year.
"""