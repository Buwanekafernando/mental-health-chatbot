from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from datetime import datetime, timedelta
from collections import Counter

from app.services.emotion_service import detect_emotion
from app.database import chat_collection

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
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

    chat_collection.insert_one({
        "user_id": data.user_id,
        "message": data.message,
        "emotion": emotion,
        "reply": reply,
        "timestamp": datetime.now()
    })

    return{
        "emotion": emotion,
        "reply": reply
    }

@router.get("/history/{user_id}")
def get_chat_history(user_id: str):
    chats = chat_collection.find({"user_id": user_id}).sort("timestamp", 1)
    
    history = []
    for chat in chats:
        history.append({
            "id": str(chat["_id"]),
            "message": chat["message"],
            "emotion": chat["emotion"],
            "reply": chat["reply"],
            "timestamp": chat["timestamp"]
        })

    return {
        user_id: user_id,
        history: history
    }


def weekly_sentiment_summary(user_id: str):
    one_week_ago = datetime.now() - timedelta(days=7)
    
    chats = chat_collection.find({
        "user_id": user_id,
        "timestamp": {"$gte": one_week_ago}
    })

    emotion = [chat["emotion"] for chat in chats]

    if not emotion:
        return {
            "user_id": user_id,
            "summary": "No chat history found for the last days"
        }