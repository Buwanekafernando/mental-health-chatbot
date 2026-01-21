from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from collections import Counter, defaultdict

from app.database import chat_collection
from app.services.jwt_dependency import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/multimodal-trends")
def multimodal_emotion_trends(
    weeks: int = 6,
    user_email: str = Depends(get_current_user)
):
    start_date = datetime.utcnow() - timedelta(weeks=weeks)

    chats = chat_collection.find({
        "user_id": user_email,
        "timestamp": {"$gte": start_date}
    })

    weekly = defaultdict(lambda: {
        "text": Counter(),
        "face": Counter(),
        "final": Counter()
    })

    for chat in chats:
        week = chat["timestamp"].strftime("%Y-W%U")

        # Use final_emotion if available, otherwise fall back to emotion
        final_emotion = chat.get("final_emotion") or chat.get("emotion")
        
        weekly[week]["text"][chat.get("text_emotion")] += 1
        if chat.get("face_emotion"):
            weekly[week]["face"][chat["face_emotion"]] += 1
        if final_emotion:
            weekly[week]["final"][final_emotion] += 1

    return {
        "weeks": weekly
    }

@router.get("/emotion-agreement")
def emotion_agreement(user_email: str = Depends(get_current_user)):
    chats = chat_collection.find({"user_id": user_email})

    total = 0
    agree = 0

    for chat in chats:
        if chat.get("face_emotion"):
            total += 1
            if chat["text_emotion"] == chat["face_emotion"]:
                agree += 1

    agreement_rate = round((agree / total) * 100, 2) if total else 0

    return {
        "total_samples": total,
        "agreement_rate": agreement_rate,
        "conflict_rate": round(100 - agreement_rate, 2)
    }
