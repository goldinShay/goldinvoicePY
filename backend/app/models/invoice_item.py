from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))

    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)

    subtotal = Column(Float)  # quantity * unit_price

    invoice = relationship("Invoice", back_populates="items")
