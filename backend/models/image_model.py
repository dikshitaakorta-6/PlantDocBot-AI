import numpy as np
import tensorflow as tf
from PIL import Image
import io
import sys
import os

# Add ml/ folder to path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), "../../ml"))
from config import CNN_MODEL_PATH, IMAGE_SIZE, CONFIDENCE_THRESHOLD

# ── Load model once at startup ───────────────────────────
print("📂 Loading CNN model...")
cnn_model = tf.keras.models.load_model(CNN_MODEL_PATH)

# Class labels (must match training order)
CLASS_LABELS = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Corn___Common_rust",
    "Grape___Black_rot",
    "Healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_YellowLeaf_Curl_Virus",
    "Tomato___Target_Spot"
]

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocess image bytes for CNN inference."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(IMAGE_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_disease(image_bytes: bytes) -> dict:
    """Run CNN inference on image bytes."""
    try:
        img_array = preprocess_image(image_bytes)
        predictions = cnn_model.predict(img_array, verbose=0)
        confidence = float(np.max(predictions))
        class_idx = int(np.argmax(predictions))

        # Get top 3 predictions
        top3_idx = np.argsort(predictions[0])[::-1][:3]
        top3 = [
            {
                "disease"   : CLASS_LABELS[i] if i < len(CLASS_LABELS) else f"Class_{i}",
                "confidence": round(float(predictions[0][i]) * 100, 2)
            }
            for i in top3_idx
        ]

        # Low confidence check
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "status"        : "low_confidence",
                "message"       : "Image unclear. Please upload a clearer photo of the leaf.",
                "confidence"    : round(confidence * 100, 2),
                "top_predictions": top3
            }

        disease_label = CLASS_LABELS[class_idx] if class_idx < len(CLASS_LABELS) else f"Class_{class_idx}"

        return {
            "status"         : "success",
            "disease_label"  : disease_label,
            "confidence"     : round(confidence * 100, 2),
            "top_predictions": top3
        }

    except Exception as e:
        return {
            "status" : "error",
            "message": f"Image processing failed: {str(e)}"
        }