from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.models.enums import Currency
from app.schemas.invoice_item import InvoiceItemRead, InvoiceItemCreate

class InvoiceBase(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    description: Optional[str] = None
    currency: Optional[Currency] = Currency.EUR
    vat: Optional[float] = 21.0
    outside_eu: Optional[bool] = False
    payment_instructions: Optional[str] = None
    note: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    contact_id: int
    items: List[InvoiceItemCreate]

class InvoiceUpdate(InvoiceBase):
    items: Optional[List[InvoiceItemCreate]] = None

class InvoiceRead(InvoiceBase):
    id: int
    contact_id: int
    subtotal: float
    total: float
    items: List[InvoiceItemRead]

    class Config:
        orm_mode = True
