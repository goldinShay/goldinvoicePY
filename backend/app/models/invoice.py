from sqlalchemy import Column, Integer, Float, String, Boolean, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import Currency

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))

    invoice_number = Column(String)
    invoice_date = Column(Date)
    description = Column(String)

    currency = Column(Enum(Currency), default=Currency.EUR)

    vat = Column(Float)  # percentage
    outside_eu = Column(Boolean, default=False)

    subtotal = Column(Float)
    total = Column(Float)

    payment_instructions = Column(String)
    note = Column(String)

    contact = relationship("Contact", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete")
