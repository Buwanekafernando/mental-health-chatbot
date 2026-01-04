from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from datetime import datetime, timedelta
from collections import Counter


from app.services.emotion_service import detect_emotion
from app.database import chat_collection
from app.services.crisis_service import detect_crisis

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

@router.get("/weekly-summary/{user_id}")
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
            "summary": {},
            "message": "No data available for the last 7 days"
        }

    emotion_counts = Counter(emotions)
    total = sum(emotion_counts.values())

    summary = {
        emotion: round((count / total) * 100, 2)
        for emotion, count in emotion_counts.items()
    }

    # Simple AI insight
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)

    insight_map = {
        "happy": "You've been feeling positive overall this week 😊",
        "sad": "It seems like this week was emotionally heavy 💙",
        "stressed": "You've experienced a lot of stress this week 🌱",
        "angry": "There were moments of frustration this week 😤",
        "neutral": "Your emotions were fairly balanced this week ⚖️"
    }

    return {
        "user_id": user_id,
        "summary": summary,
        "dominant_emotion": dominant_emotion,
        "insight": insight_map.get(dominant_emotion, "Thank you for sharing your feelings.")
    }


@router.post("/analyze", response_model=ChatResponse)
def analyze_message(data: ChatRequest):

    # 🚨 Crisis check FIRST
    if detect_crisis(data.message):
        reply = (
            "I'm really sorry that you're feeling this much pain 💙\n\n"
            "You deserve support and help. Please consider reaching out to:\n"
            "• A trusted person\n"
            "• A mental health professional\n"
            "• Emergency services in your country\n\n"
            "If you're in immediate danger, please contact local emergency services."
        )

        emotion = "crisis"

        chat_collection.insert_one({
            "user_id": data.user_id,
            "message": data.message,
            "emotion": emotion,
            "reply": reply,
            "timestamp": datetime.utcnow(),
            "crisis": True
        })

        return {
            "emotion": emotion,
            "reply": reply
        }

    # Normal flow
    emotion = detect_emotion(data.message)
    ...