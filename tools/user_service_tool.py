from langchain.tools import tool

from db.database import get_db
from db.models import WellnessBreakExtraInfo

# user additional info for wellness breaks

@tool
def get_user_additional_info(user_id: str) -> str:
    """
    Fetch additional information of the user for wellness breaks.
    """
    db = next(get_db())
    info = db.query(WellnessBreakExtraInfo).filter(WellnessBreakExtraInfo.user_id == user_id).first()

    if not info:
        return "No wellness break info found."
    
    # user friendly format
    additional_info = f"Wellness Break Info for user_id {user_id}:\n"
    additional_info += f"- preferred_break_duration: {info.preferred_break_duration} minutes\n"
    additional_info += f"- focus_session_length: {info.focus_session_length or 'N/A'} minutes\n"
    additional_info += f"- relaxation_reminder_frequency: {info.relaxation_reminder_frequency or 'N/A'} minutes\n"
    additional_info += f"- preferred_notification_method: {info.preferred_notification_method or 'N/A'}\n"
   
    return additional_info