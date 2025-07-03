# backend/main.py

import os
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from lang_agent import run_agent
from pydantic import BaseModel


# Load environment variables
load_dotenv()
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
CALENDAR_ID = os.getenv("CALENDAR_ID")

# Google Calendar authentication using service account
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_PATH,
    scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)


#Chat input Model
class ChatInput(BaseModel):
    message: str

# FastAPI app instance
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/check_availability")
def check_availability():
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


@app.post("/chat")
def chat_with_user(input: ChatInput):
    try:
        print("🔹 Incoming message:", input.message)
        response = run_agent(input.message)  # now returns a dict
        print("✅ Agent response:", response)
        return response
    except Exception as e:
        print("❌ ERROR in agent.run:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/book_appointment")
def book_appointment():
    start_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    end_time = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()

    event = {
        'summary': 'Test Booking',
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return {"message": "Booking successful!", "eventLink": created_event.get("htmlLink")}
