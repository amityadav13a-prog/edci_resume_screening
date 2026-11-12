import sys

from ingestion import load_document
from extraction.pipeline import EntityExtractionPipeline


def main():

    if len(sys.argv) != 2:

        print(
            "Usage: "
            "python src/main.py <resume>"
        )

        return

    file_path = sys.argv[1]

    document = load_document(
        file_path
    )

    extractor = EntityExtractionPipeline()

    entities = extractor.extract(
        document
    )

    print("\n" + "=" * 60)
    print("EXTRACTED ENTITIES")
    print("=" * 60)

    for entity in entities:

        print(
            f"\n[{entity.entity_type}] "
            f"{entity.text}"
        )

        print(
            f"Confidence: "
            f"{entity.confidence}"
        )

        print(
            f"Page: {entity.page}"
        )

        if entity.normalized_value:

            print(
                f"Normalized: "
                f"{entity.normalized_value}"
            )

        print(
            f"Evidence: "
            f"{entity.source_text}"
        )


if __name__ == "__main__":
    main()