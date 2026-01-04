from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.database import db
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()
users = db["users"]

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: RegisterRequest):
    if users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    users.insert_one({
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "created_at": datetime.utcnow()
    })

    return {"message": "User registered successfully"}

@router.post("/login")
def login(data: LoginRequest):
    user = users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": data.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
