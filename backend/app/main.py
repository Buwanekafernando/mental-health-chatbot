from fastapi import FastAPI
from app.routers import chat
from app.routers import auth
from app.routers import face_emotion

app = FastAPI(
    title="AI Mental Health Chat Companion",
    description="Non-clinical emotional support chatbot",
    version="1.0"
)

app.include_router(chat.router, prefix="/api/chat")
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(face_emotion.router)

@app.get("/")
def root():
    return {"status": "Backend is running"}