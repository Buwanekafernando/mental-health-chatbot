def fuse_emotions(text_emotion: str, face_emotion: str | None):
    """
    Combines text and face emotion into a final emotion
    """

    # If no face emotion detected recently
    if not face_emotion:
        return text_emotion

    # If both match → strong confidence
    if text_emotion == face_emotion:
        return text_emotion

    # Conflict resolution rules
    priority_map = {
        "crisis": 10,
        "sad": 8,
        "fear": 7,
        "angry": 6,
        "neutral": 5,
        "happy": 4
    }

    if priority_map.get(text_emotion, 0) >= priority_map.get(face_emotion, 0):
        return text_emotion
    else:
        return face_emotion
