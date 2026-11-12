import json
from pathlib import Path


def load_training_data(file_path: str):
    """
    Load NER dataset from JSON.

    Expected format:

    {
        "resume_id": "resume_0001",
        "text": "John is a Python developer.",
        "entities": [
            {
                "start": 11,
                "end": 17,
                "text": "Python",
                "label": "PROGRAMMING_LANGUAGE"
            }
        ]
    }
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Training data not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def validate_training_data(
    data,
    allowed_labels=None
):
    """
    Validate NER data that already contains
    character offsets.

    Checks:

    1. start/end exist
    2. start/end are integers
    3. offsets are inside text
    4. start < end
    5. label is valid
    6. text[start:end] matches entity text
    7. entities do not overlap
    """

    errors = []

    for example_index, example in enumerate(data):

        # --------------------------------------------------
        # CHECK TEXT
        # --------------------------------------------------

        if "text" not in example:

            errors.append(
                f"Example {example_index}: "
                f"missing 'text'"
            )

            continue

        text = example["text"]

        # --------------------------------------------------
        # CHECK ENTITIES
        # --------------------------------------------------

        if "entities" not in example:

            errors.append(
                f"Example {example_index}: "
                f"missing 'entities'"
            )

            continue

        entities = example["entities"]

        previous_entities = []

        for entity_index, entity in enumerate(entities):

            # --------------------------------------------------
            # CHECK ENTITY FORMAT
            # --------------------------------------------------

            if not isinstance(entity, dict):

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"entity must be a dictionary"
                )

                continue

            required_fields = {
                "start",
                "end",
                "text",
                "label"
            }

            missing_fields = (
                required_fields
                - set(entity.keys())
            )

            if missing_fields:

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"missing fields: "
                    f"{missing_fields}"
                )

                continue

            # --------------------------------------------------
            # GET VALUES
            # --------------------------------------------------

            start = entity["start"]
            end = entity["end"]
            entity_text = entity["text"]
            label = entity["label"]

            # --------------------------------------------------
            # CHECK OFFSET TYPES
            # --------------------------------------------------

            if not isinstance(start, int):

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"start must be an integer"
                )

                continue

            if not isinstance(end, int):

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"end must be an integer"
                )

                continue

            # --------------------------------------------------
            # CHECK OFFSET RANGE
            # --------------------------------------------------

            if start < 0:

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"negative start offset: {start}"
                )

                continue

            if end > len(text):

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"end offset {end} exceeds "
                    f"text length {len(text)}"
                )

                continue

            if start >= end:

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"invalid span {start}:{end}"
                )

                continue

            # --------------------------------------------------
            # CHECK LABEL
            # --------------------------------------------------

            if (
                allowed_labels is not None
                and label not in allowed_labels
            ):

                errors.append(
                    f"Example {example_index}, "
                    f"entity {entity_index}: "
                    f"unknown label {label!r}"
                )

            # --------------------------------------------------
            # CRITICAL OFFSET CHECK
            # --------------------------------------------------

            extracted_text = text[start:end]

            if extracted_text != entity_text:

                errors.append(
                    f"\nExample {example_index}"
                    f" ({example.get('resume_id', 'unknown')}):\n"
                    f"Entity {entity_index} offset mismatch:\n"
                    f"  Expected: {entity_text!r}\n"
                    f"  Found   : {extracted_text!r}\n"
                    f"  Span    : {start}:{end}"
                )

            # --------------------------------------------------
            # CHECK OVERLAPPING ENTITIES
            # --------------------------------------------------

            for (
                previous_start,
                previous_end,
                previous_label
            ) in previous_entities:

                if (
                    start < previous_end
                    and end > previous_start
                ):

                    errors.append(
                        f"Example {example_index}: "
                        f"overlapping entities:\n"
                        f"  {previous_start}:{previous_end} "
                        f"{previous_label}\n"
                        f"  {start}:{end} "
                        f"{label}"
                    )

            previous_entities.append(
                (
                    start,
                    end,
                    label
                )
            )

    # ------------------------------------------------------
    # REPORT ERRORS
    # ------------------------------------------------------

    if errors:

        preview = "\n".join(
            errors[:20]
        )

        raise ValueError(
            "\n"
            + "=" * 70
            + "\n"
            + "NER DATA VALIDATION FAILED"
            + "\n"
            + "=" * 70
            + "\n\n"
            + preview
            + "\n\n"
            + f"Total errors: {len(errors)}"
        )

    return True