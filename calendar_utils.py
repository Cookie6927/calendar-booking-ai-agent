def book_meeting_on_calendar(query: str) -> str:
    from datetime import datetime, timedelta, timezone
    import os
    import dateparser
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    import json

    # Load credentials from env var
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        raise ValueError("❌ GOOGLE_CREDENTIALS_JSON not set")

    try:
        creds_dict = json.loads(creds_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Invalid JSON in GOOGLE_CREDENTIALS_JSON: {e}")

    credentials = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    # Try to parse the query into datetime
    parsed_dt = dateparser.parse(
        query,
        settings={'TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True}
    )

    # Fallback: Tomorrow at 3PM IST
    if not parsed_dt:
        ist = timezone(timedelta(hours=5, minutes=30))
        parsed_dt = datetime.now(ist).replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=1)

    start_time = parsed_dt
    end_time = start_time + timedelta(hours=1)

    service = build("calendar", "v3", credentials=credentials)

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

    calendar_id = os.getenv("CALENDAR_ID")
    if not calendar_id:
        raise ValueError("❌ CALENDAR_ID not set")

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return f"📅 Meeting booked! [View on Calendar]({created_event.get('htmlLink')})"
