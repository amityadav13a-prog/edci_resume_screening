from transformers import pipeline


class ContextClassifier:

    def __init__(self):

        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )

    def classify(
        self,
        text: str,
        labels: list[str]
    ):

        result = self.classifier(
            text,
            candidate_labels=labels
        )

        return {
            "label": result["labels"][0],
            "confidence": float(
                result["scores"][0]
            )
        }
    """
FILE PURPOSE:
Uses the surrounding context of extracted entities to help classify
their semantic type.

It can distinguish concepts such as company, job title, skill,
project, degree, and certification when general NER alone is insufficient.

The current implementation uses a zero-shot/context classification
approach for experimentation.

LIMITATION:
Large zero-shot models can be slow and are not ideal for final
production-scale processing.
"""