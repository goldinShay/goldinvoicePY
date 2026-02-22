from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.enums import ContactType, Language  # if still used


class ContactBase(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    company_name: Optional[str] = None
    birth_date: Optional[date] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    first_name: str
    last_name: str
    # email, phone_number, etc. remain optional
    # birth_date, location, notes optional


class ContactUpdate(ContactBase):
    pass


class ContactRead(ContactBase):
    id: int
    uid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode
