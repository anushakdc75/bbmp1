import os
import pandas as pd
import torch

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib


# ---------------- CONFIG ----------------

MODEL_NAME = "intfloat/e5-base-v2"
DATA_FILE = "train_topic_data.csv"
OUT_DIR = "models/e5_topic_classifier"

os.makedirs(OUT_DIR, exist_ok=True)


# ---------------- LOAD DATA ----------------

print("Loading dataset...")

df = pd.read_csv(DATA_FILE)

texts = df["text"].astype(str).tolist()
labels = df["label_topic"].astype(str).tolist()

print("Total samples:", len(texts))


# ---------------- LABEL ENCODING ----------------

le = LabelEncoder()
labels_encoded = le.fit_transform(labels)

num_labels = len(le.classes_)

print("Number of classes:", num_labels)


# ---------------- TRAIN / TEST SPLIT ----------------

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels_encoded,
    test_size=0.2,
    random_state=42,
    stratify=labels_encoded
)

print("Train size:", len(X_train))
print("Test size :", len(X_test))


# ---------------- TOKENIZER ----------------

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )


# ---------------- HF DATASET ----------------

train_df = pd.DataFrame({
    "text": X_train,
    "label": y_train
})

test_df = pd.DataFrame({
    "text": X_test,
    "label": y_test
})


train_ds = Dataset.from_pandas(train_df)
test_ds = Dataset.from_pandas(test_df)


train_ds = train_ds.map(tokenize, batched=True)
test_ds = test_ds.map(tokenize, batched=True)


train_ds.set_format(
    "torch",
    columns=["input_ids", "attention_mask", "label"]
)

test_ds.set_format(
    "torch",
    columns=["input_ids", "attention_mask", "label"]
)


# ---------------- LOAD MODEL ----------------

print("Loading model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels
)


# ---------------- FREEZE FIRST 6 LAYERS ----------------

print("Freezing first 6 layers...")

for name, param in model.named_parameters():

    if "encoder.layer." in name:

        layer_num = int(
            name.split("encoder.layer.")[1].split(".")[0]
        )

        if layer_num < 6:
            param.requires_grad = False


# ---------------- TRAINING ARGUMENTS ----------------

training_args = TrainingArguments(

    output_dir=OUT_DIR,

    # NEW PARAM NAME (for transformers 4.57+)
    eval_strategy="epoch",

    save_strategy="epoch",

    learning_rate=2e-5,

    per_device_train_batch_size=32,
    per_device_eval_batch_size=16,

    num_train_epochs=2,


    weight_decay=0.01,

    logging_dir="./logs",

    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",

    save_total_limit=2,

    report_to="none"   # disables wandb etc
)


# ---------------- TRAINER ----------------

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds
)


# ---------------- TRAIN ----------------

print("\n🚀 Starting training...\n")

trainer.train()


# ---------------- SAVE MODEL ----------------

print("\nSaving model...")

model.save_pretrained(OUT_DIR)
tokenizer.save_pretrained(OUT_DIR)

joblib.dump(
    le,
    os.path.join(OUT_DIR, "label_encoder.pkl")
)


print("\n✅ E5 MODEL TRAINING COMPLETED")
print("Saved in:", OUT_DIR)