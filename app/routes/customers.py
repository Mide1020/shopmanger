from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, PaginatedCustomerResponse
from app.utils.dependencies import admin_only
from app.services import customer_service
from typing import List, Optional

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return customer_service.create_customer(db, customer)

@router.get("/", response_model=PaginatedCustomerResponse)
def get_customers(
    search: Optional[str] = Query(None), 
    page: int = Query(1, ge=1), 
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db), 
    current_user = Depends(admin_only)
):
    return customer_service.get_all_customers(db, search, page, limit)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return customer_service.get_customer(db, customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, updated: CustomerUpdate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return customer_service.update_customer(db, customer_id, updated)

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    customer_service.delete_customer(db, customer_id)
    return {"message": "Customer deleted successfully"}