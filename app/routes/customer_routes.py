from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
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
import os

router = APIRouter(
    prefix="/me",
    tags=["Customer"]
)


@router.get("/profile", response_model=UserResponse)
def get_my_profile(current_user = Depends(get_current_user)):
    return current_user


@router.post("/orders", response_model=OrderResponse)
def place_order(order: OrderCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return order_service.process_order(db, order, background_tasks)


@router.get("/orders", response_model=List[OrderResponse])
def get_my_orders(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Resolve the Customer record that belongs to this user via email.
    # User.id and Customer.id are separate sequences — they must not be mixed.
    from app.crud import customer as crud_customer
    customer = crud_customer.get_customer_by_email(db, current_user.email)
    if not customer:
        return []
    return crud_order.get_orders_by_customer_id(db, customer.id)


@router.get("/orders/{order_id}/invoice", response_model=InvoiceResponse)
def get_my_invoice(order_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    from app.crud import customer as crud_customer
    customer = crud_customer.get_customer_by_email(db, current_user.email)
    order = crud_order.get_order_by_id(db, order_id)
    if not order or not customer or order.customer_id != customer.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return invoice_service.get_invoice_by_order(db, order_id)


@router.get("/orders/{order_id}/invoice/download")
def download_my_invoice(
    order_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    from app.crud import customer as crud_customer
    customer = crud_customer.get_customer_by_email(db, current_user.email)
    order = crud_order.get_order_by_id(db, order_id)
    if not order or not customer or order.customer_id != customer.id:
        raise HTTPException(status_code=404, detail="Order not found")

    invoice = invoice_service.get_invoice_by_order(db, order_id)
    filepath, filename = invoice_service.generate_pdf(db, invoice.id)

    # Schedule temp file deletion after the response is sent
    background_tasks.add_task(os.remove, filepath)
    return FileResponse(filepath, media_type="application/pdf", filename=filename)