from sqlalchemy import Column, Integer, String
from app.db.database import Base
from app.core.config import get_settings

settings = get_settings()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)