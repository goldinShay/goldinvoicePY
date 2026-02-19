from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.contact import ContactCreate, ContactUpdate, ContactRead
from app.services import contact_service
from typing import List

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.contact import ContactCreate
from app.services.contact_service import create_contact, get_all_contacts


router = APIRouter(prefix="/contacts", tags=["Contacts"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/new", response_class=HTMLResponse)
def add_contact_form(request: Request):
    return templates.TemplateResponse("add_contact.html", {"request": request})

@router.post("/new")
def add_contact(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(None),
        phone: str = Form(None),
        db: Session = Depends(get_db)
):
    contact_data = ContactCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )
    contact_service.create_contact(db, contact_data)
    return RedirectResponse(url="/contacts/", status_code=303)


@router.get("/", response_model=List[ContactRead])
def list_contacts(db: Session = Depends(get_db)):
    return contact_service.get_contacts(db)

@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = contact_service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactRead)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contact_service.create_contact(db, contact)

@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated = contact_service.update_contact(db, contact_id, contact)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = contact_service.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}