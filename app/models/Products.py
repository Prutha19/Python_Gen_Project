from sqlalchemy import Column, Integer, String, Numeric
from ..database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(50), unique=True, index=True)
    product_image = Column(String(255), nullable=True)
    product_price = Column(Numeric(10, 2))
