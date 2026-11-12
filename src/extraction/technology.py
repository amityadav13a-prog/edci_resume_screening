import re

from .entities import Entity
from normalization.technology import TECHNOLOGY_ALIASES


class TechnologyExtractor:

    def __init__(self):

        self.aliases = TECHNOLOGY_ALIASES

        self.patterns = [
            (
                alias,
                canonical
            )
            for alias, canonical
            in self.aliases.items()
        ]

    def extract(self, parsed_document):

        entities = []

        for page in parsed_document.pages:

            for block in page.blocks:

                text = block.text

                lower_text = text.lower()

                for alias, canonical in self.patterns:

                    pattern = (
                        r"(?<!\w)"
                        + re.escape(alias)
                        + r"(?!\w)"
                    )

                    matches = re.finditer(
                        pattern,
                        lower_text
                    )

                    for match in matches:

                        original = text[
                            match.start():
                            match.end()
                        ]

                        entities.append(
                            Entity(
                                text=original,
                                entity_type="TECHNOLOGY",
                                confidence=0.98,
                                page=page.page_number,
                                source_text=text,
                                normalized_value=canonical
                            )
                        )

        return entities

    """
FILE PURPOSE:
Detects technology-related terms in resume text.

Recognizes technologies such as Python, AWS, Docker, React, and
Kubernetes and handles known aliases such as K8s and ReactJS.

Technology entities are later normalized so different names for the
same technology can be treated as one concept.

LIMITATION:
Unknown technologies or aliases may not be detected until added or
handled by a stronger ML-based recognizer.
"""