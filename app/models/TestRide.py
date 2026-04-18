from sqlalchemy import Column, DateTime, Integer, String, Numeric
from ..database import Base


class TestRide(Base):
    __tablename__ = "test_rides"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    bike_name = Column(String(255), nullable=True)
    time = Column(DateTime, nullable=True)
    location = Column(String(255), nullable=True)
