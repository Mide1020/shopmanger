from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.utils.dependencies import admin_only
from app.services import order_service
from typing import List

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return order_service.process_order(db, order)

@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return order_service.get_all_orders(db)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return order_service.get_order(db, order_id)

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, updated: OrderUpdate, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return order_service.update_order(db, order_id, updated)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    order_service.delete_order(db, order_id)
    return {"message": "Order deleted successfully"}