import json
import random
from pathlib import Path

import spacy
from spacy.training import Example

from src.extraction.ner_labels import RESUME_NER_LABELS
from src.extraction.ner_data import (
    load_training_data,
    validate_training_data,
)


# ==========================================================
# PROJECT PATHS
# ==========================================================

# train_ner.py is located at:
# resume_matching_engine/src/ner_training/train_ner.py
#
# parents[0] = ner_training
# parents[1] = src
# parents[2] = resume_matching_engine

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "ner"
    / "training_data.json"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "resume_ner"
)


# ==========================================================
# CONFIGURATION
# ==========================================================

N_ITER = 30
DEV_SPLIT = 0.10
SEED = 42

BATCH_START = 4
BATCH_END = 32
BATCH_GROWTH = 1.001

DROPOUT = 0.2


# ==========================================================
# GPU / CPU SETUP
# ==========================================================

print("=" * 60)
print("CHECKING GPU / CPU")
print("=" * 60)

try:
    gpu_available = spacy.prefer_gpu()

    if gpu_available:
        print("🚀 GPU detected!")
        print("Training device: GPU")
    else:
        print("⚠️ GPU not available.")
        print("Training device: CPU")

except Exception as e:
    gpu_available = False

    print("⚠️ Could not enable GPU.")
    print(f"Reason: {e}")
    print("Training device: CPU")

print("=" * 60)


# ==========================================================
# SHOW PATHS
# ==========================================================

print("\nProject root:")
print(PROJECT_ROOT)

print("\nTraining data:")
print(DATA_PATH)

print("\nModel output:")
print(MODEL_DIR)


# ==========================================================
# CHECK DATA FILE
# ==========================================================

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"\nTraining data not found:\n{DATA_PATH}"
    )


# ==========================================================
# LOAD TRAINING DATA
# ==========================================================

print("\n" + "=" * 60)
print("LOADING TRAINING DATA")
print("=" * 60)

raw_data = load_training_data(DATA_PATH)

print(f"Total resumes loaded: {len(raw_data)}")


# ==========================================================
# VALIDATE TRAINING DATA
# ==========================================================

print("\n" + "=" * 60)
print("VALIDATING TRAINING DATA")
print("=" * 60)

validate_training_data(
    raw_data,
    RESUME_NER_LABELS
)

print("✓ Training data validation passed")


# ==========================================================
# TRAIN / DEV SPLIT
# ==========================================================

random.seed(SEED)

data = list(raw_data)
random.shuffle(data)

dev_size = int(len(data) * DEV_SPLIT)

dev_data = data[:dev_size]
train_data = data[dev_size:]


print("\n" + "=" * 60)
print("DATASET SPLIT")
print("=" * 60)

print(f"Total resumes : {len(data)}")
print(f"Training      : {len(train_data)}")
print(f"Development   : {len(dev_data)}")

print("=" * 60)


# ==========================================================
# CREATE BLANK SPACY MODEL
# ==========================================================

print("\nCreating blank spaCy English model...")

nlp = spacy.blank("en")

ner = nlp.add_pipe("ner")


# ==========================================================
# ADD NER LABELS
# ==========================================================

for label in RESUME_NER_LABELS:
    ner.add_label(label)

print(
    f"✓ Added {len(RESUME_NER_LABELS)} NER labels"
)


# ==========================================================
# CONVERT DATA TO SPACY EXAMPLES
# ==========================================================

def create_examples(nlp, dataset):

    examples = []

    for item in dataset:

        text = item["text"]

        entities = []

        for entity in item["entities"]:

            start = entity["start"]
            end = entity["end"]
            label = entity["label"]

            entities.append(
                (start, end, label)
            )

        doc = nlp.make_doc(text)

        example = Example.from_dict(
            doc,
            {
                "entities": entities
            }
        )

        examples.append(example)

    return examples


print("\n" + "=" * 60)
print("CREATING SPACY EXAMPLES")
print("=" * 60)

train_examples = create_examples(
    nlp,
    train_data
)

dev_examples = create_examples(
    nlp,
    dev_data
)

