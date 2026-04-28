from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Test User",
                "email": "test@example.com",
                "password": "testpassword123",
                "role": "customer"
            }
        }
    )

    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: Optional[str] = "customer"  # Optional role for demo/portfolio purposes

class UserLogin(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "password": "testpassword123"
            }
        }
    )

    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str