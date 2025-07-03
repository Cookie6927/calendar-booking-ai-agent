# backend/calendar_utils.py

import os
from datetime import datetime, timedelta, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def book_meeting_on_calendar(query: str) -> str:
    # Step 1: Parse fixed time from query (replace with NLP later)
    start_time = datetime.now(timezone.utc) + timedelta(days=1, hours=3)
    end_time = start_time + timedelta(hours=1)
    # Step 2: Authenticate with service account
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_CREDENTIALS_PATH"),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    service = build("calendar", "v3", credentials=creds)

    # Step 3: Create event
   
    event = {
    "summary": "Meeting via AI Agent",
    "description": "Booked using Gemini and LangChain",
    "start": {
        "dateTime": start_time.isoformat(),
        "timeZone": "Asia/Kolkata"
    },
    "end": {
        "dateTime": end_time.isoformat(),
        "timeZone": "Asia/Kolkata"
    }
}

    event = service.events().insert(calendarId=os.getenv("CALENDAR_ID"), body=event).execute()

    return f"📅 Meeting booked on Google Calendar: {event.get('htmlLink')}"
