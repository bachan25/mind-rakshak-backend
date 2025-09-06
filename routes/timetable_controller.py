from fastapi import APIRouter, HTTPException, Depends
from requests import Session
from sqlalchemy import func
from db.models import TimeTableEntry, TimeTableEntryCreate, TimeTableEntryRead
from db.database import get_db
from datetime import date

today = date.today()

router = APIRouter()

@router.post("/add", response_model=TimeTableEntryRead,summary="Add a new timetable entry")
def create_entry(entry: TimeTableEntryCreate, db: Session = Depends(get_db)):
    db_entry = TimeTableEntry(**entry.dict())  # Convert Pydantic → SQLAlchemy
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/get/{entry_id}", response_model=TimeTableEntryRead,summary="Get a timetable entry by ID")
def read_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = db.query(TimeTableEntry).filter(TimeTableEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return db_entry

# get timetable entries for a user for today
@router.get("/user/{user_id}/today", response_model=list[TimeTableEntryRead],summary="Get today's timetable entries for a user")
def read_entries_for_user_today(user_id: str, db: Session = Depends(get_db)):
    return db.query(TimeTableEntry).filter(
        TimeTableEntry.user_id == user_id,
        func.date(TimeTableEntry.start_time) == today
    ).all()

@router.put("/update/{entry_id}", response_model=TimeTableEntryRead,summary="Update a timetable entry by ID")
def update_entry(entry_id: int, entry: TimeTableEntryCreate, db: Session = Depends(get_db)):
    db_entry = db.query(TimeTableEntry).filter(TimeTableEntry.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in entry.dict().items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry
