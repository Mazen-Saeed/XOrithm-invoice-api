from pydantic import BaseModel, ConfigDict
from datetime import datetime

class InvoiceBase(BaseModel):
    # Shared properties for creating or reading an invoice.

    amount_original: float
    currency: str
    account_id: int

class InvoiceCreate(InvoiceBase):
    # Inherits base fields for POST /invoices.

    pass

class InvoiceRead(InvoiceBase):
    # What we return from the API for invoices:
    id: int
    amount_default: float
    created_at: datetime

    # allow reading attributes off ORM
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={float: lambda v: round(v, 2)}
    )
