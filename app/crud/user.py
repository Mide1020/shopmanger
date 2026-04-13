from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed,
        role=user.role
    )
    db.add(new_user)
    db.flush()
    return new_user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.flush()
    return user