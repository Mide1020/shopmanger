from pydantic import BaseModel, ConfigDict
from datetime import datetime

class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    invoice_number: str
    amount: float
    payment_status: str
    created_at: datetime