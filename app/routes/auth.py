from fastapi import APIRouter, Depends, Request, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services import auth_service
from app.utils.rate_limit import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user, background_tasks)

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user)

@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("5/minute")
def refresh(request: Request, refresh_token: str = Form(...), db: Session = Depends(get_db)):
    return auth_service.refresh_token(db, refresh_token)

@router.get("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    return auth_service.verify_email(db, token)