print(
    f"✓ Training examples : {len(train_examples)}"
)

print(
    f"✓ Dev examples      : {len(dev_examples)}"
)


# ==========================================================
# INITIALIZE MODEL
# ==========================================================

print("\n" + "=" * 60)
print("INITIALIZING NER MODEL")
print("=" * 60)

optimizer = nlp.initialize(
    get_examples=lambda: train_examples
)

print("✓ Model initialized")


# ==========================================================
# EVALUATION FUNCTION
# ==========================================================

def evaluate_model(nlp, examples):

    true_entities = 0
    predicted_entities = 0
    correct_entities = 0

    for example in examples:

        predicted_doc = nlp(example.text)

        predicted = {
            (
                ent.start_char,
                ent.end_char,
                ent.label_
            )
            for ent in predicted_doc.ents
        }

        gold = {
            (
                ent.start_char,
                ent.end_char,
                ent.label_
            )
            for ent in example.reference.ents
        }

        true_entities += len(gold)
        predicted_entities += len(predicted)

        correct_entities += len(
            predicted.intersection(gold)
        )

    if predicted_entities > 0:
        precision = (
            correct_entities /
            predicted_entities
        )
    else:
        precision = 0.0

    if true_entities > 0:
        recall = (
            correct_entities /
            true_entities
        )
    else:
        recall = 0.0

    if precision + recall > 0:

        f1 = (
            2 * precision * recall
            /
            (precision + recall)
        )

    else:
        f1 = 0.0

    return precision, recall, f1


# ==========================================================
# TRAINING
# ==========================================================

print("\n" + "=" * 60)
print("STARTING NER TRAINING")
print("=" * 60)

print(f"Iterations : {N_ITER}")
print(f"Dropout    : {DROPOUT}")

if gpu_available:
    print("Device     : GPU")
else:
    print("Device     : CPU")

print("=" * 60)


best_f1 = 0.0


for iteration in range(N_ITER):

    random.shuffle(train_examples)

    losses = {}

    batches = spacy.util.minibatch(
        train_examples,
        size=spacy.util.compounding(
            BATCH_START,
            BATCH_END,
            BATCH_GROWTH
        )
    )

    for batch in batches:

        nlp.update(
            batch,
            drop=DROPOUT,
            sgd=optimizer,
            losses=losses
        )

    # ------------------------------------------------------
    # DEV EVALUATION
    # ------------------------------------------------------

    precision, recall, f1 = evaluate_model(
        nlp,
        dev_examples
    )

    loss = losses.get(
        "ner",
        0.0
    )

    print(
        f"\nIteration {iteration + 1:02d} | "
        f"Loss: {loss:.4f} | "
        f"Dev Precision: {precision:.4f} | "
        f"Dev Recall: {recall:.4f} | "
        f"Dev F1: {f1:.4f}"
    )

    # ------------------------------------------------------
    # SAVE BEST MODEL
    # ------------------------------------------------------

    if f1 > best_f1:

        best_f1 = f1

        MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        nlp.to_disk(
            MODEL_DIR
        )

        print(
            f"   ✓ Best model saved "
            f"(Dev F1 = {best_f1:.4f})"
        )


# ==========================================================
# SAVE TRAINING INFORMATION
# ==========================================================

training_info = {
    "total_resumes": len(data),
    "training_resumes": len(train_data),
    "dev_resumes": len(dev_data),
    "num_labels": len(
        RESUME_NER_LABELS
    ),
    "labels": RESUME_NER_LABELS,
    "iterations": N_ITER,
    "best_dev_f1": best_f1,
    "device": (
        "GPU"
        if gpu_available
        else "CPU"
    )
}


MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    MODEL_DIR / "training_info.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        training_info,
        f,
        indent=2
    )


# ==========================================================
# TRAINING COMPLETE
# ==========================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(
    f"Best Dev F1 : {best_f1:.4f}"
)

print(
    f"Model saved : {MODEL_DIR}"
)

print(
    "Device      : "
    + (
        "GPU"
        if gpu_available
        else "CPU"
    )
)

print("=" * 60)