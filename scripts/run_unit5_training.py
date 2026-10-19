#!/usr/bin/env python3
"""
Runs Sections 1 to 5 of takemeter.ipynb:
- Hardware check
- Check dataset
- Stratified 70/15/15 split
- Train DistilBERT classifier
- Evaluate on test split, write results.json and test_split.csv
- Updates takemeter.ipynb with cell outputs
"""

import os
import json
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    TrainingArguments, Trainer, set_seed,
)
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support

# ── Section 1: Setup ──────────────────────────────────────────────────────────
def pick_device():
    if torch.cuda.is_available():
        return "cuda", torch.cuda.get_device_name(0)
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps", "Apple Silicon GPU (MPS)"
    return "cpu", "CPU"

DEVICE, DEVICE_NAME = pick_device()
print(f"device: {DEVICE}  ({DEVICE_NAME})")
print(f"torch:  {torch.__version__}")

NAME  = "Quang Ngo"
EMAIL = "ngotuanquang92@gmail.com"
REPO_DIR = Path.cwd()
print(f"Working in: {REPO_DIR}")
print(f"Results will be labelled: {NAME} <{EMAIL}>")

# ── Section 2: Your labels ───────────────────────────────────────────────────
LABELS = ["analysis", "hot_take", "reaction", "joke"]
BASE_MODEL = "distilbert-base-uncased"
EPOCHS = 3
LEARNING_RATE = 2e-5
BATCH_SIZE = 16
MAX_LENGTH = 128
SEED = 42

print(f"{len(LABELS)} labels: {', '.join(LABELS)}")
print(f"seed {SEED}, {EPOCHS} epochs, lr {LEARNING_RATE}, batch {BATCH_SIZE}")

CSV = "labels.csv"
df = pd.read_csv(CSV)
print(f"Loaded {CSV}: {len(df)} rows")
print(f"Columns: {', '.join(df.columns)}")

def check_dataset(df, labels):
    problems, warnings = [], []
    for column in ("text", "label"):
        if column not in df.columns:
            problems.append(f"No '{column}' column. Found: {', '.join(df.columns)}")
    if problems:
        return problems, warnings

    blank = df["text"].isna().sum() + (df["text"].astype(str).str.strip() == "").sum()
    if blank:
        problems.append(f"{blank} rows have an empty text column.")

    found = set(df["label"].dropna().astype(str).str.strip().unique())
    expected = set(labels)

    unknown = found - expected
    if unknown:
        problems.append(f"Labels in CSV that aren't in LABELS: {sorted(unknown)}")

    unused = expected - found
    if unused:
        warnings.append(f"Labels in LABELS that never appear in your CSV: {sorted(unused)}")

    counts = df["label"].value_counts()
    total = len(df)
    for label, count in counts.items():
        share = count / total
        if share > 0.70:
            problems.append(f"'{label}' is {share:.0%} of data. Over 70% cap.")
        elif share > 0.60:
            warnings.append(f"'{label}' is {share:.0%} of data. Getting lopsided.")

    if total < 150:
        warnings.append(f"{total} rows. The brief's floor is 150.")
    elif total < 200:
        warnings.append(f"{total} rows. Under 200.")

    duplicates = df["text"].duplicated().sum()
    if duplicates:
        warnings.append(f"{duplicates} duplicate posts.")

    for label, count in counts.items():
        if count < 20:
            warnings.append(f"Only {count} examples of '{label}'.")

    return problems, warnings

problems, warnings = check_dataset(df, LABELS)
for w in warnings:
    print(f"[look at]  {w}")
for p in problems:
    print(f"[FIX ME]   {p}")

if problems:
    raise SystemExit("Fix problems before training.")
print("\nData looks fine.\n")
print(df["label"].value_counts().to_string())

# ── Section 3: Split ──────────────────────────────────────────────────────────
def split_dataset(df, seed, test_size=0.15, val_size=0.15):
    def _stratify_on(frame):
        counts = frame["label"].value_counts()
        return frame["label"] if counts.min() >= 2 else None

    rest, test = train_test_split(
        df, test_size=test_size, random_state=seed, stratify=_stratify_on(df)
    )
    val_share = val_size / (1 - test_size)
    train, val = train_test_split(
        rest, test_size=val_share, random_state=seed, stratify=_stratify_on(rest)
    )
    return (
        train.reset_index(drop=True),
        val.reset_index(drop=True),
        test.reset_index(drop=True),
    )

def describe_splits(train, val, test, labels):
    table = pd.DataFrame({
        "train": train["label"].value_counts(),
        "val": val["label"].value_counts(),
        "test": test["label"].value_counts(),
    }).reindex(labels).fillna(0).astype(int)

    thin = [label for label in labels if table.loc[label, "test"] < 8]
    return table, thin

