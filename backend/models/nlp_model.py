import torch
import json
import os
import sys
from transformers import BertTokenizer, BertForSequenceClassification

sys.path.append(os.path.join(os.path.dirname(__file__), "../../ml"))
from config import BERT_MODEL_PATH, CONFIDENCE_THRESHOLD

print("📂 Loading BERT model...")

# Load label map
label_map_path = os.path.join(BERT_MODEL_PATH, "label_map.json")
with open(label_map_path, "r") as f:
    label_data = json.load(f)

label2id = label_data["label2id"]
id2label = {int(k): v for k, v in label_data["id2label"].items()}

# Load model and tokenizer
tokenizer  = BertTokenizer.from_pretrained(BERT_MODEL_PATH)
bert_model = BertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
bert_model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

def predict_from_text(symptom_text: str) -> dict:
    """Run BERT inference on symptom text."""
    try:
        encoding = tokenizer(
            symptom_text,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        input_ids      = encoding["input_ids"].to(device)
        attention_mask = encoding["attention_mask"].to(device)

        with torch.no_grad():
            outputs     = bert_model(input_ids=input_ids, attention_mask=attention_mask)
            probs       = torch.softmax(outputs.logits, dim=1)
            confidence  = float(probs.max())
            class_idx   = int(probs.argmax())

        disease_label = id2label.get(class_idx, "Unknown")

        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "status"    : "low_confidence",
                "message"   : "Could not determine disease from description. Please provide more details or upload an image.",
                "confidence": round(confidence * 100, 2)
            }

        return {
            "status"       : "success",
            "disease_label": disease_label,
            "confidence"   : round(confidence * 100, 2)
        }

    except Exception as e:
        return {
            "status" : "error",
            "message": f"Text processing failed: {str(e)}"
        }