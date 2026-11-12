from pathlib import Path

import spacy


MODEL_DIR = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "resume_ner"
)


def test_resume_ner_model():

    print("\n")
    print("=" * 80)
    print("RESUME NER MODEL TEST")
    print("=" * 80)

    assert MODEL_DIR.exists(), (
        f"NER model not found: {MODEL_DIR}"
    )

    nlp = spacy.load(MODEL_DIR)

    test_text = (
        "John worked at Google as a Software Engineer "
        "using Python and Docker."
    )

    print("\nTEST TEXT")
    print("-" * 80)
    print(test_text)

    doc = nlp(test_text)

    print("\nEXTRACTED ENTITIES")
    print("-" * 80)

    for entity in doc.ents:

        print(
            f"[{entity.label_}] "
            f"{entity.text!r} "
            f"({entity.start_char}:{entity.end_char})"
        )

    print("\n")
    print("=" * 80)
    print(
        f"TOTAL ENTITIES: {len(doc.ents)}"
    )
    print("=" * 80)

    assert len(doc.ents) > 0