train_df, val_df, test_df = split_dataset(df, SEED)
table, thin = describe_splits(train_df, val_df, test_df, LABELS)
print(f"\ntrain {len(train_df)}  ·  val {len(val_df)}  ·  test {len(test_df)}\n")
print(table.to_string())
if thin:
    for label in thin:
        n = table.loc[label, "test"]
        print(f"[note] '{label}' has only {n} examples in the test split.")

# ── Section 4: Train ──────────────────────────────────────────────────────────
def to_ids(df, labels):
    lookup = {label: i for i, label in enumerate(labels)}
    out = df.copy()
    out["labels"] = out["label"].astype(str).str.strip().map(lookup)
    return out[["text", "labels"]]

def compute_metrics(eval_pred):
    logits, gold = eval_pred
    predicted = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(gold, predicted),
        "f1_macro": f1_score(gold, predicted, average="macro", zero_division=0),
    }

def train_model(train_df, val_df, labels, seed, epochs, learning_rate, batch_size,
                base_model, quiet=False):
    set_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForSequenceClassification.from_pretrained(
        base_model,
        num_labels=len(labels),
        id2label={i: l for i, l in enumerate(labels)},
        label2id={l: i for i, l in enumerate(labels)},
    )

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH)

    train_ds = Dataset.from_pandas(to_ids(train_df, labels)).map(tokenize, batched=True)
    val_ds = Dataset.from_pandas(to_ids(val_df, labels)).map(tokenize, batched=True)

    args = TrainingArguments(
        output_dir="./takemeter_out",
        num_train_epochs=epochs,
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=10,
        seed=seed,
        report_to="none",
        disable_tqdm=quiet,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    return trainer, tokenizer

print("\nStarting training...")
trainer, tokenizer = train_model(
    train_df, val_df, LABELS, SEED, EPOCHS, LEARNING_RATE, BATCH_SIZE, BASE_MODEL
)
print("Trained.")

# ── Section 5: Results ────────────────────────────────────────────────────────
def confidence_report(confidence, gold, predicted):
    right = gold == predicted
    ranked = np.argsort(confidence)
    third = max(1, len(confidence) // 3)
    least, most = ranked[:third], ranked[-third:]

    return {
        "mean_when_right": float(confidence[right].mean()) if right.any() else None,
        "mean_when_wrong": float(confidence[~right].mean()) if (~right).any() else None,
        "accuracy_most_confident_third": float(right[most].mean()),
        "accuracy_least_confident_third": float(right[least].mean()),
        "n_per_third": int(third),
    }

def confusion_counts(gold, predicted, labels):
    matrix = {t: {p: 0 for p in labels} for t in labels}
    for g, p in zip(gold, predicted):
        matrix[labels[int(g)]][labels[int(p)]] += 1
    return matrix

def evaluate(trainer, tokenizer, test_df, labels, seed=None):
    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=MAX_LENGTH)

    test_ds = Dataset.from_pandas(to_ids(test_df, labels)).map(tokenize, batched=True)
    output = trainer.predict(test_ds)

    predicted = np.argmax(output.predictions, axis=-1)
    gold = np.array(output.label_ids)

    scores = output.predictions
    exp = np.exp(scores - scores.max(axis=-1, keepdims=True))
    confidence = (exp / exp.sum(axis=-1, keepdims=True)).max(axis=-1)

    precision, recall, f1, support = precision_recall_fscore_support(
        gold, predicted, labels=list(range(len(labels))), zero_division=0
    )

    return {
        "seed": seed,
        "n_test": int(len(gold)),
        "accuracy": float(accuracy_score(gold, predicted)),
        "f1_macro": float(f1_score(gold, predicted, average="macro", zero_division=0)),
        "per_label": {
            label: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "support": int(support[i]),
            }
            for i, label in enumerate(labels)
        },
        "confusion": confusion_counts(gold, predicted, labels),
        "confidence": confidence_report(confidence, gold, predicted),
    }

results = evaluate(trainer, tokenizer, test_df, LABELS, seed=SEED)
results["device"] = DEVICE
results["device_name"] = DEVICE_NAME
results["torch_version"] = torch.__version__
results["max_length"] = MAX_LENGTH

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

test_df.to_csv("test_split.csv", index=False)

print(f"\naccuracy  {results['accuracy']:.3f}")
print(f"macro F1  {results['f1_macro']:.3f}\n")
for label, scores in results["per_label"].items():
    print(f"  {label:<16} F1 {scores['f1']:.3f}   (n={scores['support']})")

c = results["confidence"]
print(f"\nconfidence   most-sure third {c['accuracy_most_confident_third']:.3f}"
      f"   ·   least-sure third {c['accuracy_least_confident_third']:.3f}")

print("\nWrote results.json and test_split.csv.")
