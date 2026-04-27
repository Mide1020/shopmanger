from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password
from datetime import datetime, timezone

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()

def get_user_by_verification_token(db: Session, token: str):
    return db.query(User).filter(User.verification_token == token, User.deleted_at.is_(None)).first()

def get_all_users(db: Session, page: int = 1, limit: int = 10):
    query = db.query(User).filter(User.deleted_at.is_(None))
    total = query.count()
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": -(-total // limit) if limit > 0 else 0, # ceiling division
        "items": items,
    }

def create_user(db: Session, user: UserCreate, verification_token: str = None):
    hashed = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed,
        role=user.role if hasattr(user, "role") and user.role else "customer",
        is_verified=False,
        verification_token=verification_token
    )
    db.add(new_user)
    db.flush()
    return new_user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        user.deleted_at = datetime.now(timezone.utc)
        user.is_active = False # Additional safety disable
        db.flush()
    return user