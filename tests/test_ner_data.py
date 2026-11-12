from pathlib import Path

from src.extraction.ner_data import (
    load_training_data,
    validate_training_data,
)


NER_DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ner"
    / "training_data.json"
)


def test_training_data():

    print("\n")
    print("=" * 80)
    print("RESUME NER TRAINING DATA")
    print("=" * 80)

    data = load_training_data(
        str(NER_DATA_FILE)
    )

    validate_training_data(data)

    print(
        f"\nTraining examples: {len(data)}"
    )

    print("\n")
    print("=" * 80)
    print("RESULT: TRAINING DATA VALID")
    print("=" * 80)