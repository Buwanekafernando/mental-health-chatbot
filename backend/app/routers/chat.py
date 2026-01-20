from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from collections import Counter


from app.services.emotion_service import detect_emotion
from app.services.crisis_service import detect_crisis
from app.services.jwt_dependency import get_current_user
from app.database import chat_collection
from app.services.gemini_service import generate_supportive_reply
from app.services.memory_service import get_recent_conversation
from app.services.emotion_fusion_service import fuse_emotions
from app.services.face_emotion_service import get_recent_face_emotion


router = APIRouter()



class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    emotion: str
    reply: str



@router.post("/analyze", response_model=ChatResponse)
def analyze_message(
    data: ChatRequest,
    user_email: str = Depends(get_current_user)
):
    user_id = user_email  # JWT-based user identity
    

    
    if detect_crisis(data.message):
        reply = (
            "I'm really sorry that you're feeling this much pain 💙\n\n"
            "You deserve support and help. Please consider reaching out to:\n"
            "• A trusted person\n"
            "• A mental health professional\n"
            "• Emergency services in your country\n\n"
            "If you're in immediate danger, please contact local emergency services."
        )

        chat_collection.insert_one({
            "user_id": user_id,
            "message": data.message,
            "emotion": "crisis",
            "reply": reply,
            "timestamp": datetime.utcnow(),
            "crisis": True
        })

        return {
            "emotion": "crisis",
            "reply": reply
        }


    emotion = detect_emotion(data.message)
    text_emotion = detect_emotion(data.message)
    
    context = get_recent_conversation(user_id, limit=5)
    recent_face_emotion = get_recent_face_emotion(user_id)

    final_emotion = fuse_emotions(
    text_emotion=text_emotion,
    face_emotion=recent_face_emotion
    )



    reply = generate_supportive_reply(
    message=data.message,
    emotion=final_emotion,
    context=context
    )

    chat_collection.insert_one({
        "user_id": user_id,
        "message": data.message,
        "emotion": emotion,
        "reply": reply,
        "timestamp": datetime.utcnow(),
        "crisis": False
    })

    chat_collection.insert_one({
    "user_id": user_id,
    "message": data.message,
    "text_emotion": text_emotion,
    "face_emotion": recent_face_emotion,
    "final_emotion": final_emotion,
    "reply": reply,
    "timestamp": datetime.utcnow()
    })


    return {
        "emotion": final_emotion,
        "reply": reply
    }



@router.get("/history")
def get_chat_history(
    user_email: str = Depends(get_current_user)
):
    chats = chat_collection.find(
        {"user_id": user_email}
    ).sort("timestamp", 1)

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
        "user_id": user_email,
        "history": history
    }



@router.get("/weekly-summary")
def weekly_sentiment_summary(
    user_email: str = Depends(get_current_user)
):
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    chats = chat_collection.find({
        "user_id": user_email,
        "timestamp": {"$gte": one_week_ago}
    })

    emotions = [chat["emotion"] for chat in chats if chat["emotion"] != "crisis"]

    if not emotions:
        return {
            "user_id": user_email,
            "summary": {},
            "message": "No data available for the last 7 days"
        }

    emotion_counts = Counter(emotions)
    total = sum(emotion_counts.values())

    summary = {
        emotion: round((count / total) * 100, 2)
        for emotion, count in emotion_counts.items()
    }

    dominant_emotion = max(emotion_counts, key=emotion_counts.get)

    insight_map = {
        "happy": "You've been feeling positive overall this week 😊",
        "sad": "It seems like this week was emotionally heavy 💙",
        "fear": "You've experienced anxiety or stress this week 🌱",
        "angry": "There were moments of frustration this week 😤",
        "neutral": "Your emotions were fairly balanced this week ⚖️"
    }

    return {
        "user_id": user_email,
        "summary": summary,
        "dominant_emotion": dominant_emotion,
        "insight": insight_map.get(dominant_emotion, "Thank you for sharing your feelings.")
    }
