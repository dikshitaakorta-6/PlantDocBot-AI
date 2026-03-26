from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from models.image_model import predict_disease
from models.nlp_model import predict_from_text
from services.treatment_service import get_treatment

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/image")
async def diagnose_image(file: UploadFile = File(...)):
    """Diagnose plant disease from uploaded leaf image."""

    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG or PNG image."
        )

    image_bytes = await file.read()

    # Run CNN inference
    result = predict_disease(image_bytes)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    if result["status"] == "low_confidence":
        return {
            "input_type"    : "image",
            "status"        : "low_confidence",
            "message"       : result["message"],
            "confidence"    : result["confidence"],
            "top_predictions": result.get("top_predictions", [])
        }

    # Get treatment
    treatment = get_treatment(result["disease_label"])

    return {
        "input_type"   : "image",
        "status"       : "success",
        "disease_label": result["disease_label"],
        "confidence"   : result["confidence"],
        "treatment"    : treatment["data"],
        "top_predictions": result.get("top_predictions", [])
    }

@router.post("/text")
async def diagnose_text(input: TextInput):
    """Diagnose plant disease from symptom text description."""

    if not input.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide a symptom description."
        )

    # Run BERT inference
    result = predict_from_text(input.text)

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    if result["status"] == "low_confidence":
        return {
            "input_type": "text",
            "status"    : "low_confidence",
            "message"   : result["message"],
            "confidence": result["confidence"]
        }

    # Get treatment
    treatment = get_treatment(result["disease_label"])

    return {
        "input_type"   : "text",
        "status"       : "success",
        "disease_label": result["disease_label"],
        "confidence"   : result["confidence"],
        "treatment"    : treatment["data"]
    }