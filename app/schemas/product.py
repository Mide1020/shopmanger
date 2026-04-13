from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None
    image_url: Optional[str] = None
    low_stock_threshold: int = 5

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than zero")
        return v

    @field_validator("stock")
    @classmethod
    def stock_must_not_be_negative(cls, v):
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    low_stock_threshold: Optional[int] = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than zero")
        return v

    @field_validator("stock")
    @classmethod
    def stock_must_not_be_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Stock cannot be negative")
        return v


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: Optional[str]
    image_url: Optional[str]
    is_active: bool
    low_stock_threshold: int


class PaginatedProductResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: List[ProductResponse]