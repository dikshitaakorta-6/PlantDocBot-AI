from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from models.nlp_model import predict_from_text
from services.treatment_service import get_treatment

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    message: str
    history: List[Message] = []

@router.post("/")
async def chat(input: ChatInput):
    """Handle conversational chat input."""

    user_message = input.message.lower().strip()

    # Greeting detection
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if any(g in user_message for g in greetings):
        return {
            "reply": " Hello! I'm PlantDocBot. I can help diagnose plant diseases.\n\nYou can:\n• **Upload a leaf image** for visual diagnosis\n• **Describe symptoms** and I'll analyze them\n\nWhat's wrong with your plant?",
            "type" : "greeting"
        }

    # Help detection
    if "help" in user_message or "what can you do" in user_message:
        return {
            "reply": "I can help you with:\n\n🔍 **Image Diagnosis** — Upload a photo of a diseased leaf\n💬 **Symptom Analysis** — Describe what you see on your plant\n💊 **Treatment Advice** — Get organic and chemical remedies\n🛡️ **Prevention Tips** — Learn how to protect your crops",
            "type" : "help"
        }

    # Run NLP diagnosis on message
    result = predict_from_text(input.message)

    if result["status"] == "low_confidence":
        return {
            "reply": f"I'm not sure about that. Could you describe the symptoms in more detail?\n\nFor example:\n• What color are the spots?\n• Which part of the plant is affected?\n• How fast is it spreading?\n\nOr you can **upload a photo** for accurate diagnosis.",
            "type" : "clarification"
        }

    disease_label = result["disease_label"]
    confidence    = result["confidence"]
    treatment     = get_treatment(disease_label)

    if treatment["status"] == "not_found":
        return {
            "reply": "I detected something unusual but couldn't find a match in my database. Please consult a local agricultural expert or upload a clearer image.",
            "type" : "not_found"
        }

    data = treatment["data"]
    reply = (
        f" **Diagnosis:** {data['disease_name']}\n"
        f" **Plant:** {data['plant']}\n"
        f" **Severity:** {data['severity']}\n"
        f" **Confidence:** {confidence}%\n\n"
        f" **Description:** {data['description']}\n\n"
        f" **Organic Remedy:** {data['organic_remedy'][0]}\n"
        f" **Chemical Remedy:** {data['chemical_remedy'][0] if data['chemical_remedy'] else 'Not required'}\n\n"
        f"Would you like detailed treatment steps?"
    )

    return {
        "reply"        : reply,
        "type"         : "diagnosis",
        "disease_label": disease_label,
        "confidence"   : confidence,
        "treatment"    : data
    }



