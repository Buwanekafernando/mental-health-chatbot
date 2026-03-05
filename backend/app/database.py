import os 
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")


client = MongoClient(MONGODB_URL)
db = client[DB_NAME]

chat_collection = db["chat_history"]
face_emotion_collection = db["face_emotions"]
