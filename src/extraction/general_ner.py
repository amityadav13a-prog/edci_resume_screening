import spacy

from .entities import Entity


class GeneralNER:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    def extract(self, parsed_document):

        entities = []

        for page in parsed_document.pages:

            for block in page.blocks:

                doc = self.nlp(block.text)

                for ent in doc.ents:

                    entity_type = self.map_entity_type(
                        ent.label_
                    )

                    if entity_type is None:
                        continue

                    entities.append(
                        Entity(
                            text=ent.text,
                            entity_type=entity_type,
                            confidence=0.80,
                            page=page.page_number,
                            source_text=block.text
                        )
                    )

        return entities

    @staticmethod
    def map_entity_type(label):

        mapping = {
            "PERSON": "PERSON",
            "ORG": "COMPANY",
            "GPE": "LOCATION",
            "LOC": "LOCATION",
            "DATE": "DATE",
            "TIME": "DATE",
            "FAC": "LOCATION"
        }

        return mapping.get(label)

    """
FILE PURPOSE:
Uses a general-purpose NLP NER model to identify common entities
such as people, organizations, locations, and dates.

The extracted entities are mapped to the project's internal ontology
and converted into Entity objects.

LIMITATION:
The model is not specifically trained for resumes, so resume-specific
entities such as job titles, projects, and technologies may be missed
or incorrectly classified.
"""