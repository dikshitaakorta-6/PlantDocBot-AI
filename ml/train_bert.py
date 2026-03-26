import os
import json
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from config import *

# ── Device Setup ─────────────────────────────────────────
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"  Using device: {device}")

# ── Load Corpus ──────────────────────────────────────────
def load_corpus():
    corpus_path = os.path.join(SYMPTOM_DIR, "symptom_corpus.json")
    label_map_path = os.path.join(SYMPTOM_DIR, "label_map.json")

    with open(corpus_path, "r") as f:
        corpus = json.load(f)

    with open(label_map_path, "r") as f:
        label2id = json.load(f)

    texts  = [item["text"]     for item in corpus]
    labels = [item["label_id"] for item in corpus]

    return texts, labels, label2id

# ── Dataset Class ────────────────────────────────────────
class SymptomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts     = texts
        self.labels    = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "input_ids"      : encoding["input_ids"].squeeze(),
            "attention_mask" : encoding["attention_mask"].squeeze(),
            "label"          : torch.tensor(self.labels[idx], dtype=torch.long)
        }

# ── Training Function ────────────────────────────────────
def train_epoch(model, loader, optimizer, scheduler):
    model.train()
    total_loss = 0
    correct    = 0
    total      = 0

    for batch in loader:
        input_ids      = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels         = batch["label"].to(device)

        optimizer.zero_grad()
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()
        preds       = outputs.logits.argmax(dim=1)
        correct    += (preds == labels).sum().item()
        total      += labels.size(0)

    return total_loss / len(loader), correct / total

# ── Evaluation Function ──────────────────────────────────
def evaluate(model, loader):
    model.eval()
    total_loss = 0
    correct    = 0
    total      = 0
    all_preds  = []
    all_labels = []

    with torch.no_grad():
        for batch in loader:
            input_ids      = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels         = batch["label"].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            total_loss += outputs.loss.item()
            preds       = outputs.logits.argmax(dim=1)
            correct    += (preds == labels).sum().item()
            total      += labels.size(0)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return total_loss / len(loader), correct / total, all_preds, all_labels

# ── Main ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("   PlantDocBot — BERT Symptom Classifier Training")
    print("=" * 55)

    # Load data
    print("\n Loading symptom corpus...")
    texts, labels, label2id = load_corpus()
    id2label = {v: k for k, v in label2id.items()}
    num_classes = len(label2id)
    print(f"  Total samples : {len(texts)}")
    print(f"  Classes       : {num_classes}")

    # Train/val split
    X_train, X_val, y_train, y_val = train_test_split(
    texts, labels,
    test_size=0.3,
    random_state=RANDOM_SEED
)
    print(f"   Train samples : {len(X_train)}")
    print(f"   Val samples   : {len(X_val)}")

    # Load tokenizer and model
    print("\n Loading BERT tokenizer and model...")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model     = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=num_classes
    )
    model.to(device)

    # Create datasets
    train_dataset = SymptomDataset(X_train, y_train, tokenizer)
    val_dataset   = SymptomDataset(X_val,   y_val,   tokenizer)
    train_loader  = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader    = DataLoader(val_dataset,   batch_size=8, shuffle=False)

    # Optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
    total_steps = len(train_loader) * 10
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=total_steps // 10,
        num_training_steps=total_steps
    )

    # Training loop
    print("\n Training BERT model...")
    best_val_acc = 0
    os.makedirs(MODELS_DIR, exist_ok=True)

    for epoch in range(10):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, scheduler)
        val_loss, val_acc, preds, true_labels = evaluate(model, val_loader)

        print(f"  Epoch {epoch+1:02d}/10 | "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | "
              f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.2f}%")

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            model.save_pretrained(BERT_MODEL_PATH)
            tokenizer.save_pretrained(BERT_MODEL_PATH)
            print(f"   Best model saved! Val Acc: {val_acc*100:.2f}%")

    # Final report
    print("\n Classification Report:")
    print(classification_report(
        true_labels, preds,
        target_names=list(label2id.keys())
    ))

    # Save label map with model
    label_map_save = os.path.join(BERT_MODEL_PATH, "label_map.json")
    with open(label_map_save, "w") as f:
        json.dump({"label2id": label2id, "id2label": id2label}, f, indent=2)

    print(f"\n BERT model saved to: {BERT_MODEL_PATH}")
    print(f" Best Val Accuracy: {best_val_acc*100:.2f}%")
    print(" BERT Training Complete!")