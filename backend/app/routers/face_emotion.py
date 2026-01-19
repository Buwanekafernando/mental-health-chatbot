from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime

from app.database import face_emotion_collection
from app.services.jwt_dependency import get_current_user

router = APIRouter(prefix="/analytics", tags=["Face Emotion"])

class FaceEmotionRequest(BaseModel):
    emotion: str


@router.post("/face-emotion")
def store_face_emotion(
    data: FaceEmotionRequest,
    user_email: str = Depends(get_current_user)
):
    face_emotion_collection.insert_one({
        "user_id": user_email,
        "emotion": data.emotion,
        "timestamp": datetime.utcnow()
    })

    return {
        "status": "saved",
        "emotion": data.emotion
    }


