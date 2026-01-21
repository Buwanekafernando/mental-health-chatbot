from fastapi import FastAPI
from app.routers import chat
from app.routers import auth
from app.routers import face_emotion
from app.routers import analytics

app = FastAPI(
    title="AI Mental Health Chat Companion",
    description="Non-clinical emotional support chatbot",
    version="1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat")
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(face_emotion.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"status": "Backend is running"}