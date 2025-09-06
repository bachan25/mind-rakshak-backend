from fastapi import APIRouter, HTTPException, Depends
from requests import Session
from db.models import  WellnessBreakExtraInfo, WellnessBreakExtraInfoBase, WellnessBreakExtraInfoRead
from db.database import get_db

router = APIRouter()


# add wellness break extra info for user
@router.post("/wellness_break_info/add", response_model=WellnessBreakExtraInfoRead,summary="Add wellness break extra info for a user")
def create_wellness_break_info(info: WellnessBreakExtraInfoBase, db: Session = Depends(get_db)):
    db_info = WellnessBreakExtraInfo(**info.dict())  # Convert Pydantic → SQLAlchemy
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info


# get wellness break extra info for user
@router.get("/wellness_break_info/get/{user_id}", response_model=WellnessBreakExtraInfoRead,summary="Get wellness break extra info for a user")
def read_wellness_break_info(user_id: str, db: Session = Depends(get_db )):
    db_info = db.query(WellnessBreakExtraInfo).filter(WellnessBreakExtraInfo.user_id == user_id).first()
    if not db_info:
        raise HTTPException(status_code=404, detail="Info not found")
    return db_info  


# update wellness break extra info for user
@router.put("/wellness_break_info/update/{user_id}", response_model=WellnessBreakExtraInfoRead,summary="Update wellness break extra info for a user")
def update_wellness_break_info(user_id: str, info: WellnessBreakExtraInfoBase   , db: Session = Depends(get_db )):
    db_info = db.query(WellnessBreakExtraInfo).filter(WellnessBreakExtraInfo.user_id == user_id).first()
    if not db_info:
        raise HTTPException(status_code=404, detail="Info not found")
    for key, value in info.dict().items():
        setattr(db_info, key, value)
    db.commit()
    db.refresh(db_info)
    return db_info