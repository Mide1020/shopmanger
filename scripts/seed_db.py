import sys
import os

# Add the project root to sys.path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.product import Product
from app.models.customer import Customer
from app.utils.hashing import hash_password
from datetime import datetime, timezone

def seed():
    print("Seeding database...")
    db = SessionLocal()
    
    try:
        # 1. Create Admin User
        admin_email = "admin@shopmanager.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin = User(
                name="System Admin",
                email=admin_email,
                password=hash_password("admin1234"),
                role="admin",
                is_verified=True
            )
            db.add(admin)
            print(f"Created Admin: {admin_email} / admin1234")

        # 2. Create some products
        products_data = [
            {"name": "Wireless Mouse", "price": 25.99, "stock": 50, "category": "Electronics", "description": "Ergonomic 2.4GHz wireless mouse"},
            {"name": "Mechanical Keyboard", "price": 89.99, "stock": 5, "category": "Electronics", "description": "RGB mechanical keyboard with blue switches"},
            {"name": "Laptop Stand", "price": 34.50, "stock": 15, "category": "Accessories", "description": "Aluminum adjustable laptop stand"},
            {"name": "USB-C Hub", "price": 45.00, "stock": 2, "category": "Accessories", "description": "7-in-1 USB-C multitasking hub"},
            {"name": "Gaming Monitor", "price": 299.99, "stock": 8, "category": "Electronics", "description": "27-inch 144Hz 1ms gaming monitor"},
        ]
        
        for p in products_data:
            existing = db.query(Product).filter(Product.name == p["name"]).first()
            if not existing:
                new_product = Product(
                    name=p["name"],
                    price=p["price"],
                    stock=p["stock"],
                    category=p["category"],
                    description=p["description"],
                    low_stock_threshold=10
                )
                db.add(new_product)
                print(f"Added product: {p['name']}")

        # 3. Create a demo customer
        customer_email = "demo.customer@test.com"
        customer = db.query(Customer).filter(Customer.email == customer_email).first()
        if not customer:
            customer = Customer(
                name="John Doe",
                email=customer_email,
                phone="08012345678",
                address="123 Portfolio Lane, Tech City",
                notes="Frequent buyer of electronics."
            )
            db.add(customer)
            print(f"Added customer: {customer_email}")

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
