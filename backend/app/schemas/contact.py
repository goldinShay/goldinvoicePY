from pydantic import BaseModel
from typing import Optional
from app.models.enums import ContactType, Language

class ContactBase(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    company_name: Optional[str] = None
    contact_type: Optional[ContactType] = None
    preferred_language: Optional[Language] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    first_name: str
    last_name: str
    email: str

class ContactUpdate(ContactBase):
    pass

class ContactRead(ContactBase):
    id: int

    class Config:
        orm_mode = True
