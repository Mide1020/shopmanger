from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None

class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    notes: Optional[str]
    tags: Optional[str]