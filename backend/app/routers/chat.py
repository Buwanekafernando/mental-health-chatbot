from fastapi import APIRouter
from pydantic import BaseModel
from app.services.emotion-service import detect_emotion

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    emotion: str
    reply: str

@router.post("/analyze",response_model=ChatResponse)
def analyze_message(data:ChatRequest):
    emotion = detect_emotion(data.message)
    
    response = {
        "sad": "I'm really sorry you're feeling this way. You're not alone 💙",
        "happy": "That's great to hear! Keep enjoying the moment 😊",
        "angry": "It sounds frustrating. Want to talk about what happened?",
        "fear": "That sounds scary. Take a deep breath with me.",
        "neutral": "I'm here with you. Tell me more."
    }

    reply = response.get(emotion, "I'm here with you. Tell me more.")

    return{
        "emotion": emotion,
        "reply": reply
    }

