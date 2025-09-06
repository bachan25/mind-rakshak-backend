from json import tool
from service import outbound_app_service

from langchain.tools import tool


BASE_URL = "https://www.googleapis.com/calendar/v3/"


@tool
def list_calendar_events(start_date: str, end_date: str,user_id: str) -> str:
    """
    List events from the user's primary Google Calendar between start_date and end_date.
    Dates should be in ISO format: 'YYYY-MM-DD'.
    Returns a user-friendly summary of events.
    """
    from datetime import datetime, timezone, timedelta
    import requests


    # 1) Get OAuth access token
    response = outbound_app_service.fetch_outbound_token("google-calendar", user_id)
    access_token = response["token"]["accessToken"]

    # 2) Normalize to RFC3339 full-day range
    def day_start(d: str) -> str:
        return datetime.fromisoformat(d).replace(hour=0, minute=0, second=0, tzinfo=timezone.utc).isoformat()

    def day_end(d: str) -> str:
        return datetime.fromisoformat(d).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc).isoformat()

    start = day_start(start_date)
    end = day_end(end_date)

    # 3) Build query params
    params = {
        "timeMin": start,
        "timeMax": end,
        "singleEvents": True,   # expand recurring events
        "orderBy": "startTime", # chronological
        "maxResults": 2500
    }

    # 4) Call Google Calendar API directly
    events_url = f"{BASE_URL}calendars/primary/events"
    headers = {"Authorization": f"Bearer {access_token}"}

    resp = requests.get(events_url, headers=headers, params=params, timeout=20)

    try:
        data = resp.json()
    except Exception:
        return f"❌ Failed to parse response. Raw: {resp.text}"

    items = data.get("items", []) if resp.ok else []

    # 5) Format user-friendly output
    if not items:
        return f"📭 No events found between {start_date} and {end_date}."

    summary_lines = [f"📅 Events from {start_date} to {end_date}:"]
    for ev in items:
        title = ev.get("summary", "Untitled")
        start_time = ev.get("start", {}).get("dateTime", ev.get("start", {}).get("date"))
        end_time = ev.get("end", {}).get("dateTime", ev.get("end", {}).get("date"))
        summary_lines.append(f"• {title} ({start_time} → {end_time})")

    return "\n".join(summary_lines)

@tool
def create_calendar_event(
    summary: str,
    start_datetime: str,
    end_datetime: str,
    description: str = "",
    attendees: list[str] = None,
    reminders: list[dict] = None,
    create_meet: bool = False,
    user_id: str = None,
) -> str:
    """
    Create a new event in the user's primary Google Calendar.

    Args:
        summary (str): Title of the event.
        start_datetime (str): Start time in RFC3339, e.g., 'YYYY-MM-DDTHH:MM:SSZ' or with offset.
        end_datetime (str): End time in RFC3339.
        description (str): Event description (optional).
        attendees (list[str]): List of attendee emails (optional).
        reminders (list[dict]): Custom reminders (optional). 
                                Example: [{"method": "email", "minutes": 30}, {"method": "popup", "minutes": 10}]
        create_meet (bool): Whether to create a Google Meet link.

    Returns:
        str: Success or failure message.
    """
    from datetime import datetime
    import requests
    import uuid

    # 1) Get OAuth access token
    response = outbound_app_service.fetch_outbound_token("google-calendar", user_id)
    access_token = response["token"]["accessToken"]

    # 2) Normalize datetime
    def normalize(dt_str: str) -> str:
        s = dt_str.strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        return dt.isoformat()

    start = normalize(start_datetime)
    end = normalize(end_datetime)

    # 3) Build event data
    event_data = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start},
        "end": {"dateTime": end}
    }

    if attendees:
        event_data["attendees"] = [{"email": email} for email in attendees]

    if reminders:
        event_data["reminders"] = {"useDefault": False, "overrides": reminders}

    if create_meet:
        event_data["conferenceData"] = {
            "createRequest": {
                "requestId": str(uuid.uuid4()),  # unique ID required
                "conferenceSolutionKey": {"type": "hangoutsMeet"}
            }
        }

    # 4) Call Google Calendar API
    
    events_url = f"{BASE_URL}calendars/primary/events?conferenceDataVersion=1"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(events_url, headers=headers, json=event_data, timeout=20)

    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}

    # 5) Handle response
    if resp.ok and "id" in data:
        link = data.get("htmlLink", "")
        meet_link = data.get("conferenceData", {}).get("entryPoints", [{}])[0].get("uri", "") if create_meet else ""
        msg = f"✅ Event '{data.get('summary', summary)}' created successfully.\n"
        msg += f"📅 {start} → {end}\n"
        if link:
            msg += f"🔗 Event link: {link}\n"
        if meet_link:
            msg += f"🎥 Google Meet: {meet_link}\n"
        return msg.strip()
    else:
        return f"❌ Failed to create event. HTTP {resp.status_code}. Details: {data}"
