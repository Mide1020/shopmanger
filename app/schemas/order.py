from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_at_least_one(cls, v):
        if v < 1:
            raise ValueError("Quantity must be at least 1")
        return v


class OrderCreate(BaseModel):
    customer_id: Optional[int] = None
    items: List[OrderItemCreate]
    payment_status: Optional[str] = "pending"

    @field_validator("items")
    @classmethod
    def items_must_have_unique_products(cls, v):
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate product_ids in order items are not allowed")
        return v

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    price: float

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: Optional[int]
    total: float
    payment_status: str
    order_status: str
    items: List[OrderItemResponse]

class OrderUpdate(BaseModel):
    payment_status: Optional[str] = None
    order_status: Optional[str] = None