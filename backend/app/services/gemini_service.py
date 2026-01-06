import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_supportive_reply(message: str, emotion: str) -> str:
    prompt = f"""
You are a supportive, empathetic mental health companion.
You are NOT a therapist or doctor.
Do NOT give medical advice.
Do NOT encourage dependency.

User emotion: {emotion}
User message: "{message}"

Respond kindly, briefly, and supportively.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "I'm here with you. Please tell me more about how you're feeling."


def generate_supportive_reply(
    message: str,
    emotion: str,
    context: str = ""
) -> str:
    prompt = f"""
You are a supportive, empathetic mental health companion.
You are NOT a therapist or doctor.
Do NOT give medical advice.
Do NOT encourage dependency.

Conversation so far:
{context}

User emotion: {emotion}
User message: "{message}"

Respond kindly, briefly, and supportively.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "I'm here with you. Please tell me more about how you're feeling."
