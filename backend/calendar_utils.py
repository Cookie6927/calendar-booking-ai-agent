def book_meeting_on_calendar(query: str) -> str:
    from datetime import datetime, timedelta, timezone
    import os
    import dateparser
    from googleapiclient.discovery import build
    from google.oauth2 import service_account

    # Try to parse user query
    parsed_dt = dateparser.parse(
        query,
        settings={'TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True}
    )

    # Fallback: if parsing fails, default to tomorrow 3PM IST
    if not parsed_dt:
        ist = timezone(timedelta(hours=5, minutes=30))
        parsed_dt = datetime.now(ist).replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=1)

    start_time = parsed_dt
    end_time = start_time + timedelta(hours=1)

    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_CREDENTIALS_PATH"),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": "Meeting via AI Agent",
        "description": f"Auto-booked via LangChain Gemini | Original Query: {query}",
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
