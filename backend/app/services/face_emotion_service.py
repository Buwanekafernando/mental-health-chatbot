from datetime import datetime, timedelta
from app.database import face_emotion_collection

def get_recent_face_emotion(user_id: str, minutes: int = 2):
    since_time = datetime.utcnow() - timedelta(minutes=minutes)

    record = face_emotion_collection.find_one(
        {
            "user_id": user_id,
            "timestamp": {"$gte": since_time}
        },
        sort=[("timestamp", -1)]
    )

    if record:
        return record["emotion"]

    return None
