from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

EMOTION_MAP = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "fear",
    "disgust": "angry",
    "surprise": "happy",
    "neutral": "neutral"
}

def detect_emotion(text: str) -> str:
    result = emotion_classifier(text)[0]
    top_emotion = max(result, key=lambda x: x['score'])
    label = top_emotion['label']
    return EMOTION_MAP.get(label, label)
    