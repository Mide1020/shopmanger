from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional

class CustomerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[str] = Field(None, max_length=200)

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[str] = Field(None, max_length=200)


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    notes: Optional[str]
    tags: Optional[str]

class PaginatedCustomerResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: List[CustomerResponse]