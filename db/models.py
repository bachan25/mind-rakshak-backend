from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from db.database import Base
from datetime import datetime



class TimeTableEntry(Base):
    __tablename__ = "timetable_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, nullable=False)  # e.g., "Monday"
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, default=datetime.now)
    subject = Column(String, nullable=False)
    teacher = Column(String, nullable=True)
    user_id = Column(String, nullable=False)  # Assuming user_id is a string (like email or UUID)
    description = Column(String, nullable=True)



from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TimeTableEntryBase(BaseModel):
    day_of_week: str
    start_time: datetime
    end_time: datetime
    subject: str
    teacher: Optional[str] = None
    user_id: str
    description: Optional[str] = None

class TimeTableEntryCreate(TimeTableEntryBase):
    pass

class TimeTableEntryRead(TimeTableEntryBase):
    id: int

    class Config:
        from_attributes = True   # ✅ allow ORM → Pydantic conversion



class WellnessBreakExtraInfo(Base):
    __tablename__ = "wellness_break_extra_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False)  # Assuming user_id is a string (like email or UUID)
    preferred_break_duration = Column(Integer, default=10)  # in minutes
    focus_session_length = Column(Integer, default=50)  # in minutes
    relaxation_reminder_frequency = Column(Integer, default=120)  # in minutes
    preferred_notification_method = Column(String, default="email")  # e.g., "email", "sms", "call"
    additional_notes = Column(String, nullable=True)  # Any other preferences or notes
    hobbies = Column(String, nullable=True)  # User hobbies or interests

class WellnessBreakExtraInfoBase(BaseModel):
    user_id: str
    preferred_break_duration: Optional[int] = 10  # in minutes
    focus_session_length: Optional[int] = 50  # in minutes
    relaxation_reminder_frequency: Optional[int] = 120  # in minutes
    preferred_notification_method: Optional[str] = "email"  # e.g., "email", "sms", "call"
    additional_notes: Optional[str] = None  # Any other preferences or notes
    hobbies: Optional[str] = None  # User hobbies or interests

class WellnessBreakExtraInfoCreate(WellnessBreakExtraInfoBase):
    pass
class WellnessBreakExtraInfoRead(WellnessBreakExtraInfoBase):
    id: int

    class Config:
        from_attributes = True  


