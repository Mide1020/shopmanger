from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.schemas.error import ErrorCode

def _sanitize(obj):
    """Recursively convert values to JSON-serializable types.
    Handles bytes (common in pydantic errors) and non-serializable objects like exceptions."""
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    if isinstance(obj, (dict, list)):
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items()}
        return [_sanitize(i) for i in obj]
    # If it's not a primitive JSON type, convert to string (fixes ValueError serialization crash)
    if not isinstance(obj, (str, int, float, bool, type(None))):
        return str(obj)
    return obj

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": ErrorCode.VALIDATION_ERROR,
            "message": "Validation error",
            "details": _sanitize(exc.errors())
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "code": ErrorCode.INTEGRITY_ERROR,
            "message": "Database integrity error — duplicate or invalid data",
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "code": ErrorCode.INTERNAL_SERVER_ERROR,
            "message": "Something went wrong on our end",
        }
    )