import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.utils.hashing import hash_password
import argparse

def create_admin(email: str, password: str, name: str):
    db: Session = SessionLocal()
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            if existing_user.role != "admin":
                print("Updating existing user's role to admin...")
                existing_user.role = "admin"
                db.commit()
                print("Role updated successfully.")
            return

        print(f"Creating admin user: {email}")
        hashed = hash_password(password)
        new_admin = User(
            name=name,
            email=email,
            password=hashed,
            role="admin",  # Explicitly setting admin role
            is_verified=True,  # Admins are auto-verified
            verification_token=None
        )
        db.add(new_admin)
        db.commit()
        print("Admin user created successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed an admin user into the database.")
    parser.add_argument("--email", required=True, help="Admin email address")
    parser.add_argument("--password", required=True, help="Admin password")
    parser.add_argument("--name", default="Admin User", help="Admin full name")

    args = parser.parse_args()

    create_admin(args.email, args.password, args.name)
