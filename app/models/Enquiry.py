from sqlalchemy import Column ,Integer,String
from ..database import Base

class Enquire(Base):
    __tablename__ ="enquires"
    id = Column(Integer,primary_key=True,index = True)
    user_name = Column(String(50),index = True)
    bike_name = Column(String(100),nullable = True)
    model_name =Column(String(50),nullable=True)
    location = Column(String(50),nullable=True)
