from sqlalchemy.orm import Session
from contextlib import contextmanager

from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

