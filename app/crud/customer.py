from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from datetime import datetime, timezone

def create_customer(db: Session, customer: CustomerCreate):
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)
    db.flush()
    return new_customer

def get_all_customers(db: Session, search: str = None, page: int = 1, limit: int = 10):
    query = db.query(Customer).filter(Customer.deleted_at.is_(None))
    if search:
        query = query.filter(
            Customer.name.ilike(f"%{search}%") |
            Customer.email.ilike(f"%{search}%") |
            Customer.phone.ilike(f"%{search}%")
        )
    
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

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id, Customer.deleted_at.is_(None)).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email, Customer.deleted_at.is_(None)).first()

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
        customer.deleted_at = datetime.now(timezone.utc)
        
        # Cascade soft-delete to all orders associated with this customer
        from app.models.order import Order
        db.query(Order).filter(
            Order.customer_id == customer_id,
            Order.deleted_at.is_(None)
        ).update({"deleted_at": customer.deleted_at}, synchronize_session=False)
        
        db.flush()
    return customer