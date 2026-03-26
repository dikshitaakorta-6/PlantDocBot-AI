import os

# ── Base Paths ──────────────────────────────────────────
BASE_DIR         = r"C:\Users\HP\Downloads\PLANTBOT AI\plantdocbot"
DATA_DIR         = os.path.join(BASE_DIR, "data")

PLANTVILLAGE_DIR = os.path.join(DATA_DIR, "PlantVillage")   # capital P and V
PLANTDOC_DIR     = os.path.join(DATA_DIR, "plantdoc")
SYMPTOM_DIR      = os.path.join(DATA_DIR, "symptom_corpus")

# ── Processed Output ────────────────────────────────────
PROCESSED_DIR    = os.path.join(DATA_DIR, "processed")
PROCESSED_TRAIN  = os.path.join(PROCESSED_DIR, "train")
PROCESSED_VAL    = os.path.join(PROCESSED_DIR, "val")
PROCESSED_TEST   = os.path.join(PROCESSED_DIR, "test")

# ── Image Settings ──────────────────────────────────────
IMAGE_SIZE    = (224, 224)
BATCH_SIZE    = 32
VAL_SPLIT     = 0.15
TEST_SPLIT    = 0.10
RANDOM_SEED   = 42

# ── Model Paths ─────────────────────────────────────────
MODELS_DIR       = os.path.join(BASE_DIR, "ml", "saved_models")
CNN_MODEL_PATH   = os.path.join(MODELS_DIR, "plant_disease_cnn.h5")
BERT_MODEL_PATH  = os.path.join(MODELS_DIR, "plant_disease_bert")

# ── Confidence ──────────────────────────────────────────
CONFIDENCE_THRESHOLD = 0.40 










