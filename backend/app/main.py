from fastapi import FastAPI
from app.routers import chat

app = FastAPI(
    title="AI Mental Health Chat Companion",
    description="Non-clinical emotional support chatbot",
    version="1.0"
)

app.include_router(chat.router, prefix="/api/chat")

@app.get("/")
def root():
    return {"status": "Backend is running"}