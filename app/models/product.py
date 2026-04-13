from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, nullable=True, index=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    low_stock_threshold = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())