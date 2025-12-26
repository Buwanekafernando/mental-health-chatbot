from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def detect_emotion(text: str) -> str:
    result = emotion_classifier(text)[0]
    top_emotion = max(result, key=lambda x: x['score'])
    return top_emotion['label']
    