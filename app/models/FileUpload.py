from sqlalchemy import Column, Integer, String
from ..database import Base


class FileUpload(Base):
    __tablename__ = "file_upload"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    file_location = Column(String(500), nullable=False)
    bike_name = Column(String(100), nullable=False)
