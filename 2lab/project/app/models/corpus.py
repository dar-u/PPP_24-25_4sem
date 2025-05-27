from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class Corpus(Base):
    __tablename__ = "corpuses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(Text)