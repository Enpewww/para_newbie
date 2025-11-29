from fastapi import FastAPI, Request
import os
import pandas as pd
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ArthiUsaha Backend")

DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Welcome to ArthiUsaha Backend"}

@app.post("/webhook")
async def waha_webhook(request: Request):
    """
    Endpoint to receive messages from WAHA (WhatsApp).
    """
    data = await request.json()
    print("Received Webhook:", data)
    # Logic to process message, call Gemini, update Tier, etc.
    return {"status": "received"}

@app.on_event("startup")
def startup_event():
    """
    Initialize DB and load initial data if needed.
    """
    print("Starting ArthiUsaha Backend...")
    # TODO: Add logic to load CSVs from /app/data into Postgres

# --- User Onboarding API ---

from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from datetime import datetime

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    phone: str
    customerEmail: Optional[str] = None
    location: Optional[str] = None
    storeName: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# Create engine
engine = create_engine(DATABASE_URL)

@app.post("/api/users")
def create_user(user: UserCreate):
    """Create a new user or return existing user."""
    try:
        with engine.connect() as conn:
            # Check if user exists
            result = conn.execute(
                text("SELECT * FROM users WHERE phone = :phone"),
                {"phone": user.phone}
            ).fetchone()
            
            if result:
                # Convert row to dict
                user_dict = result._mapping
                # Handle datetime serialization if needed (FastAPI handles it usually, but let's be safe)
                return {
                    "message": "user_exists",
                    "data": user_dict
                }

            # Insert new user
            result = conn.execute(
                text("""
                    INSERT INTO users (firstName, lastName, phone, customerEmail, location, storeName, latitude, longitude)
                    VALUES (:firstName, :lastName, :phone, :customerEmail, :location, :storeName, :latitude, :longitude)
                    RETURNING id
                """),
                user.dict()
            )
            user_id = result.fetchone()[0]
            conn.commit()
            
            return {
                "message": "success",
                "data": user.dict(),
                "id": user_id
            }
            
    except Exception as e:
        print(f"Error creating user: {e}")
        return {"error": str(e)}, 500

@app.get("/api/users/check/{phone}")
def check_user(phone: str):
    """Check if a phone number already exists."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE phone = :phone"),
                {"phone": phone}
            ).fetchone()
            
            if result:
                return {
                    "exists": True,
                    "data": result._mapping
                }
            
            return {"exists": False}
            
    except Exception as e:
        print(f"Error checking user: {e}")
        return {"error": str(e)}, 500

