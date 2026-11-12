from pathlib import Path
from collections import defaultdict
import json

import spacy


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_DATA_PATH = PROJECT_ROOT / "data" / "ner" / "test_data.json"
MODEL_PATH = PROJECT_ROOT / "models" / "resume_ner"


# ============================================================
# LOAD TEST DATA
# ============================================================

def load_test_data(path):

    if not path.exists():
        raise FileNotFoundError(
            f"Test data not found:\n{path}"
        )

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Test JSON must contain a list of resumes.")

    print(f"✓ Test resumes loaded: {len(data)}")

    return data


# ============================================================
# VALIDATE ENTITY OFFSETS
# ============================================================

def validate_entities(text, entities, resume_id):

    validated = []
    previous_end = -1

    for entity in entities:

        required = ["start", "end", "text", "label"]

        for key in required:
            if key not in entity:
                raise ValueError(
                    f"Missing '{key}' in entity of {resume_id}"
                )

        start = entity["start"]
        end = entity["end"]
        entity_text = entity["text"]
        label = entity["label"]

        # Check offset types
        if not isinstance(start, int) or not isinstance(end, int):
            raise ValueError(
                f"Invalid offsets in {resume_id}: {entity}"
            )

        # Check range
        if start < 0 or end > len(text) or start >= end:
            raise ValueError(
                f"Invalid entity range in {resume_id}: {entity}"
            )

        # Verify text matches offsets
        actual_text = text[start:end]

        if actual_text != entity_text:
            raise ValueError(
                f"\nOffset mismatch in {resume_id}\n"
                f"Entity text : {entity_text!r}\n"
                f"Actual text  : {actual_text!r}\n"
                f"Offsets      : {start}:{end}"
            )

        # Check overlap
        if start < previous_end:
            raise ValueError(
                f"Overlapping entities in {resume_id}: {entity}"
            )

        previous_end = end

        validated.append(
            (start, end, label)
        )

    return validated


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(gold, predicted):

    gold = set(gold)
    predicted = set(predicted)

    tp = len(gold & predicted)
    fp = len(predicted - gold)
    fn = len(gold - predicted)

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0.0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return tp, fp, fn, precision, recall, f1


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(nlp, test_data):

    overall_gold = []
    overall_predicted = []

    per_label_gold = defaultdict(set)
    per_label_predicted = defaultdict(set)

    total = len(test_data)

    print("\n============================================================")
    print("RUNNING FINAL TEST EVALUATION")
    print("============================================================")

    for i, item in enumerate(test_data, start=1):

        resume_id = item.get(
            "resume_id",
            f"resume_{i}"
        )

        text = item["text"]
        entities = item["entities"]

        # -----------------------------
        # GOLD ENTITIES
        # -----------------------------

        gold_entities = validate_entities(
            text,
            entities,
            resume_id
        )

        # -----------------------------
        # MODEL PREDICTIONS
        # -----------------------------

        doc = nlp(text)

        predicted_entities = []

        for ent in doc.ents:

            predicted_entities.append(
                (
                    ent.start_char,
                    ent.end_char,
                    ent.label_
                )
            )

        # -----------------------------
        # OVERALL
        # -----------------------------

        overall_gold.extend(gold_entities)
        overall_predicted.extend(predicted_entities)

        # -----------------------------
        # PER LABEL
        # -----------------------------

        for start, end, label in gold_entities:

            per_label_gold[label].add(
                (start, end, label)
            )

        for start, end, label in predicted_entities:

            per_label_predicted[label].add(
                (start, end, label)
            )

        if i % 25 == 0 or i == total:
            print(f"Processed {i}/{total} resumes")

    # ========================================================
    # OVERALL METRICS
    # ========================================================

    (
        tp,
        fp,
        fn,
        precision,
        recall,
        f1
    ) = calculate_metrics(
        overall_gold,
        overall_predicted
    )

    print("\n============================================================")
    print("FINAL TEST RESULTS")
    print("============================================================")

    print(f"Test Resumes  : {total}")
    print(f"Gold Entities : {len(overall_gold)}")
    print(f"Predicted     : {len(overall_predicted)}")
    print(f"True Positive : {tp}")
    print(f"False Positive: {fp}")
    print(f"False Negative: {fn}")

    print("\nOVERALL")
    print("------------------------------------------------------------")

    print(
        f"Precision: {precision:.4f} "
        f"({precision * 100:.2f}%)"
    )

    print(
        f"Recall   : {recall:.4f} "
        f"({recall * 100:.2f}%)"
    )

    print(
        f"F1       : {f1:.4f} "
        f"({f1 * 100:.2f}%)"
    )

    # ========================================================
    # PER LABEL RESULTS
    # ========================================================

    all_labels = sorted(
        set(per_label_gold.keys()) |
        set(per_label_predicted.keys())
    )

    print("\n============================================================")
    print("PER-LABEL RESULTS")
    print("============================================================")

    print(
        f"{'LABEL':<25}"
        f"{'GOLD':>8}"
        f"{'PRED':>8}"
        f"{'PRECISION':>12}"
        f"{'RECALL':>10}"
        f"{'F1':>10}"
    )

    print("-" * 75)

    for label in all_labels:

        gold = per_label_gold[label]
        predicted = per_label_predicted[label]

        (
            label_tp,
            label_fp,
            label_fn,
            label_precision,
            label_recall,
            label_f1
        ) = calculate_metrics(
            gold,
            predicted
        )

        print(
            f"{label:<25}"
            f"{len(gold):>8}"
            f"{len(predicted):>8}"
            f"{label_precision:>12.4f}"
            f"{label_recall:>10.4f}"
            f"{label_f1:>10.4f}"
        )

    print("\n============================================================")
    print("TEST EVALUATION COMPLETE")
    print("============================================================")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n============================================================")
    print("RESUME NER FINAL TEST")
    print("============================================================")

    print(f"Model path: {MODEL_PATH}")
    print(f"Test data : {TEST_DATA_PATH}")

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"\nNER model not found:\n"
            f"{MODEL_PATH}\n\n"
            f"Train the model first."
        )

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    print("\nLoading trained NER model...")

    nlp = spacy.load(MODEL_PATH)

    print("✓ Model loaded")

    # --------------------------------------------------------
    # LOAD TEST DATA
    # --------------------------------------------------------

    print("\nLoading test data...")

    test_data = load_test_data(
        TEST_DATA_PATH
    )

    # --------------------------------------------------------
    # VALIDATE TEST DATA
    # --------------------------------------------------------

    print("\nValidating test annotations...")

    for i, item in enumerate(test_data, start=1):

        resume_id = item.get(
            "resume_id",
            f"resume_{i}"
        )

        validate_entities(
            item["text"],
            item["entities"],
            resume_id
        )

    print(
        f"✓ All {len(test_data)} test resumes validated"
    )

    # --------------------------------------------------------
    # FINAL EVALUATION
    # --------------------------------------------------------

    evaluate_model(
        nlp,
        test_data
    )


if __name__ == "__main__":
    main()