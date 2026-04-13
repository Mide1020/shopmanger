from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.user import UserResponse
from app.schemas.invoice import InvoiceResponse
from app.utils.dependencies import get_current_user
from app.services import order_service, invoice_service
from app.crud import order as crud_order
from typing import List

router = APIRouter(
    prefix="/me",
    tags=["Customer"]
)


@router.get("/profile", response_model=UserResponse)
def get_my_profile(current_user = Depends(get_current_user)):
    return current_user


@router.post("/orders", response_model=OrderResponse)
def place_order(order: OrderCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return order_service.process_order(db, order)


@router.get("/orders", response_model=List[OrderResponse])
def get_my_orders(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    orders = crud_order.get_all_orders(db)
    return [order for order in orders if order.customer_id == current_user.id]


@router.get("/orders/{order_id}/invoice", response_model=InvoiceResponse)
def get_my_invoice(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    orders = crud_order.get_all_orders(db)
    order = next((o for o in orders if o.id == order_id and o.customer_id == current_user.id), None)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    return invoice_service.get_invoice_by_order(db, order_id)


@router.get("/orders/{order_id}/invoice/download")
def download_my_invoice(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
   
    orders = crud_order.get_all_orders(db)
    order = next((o for o in orders if o.id == order_id and o.customer_id == current_user.id), None)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    invoice = invoice_service.get_invoice_by_order(db, order_id)
    filepath, filename = invoice_service.generate_pdf(db, invoice.id)
    return FileResponse(filepath, media_type="application/pdf", filename=filename)