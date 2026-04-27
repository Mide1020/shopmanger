from sqlalchemy.orm import Session
from app.crud import invoice as crud_invoice
from app.crud import order as crud_order
from app.logger import get_logger
from fastapi import HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import tempfile

logger = get_logger(__name__)

def create_invoice(db: Session, order_id: int):
    order = crud_order.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    
    existing = crud_invoice.get_invoice_by_order_id(db, order_id)
    if existing:
        return existing

    logger.info(f"Creating invoice for order id: {order_id}")
    invoice = crud_invoice.create_invoice(
        db,
        order_id=order_id,
        amount=order.total,
        payment_status=order.payment_status
    )
    db.commit()
    db.refresh(invoice)
    logger.info(f"Invoice created: {invoice.invoice_number}")
    return invoice

def get_all_invoices(db: Session):
    return crud_invoice.get_all_invoices(db)

def get_invoice(db: Session, invoice_id: int):
    invoice = crud_invoice.get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

def get_invoice_by_order(db: Session, order_id: int):
    invoice = crud_invoice.get_invoice_by_order_id(db, order_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

def generate_pdf(db: Session, invoice_id: int):
    invoice = get_invoice(db, invoice_id)
    order = crud_order.get_order_by_id(db, invoice.order_id)

    
    filename = f"invoice_{invoice.invoice_number}.pdf"
    filepath = os.path.join(tempfile.gettempdir(), filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "ShopManager")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "Your one stop shop")

    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 120, f"INVOICE: {invoice.invoice_number}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 145, f"Date: {invoice.created_at.strftime('%Y-%m-%d')}")
    c.drawString(50, height - 165, f"Payment Status: {invoice.payment_status.upper()}")
    c.drawString(50, height - 185, f"Order ID: #{order.id}")

    
    c.line(50, height - 200, width - 50, height - 200)

    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 225, "Product")
    c.drawString(300, height - 225, "Quantity")
    c.drawString(400, height - 225, "Price")
    c.drawString(500, height - 225, "Subtotal")

    c.line(50, height - 235, width - 50, height - 235)

    y = height - 255
    c.setFont("Helvetica", 12)
    for item in order.items:
        c.drawString(50, y, item.product.name)
        c.drawString(300, y, str(item.quantity))
        c.drawString(400, y, f"₦{item.price:,.2f}")
        c.drawString(500, y, f"₦{item.price * item.quantity:,.2f}")
        y -= 20

    
    c.line(50, y - 10, width - 50, y - 10)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, y - 30, "TOTAL:")
    c.drawString(500, y - 30, f"₦{invoice.amount:,.2f}")

    c.save()
    logger.info(f"PDF generated for invoice: {invoice.invoice_number}")
    return filepath, filename