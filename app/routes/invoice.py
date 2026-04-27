from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.invoice import InvoiceResponse
from app.utils.dependencies import admin_only, get_current_user
from app.services import invoice_service
from typing import List
import os

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/{order_id}", response_model=InvoiceResponse)
def create_invoice(order_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return invoice_service.create_invoice(db, order_id)


@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return invoice_service.get_all_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db), current_user = Depends(admin_only)):
    return invoice_service.get_invoice(db, invoice_id)


@router.get("/{invoice_id}/download")
def download_invoice(
    invoice_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(admin_only),
):
    filepath, filename = invoice_service.generate_pdf(db, invoice_id)
    # Schedule temp file deletion after the response is streamed
    background_tasks.add_task(os.remove, filepath)
    return FileResponse(filepath, media_type="application/pdf", filename=filename)