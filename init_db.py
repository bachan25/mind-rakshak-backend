from db.database import engine, Base
from db.models import TimeTableEntry, WellnessBreakExtraInfo

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done ✅")
