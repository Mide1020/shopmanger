from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.crud import customer as crud_customer
from app.logger import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)

def create_customer(db: Session, customer: CustomerCreate):
    logger.info(f"Creating customer: {customer.name}")
    try:
        if customer.email is not None:
            existing = crud_customer.get_customer_by_email(db, customer.email)
            if existing:
                logger.warning(f"Customer already exists with email: {customer.email}")
                raise HTTPException(status_code=400, detail="Customer with this email already exists")
        
        new_customer = crud_customer.create_customer(db, customer)
        db.commit()
        db.refresh(new_customer)
        logger.info(f"Customer created successfully: {new_customer.name}")
        return new_customer
    except Exception as e:
        db.rollback()
        raise e

def get_all_customers(db: Session, search: str = None, page: int = 1, limit: int = 10):
    logger.info(f"Fetching all customers, search: {search}, page: {page}")
    return crud_customer.get_all_customers(db, search, page, limit)

def get_customer(db: Session, customer_id: int):
    customer = crud_customer.get_customer_by_id(db, customer_id)
    if not customer:
        logger.warning(f"Customer not found with id: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

def update_customer(db: Session, customer_id: int, updated: CustomerUpdate):
    try:
        customer = crud_customer.update_customer(db, customer_id, updated)
        if not customer:
            logger.warning(f"Customer not found with id: {customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")
        db.commit()
        db.refresh(customer)
        return customer
    except Exception as e:
        db.rollback()
        raise e

def delete_customer(db: Session, customer_id: int):
    try:
        customer = crud_customer.delete_customer(db, customer_id)
        if not customer:
            logger.warning(f"Customer not found with id: {customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")
        db.commit()
        return customer
    except Exception as e:
        db.rollback()
        raise e