from .general_ner import GeneralNER
from .deterministic import extract_deterministic
from .technology import TechnologyExtractor


class EntityExtractionPipeline:

    def __init__(self):

        self.general_ner = GeneralNER()
        self.technology_extractor = TechnologyExtractor()

    def extract(self, parsed_document):

        entities = []

        # Layer 1: deterministic
        entities.extend(
            extract_deterministic(
                parsed_document
            )
        )

        # Layer 2: general NER
        entities.extend(
            self.general_ner.extract(
                parsed_document
            )
        )

        # Layer 3: technology recognition
        entities.extend(
            self.technology_extractor.extract(
                parsed_document
            )
        )

        return self.remove_duplicates(
            entities
        )

    @staticmethod
    def remove_duplicates(entities):

        seen = set()
        result = []

        for entity in entities:

            key = (
                entity.text.lower(),
                entity.entity_type,
                entity.page
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(entity)

        return result

    """
FILE PURPOSE:
Orchestrates the complete resume extraction pipeline.

Connects document ingestion, entity extraction, technology detection,
context analysis, relationship extraction, and normalization into
one processing flow.

Its goal is to allow a resume to be processed through the complete
extraction system instead of calling every component manually.
"""