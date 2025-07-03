# backend/main.py
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from lang_agent import run_agent
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Load credentials from environment variable
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
if not GOOGLE_CREDENTIALS_JSON:
    raise ValueError("❌ GOOGLE_CREDENTIALS_JSON not set")

try:
    creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
    credentials = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
except Exception as e:
    raise ValueError(f"❌ Error loading credentials: {e}")

# Load calendar ID
CALENDAR_ID = os.getenv("CALENDAR_ID")
if not CALENDAR_ID:
    raise ValueError("❌ CALENDAR_ID not set")

# Build Google Calendar API client
service = build("calendar", "v3", credentials=credentials)

# FastAPI app instance
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming chat
class ChatInput(BaseModel):
    message: str

@app.get("/check_availability")
def check_availability():
    try:
        now = datetime.now(timezone.utc).isoformat()
        later = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()

        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            timeMax=later,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking availability: {e}")

@app.post("/chat")
def chat_with_user(input: ChatInput):
    try:
        print("🔹 Incoming message:", input.message)
        response = run_agent(input.message)  # Must return dict or JSON-serializable response
        print("✅ Agent response:", response)
        return response
    except Exception as e:
        print("❌ ERROR in run_agent:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book_appointment")
def book_appointment():
    try:
        start_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        end_time = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()

        event = {
            'summary': 'Test Booking',
            'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
        }

        created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return {
            "message": "✅ Booking successful!",
            "eventLink": created_event.get("htmlLink")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error booking appointment: {e}")
