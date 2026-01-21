import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

def generate_supportive_reply(
    message: str,
    emotion: str,
    context: str = ""
) -> str:
    """Generate a supportive reply using Gemini API with conversation context."""
    
    if not model:
        return "I'm here with you. Please tell me more about how you're feeling."
    
    prompt = f"""You are a supportive, empathetic mental health companion.
You are NOT a therapist or doctor.
Do NOT give medical advice.
Do NOT encourage dependency.
Keep responses brief (2-3 sentences).

User detected emotion: {emotion}

{f"Previous conversation context: {context}" if context else ""}

User message: "{message}"

Respond kindly, empathetically, and supportively to help the user feel heard and understood."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm here with you. Please tell me more about how you're feeling."
