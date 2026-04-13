from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.dependencies import admin_only
from app.services import product_service

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("/low-stock")
def get_low_stock(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return product_service.get_low_stock(db)

@router.put("/update-stock/{product_id}")
def update_stock(product_id: int, quantity: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    product = product_service.update_stock(db, product_id, quantity)
    return {
        "message": "Stock updated successfully",
        "product": product.name,
        "new_stock": product.stock
    }