from .context_classifier import ContextClassifier


class ResumeEntityClassifier:

    def __init__(self):

        self.classifier = ContextClassifier()

    def classify(
        self,
        entity_text: str,
        context: str
    ):

        labels = [
            "company",
            "job title",
            "skill",
            "technology",
            "degree",
            "institution",
            "project",
            "certification",
            "achievement",
            "responsibility",
            "location",
            "other"
        ]

        combined_text = (
            f"Entity: {entity_text}. "
            f"Context: {context}"
        )

        result = self.classifier.classify(
            combined_text,
            labels
        )

        return {
            "entity_type": result["label"].upper(),
            "confidence": result["confidence"]
        }


    """
FILE PURPOSE:
Classifies resume content into meaningful semantic categories that
may not be simple named entities.

For example, text describing work performed can be identified as
a responsibility or achievement.

This complements NER by helping understand descriptive resume content.

LIMITATION:
The current classifier is an early-stage approach and will later
be replaced or strengthened with resume-specific ML models.
"""