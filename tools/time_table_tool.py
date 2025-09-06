from langchain.tools import tool
from sqlalchemy import func

from db.database import get_db
from db.models import TimeTableEntry
from routes.timetable_controller import read_entries_for_user_today


@tool
def get_today_study_schedule(user_id: str) -> str:
    """
    Fetch today's study schedule for the user.
    """
    from datetime import date
    today = date.today()

    db = next(get_db())
   
    entries = db.query(TimeTableEntry).filter(
        TimeTableEntry.user_id == user_id,
        func.date(TimeTableEntry.start_time) == today
    ).all()

    if not entries:
        return "No study schedule found for today."
    
    # return list of entries in a user-friendly format
    schedule = "Today's Study Schedule:\n"  
    for entry in entries:
        schedule += f"- id {entry.id} subject {entry.subject} with teacher {entry.teacher or 'N/A'} from {entry.start_time.strftime('%H:%M')} to {entry.end_time.strftime('%H:%M')} description {entry.description or 'N/A'}\n"

    return schedule
