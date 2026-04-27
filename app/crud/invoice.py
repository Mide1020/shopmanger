from sqlalchemy.orm import Session
from app.models.invoice import Invoice
import uuid

def create_invoice(db: Session, order_id: int, amount: float, payment_status: str):
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
    new_invoice = Invoice(
        order_id=order_id,
        invoice_number=invoice_number,
        amount=amount,
        payment_status=payment_status
    )
    db.add(new_invoice)
    db.flush()  # let the service layer own the commit
    return new_invoice

def get_invoice_by_id(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_invoice_by_order_id(db: Session, order_id: int):
    return db.query(Invoice).filter(Invoice.order_id == order_id).first()

def get_all_invoices(db: Session):
    return db.query(Invoice).all()

def update_invoice_status(db: Session, invoice_id: int, payment_status: str):
    invoice = get_invoice_by_id(db, invoice_id)
    if invoice:
        invoice.payment_status = payment_status
        db.flush()
    return invoice