from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from src.database import Base


class TestModel(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
