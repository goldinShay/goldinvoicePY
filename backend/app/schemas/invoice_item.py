from pydantic import BaseModel
from typing import Optional

class InvoiceItemBase(BaseModel):
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class InvoiceItemCreate(InvoiceItemBase):
    description: str
    quantity: int
    unit_price: float

class InvoiceItemUpdate(InvoiceItemBase):
    pass

class InvoiceItemRead(InvoiceItemBase):
    id: int
    subtotal: float

    class Config:
        orm_mode = True
