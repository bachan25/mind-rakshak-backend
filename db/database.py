from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB path
SQLALCHEMY_DATABASE_URL = "sqlite:///./mindrakshak.db"

# Create engine (check_same_thread=False is needed for SQLite in multithreading)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class
Base = declarative_base()


# Dependency: create and close DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
