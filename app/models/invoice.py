from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    order = relationship("Order", backref="invoice")