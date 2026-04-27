from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.crud import user as crud_user
from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.utils.masking import mask_email
from app.logger import get_logger
from fastapi import HTTPException, BackgroundTasks
import secrets
from app.utils.email import send_email

logger = get_logger(__name__)

def register_user(db: Session, user: UserCreate, background_tasks: BackgroundTasks = None):
    masked_email = mask_email(user.email)
    logger.info(f"Register attempt for email: {masked_email}")
    try:
        existing_user = crud_user.get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"Email already registered: {masked_email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # For portfolio/demo: Auto-verify users so they can log in immediately
        new_user = crud_user.create_user(db, user, verification_token=None)
        new_user.is_verified = True
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"New user registered and auto-verified: {masked_email}")
        return new_user
    except Exception as e:
        db.rollback()
        raise e

def verify_email(db: Session, token: str):
    user = crud_user.get_user_by_verification_token(db, token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    if user.is_verified:
        return {"message": "Email already verified"}
        
    user.is_verified = True
    user.verification_token = None
    db.commit()
    logger.info(f"User email verified: {mask_email(user.email)}")
    return {"message": "Email successfully verified"}

def login_user(db: Session, user: UserLogin):
    masked_email = mask_email(user.email)
    logger.info(f"Login attempt for email: {masked_email}")
    db_user = crud_user.get_user_by_email(db, user.email)
    
    # Standardize error message to prevent user enumeration
    error_detail = "Invalid email or password"
    
    if not db_user or db_user.deleted_at is not None:
        logger.warning(f"Login failed - user not found or deleted: {masked_email}")
        raise HTTPException(status_code=401, detail=error_detail)
        
    if not db_user.is_verified:
        logger.warning(f"Login failed - email not verified: {masked_email}")
        # Use the same generic message to avoid confirming that the email is registered
        raise HTTPException(status_code=401, detail=error_detail)
    
    if not verify_password(user.password, db_user.password):
        logger.warning(f"Login failed - incorrect password for: {masked_email}")
        raise HTTPException(status_code=401, detail=error_detail)
    
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role})
    refresh_token = create_refresh_token(data={"sub": db_user.email, "role": db_user.role})
    logger.info(f"Login successful for: {masked_email}")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def refresh_token(db: Session, token: str):
    payload = verify_refresh_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    email = payload.get("sub")
    role = payload.get("role")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
        
    db_user = crud_user.get_user_by_email(db, email)
    if not db_user or db_user.deleted_at is not None:
        raise HTTPException(status_code=401, detail="User not found or inactive")
        
    new_access_token = create_access_token(data={"sub": email, "role": role})
    new_refresh_token = create_refresh_token(data={"sub": email, "role": role})
    logger.info(f"Token refreshed for: {mask_email(email)}")
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}