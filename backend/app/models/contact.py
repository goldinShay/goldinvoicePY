from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import ContactType, Language

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    address = Column(String)
    company_name = Column(String)

    contact_type = Column(Enum(ContactType))
    preferred_language = Column(Enum(Language))

    notes = Column(String)

    invoices = relationship("Invoice", back_populates="contact")
