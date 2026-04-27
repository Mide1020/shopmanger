from enum import Enum
from pydantic import BaseModel
from typing import Optional, Any

class ErrorCode(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTEGRITY_ERROR = "INTEGRITY_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"
    DUPLICATE_RESOURCE = "DUPLICATE_RESOURCE"
    PAYMENT_REQUIRED = "PAYMENT_REQUIRED"

class ErrorResponse(BaseModel):
    status: str = "error"
    code: ErrorCode
    message: str
    details: Optional[Any] = None
