from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

def create_customer(db: Session, customer: CustomerCreate):
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)
    db.flush()
    return new_customer

def get_all_customers(db: Session, search: str = None):
    query = db.query(Customer)
    if search:
        query = query.filter(
            Customer.name.ilike(f"%{search}%") |
            Customer.email.ilike(f"%{search}%") |
            Customer.phone.ilike(f"%{search}%")
        )
    return query.all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()

def update_customer(db: Session, customer_id: int, updated: CustomerUpdate):
    customer = get_customer_by_id(db, customer_id)
    if customer:
        for key, value in updated.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)
        db.flush()
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if customer:
        db.delete(customer)
        db.flush()
    return customer