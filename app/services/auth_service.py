from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.crud import user as crud_user
from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token
from app.logger import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)

def register_user(db: Session, user: UserCreate):
    logger.info(f"Register attempt for email: {user.email}")
    try:
        existing_user = crud_user.get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = crud_user.create_user(db, user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"New user registered: {new_user.email} with role: {new_user.role}")
        return new_user
    except Exception as e:
        db.rollback()
        raise e

def login_user(db: Session, user: UserLogin):
    logger.info(f"Login attempt for email: {user.email}")
    db_user = crud_user.get_user_by_email(db, user.email)
    
    # Standardize error message to prevent user enumeration
    error_detail = "Invalid email or password"
    
    if not db_user:
        logger.warning(f"Login failed - user not found: {user.email}")
        raise HTTPException(status_code=401, detail=error_detail)
    
    if not verify_password(user.password, db_user.password):
        logger.warning(f"Login failed - incorrect password for: {user.email}")
        raise HTTPException(status_code=401, detail=error_detail)
    
    token = create_access_token(data={"sub": db_user.email, "role": db_user.role})
    logger.info(f"Login successful for: {user.email}")
    return {"access_token": token, "token_type": "bearer"}