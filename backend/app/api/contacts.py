from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.schemas.contact import ContactCreate, ContactUpdate, ContactRead
from app.services import contact_service


router = APIRouter(prefix="/contacts", tags=["Contacts"])
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def contacts_page(request: Request, db: Session = Depends(get_db)):
    contacts = contact_service.get_contacts(db)
    return templates.TemplateResponse("contacts_list.html", {
        "request": request,
        "contacts": contacts
    })

@router.get("/new", response_class=HTMLResponse)
def add_contact_form(request: Request):
    return templates.TemplateResponse("add_contact.html", {"request": request})

@router.post("/new")
def add_contact(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(None),
        phone_number: str = Form(None),
        company_name: str = Form(None),   # ⭐ ADD THIS
        birth_date: str = Form(None),
        location: str = Form(None),
        notes: str = Form(None),
        db: Session = Depends(get_db)
):
    contact_data = ContactCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        company_name=company_name,       # ⭐ AND THIS
        birth_date=birth_date or None,
        location=location,
        notes=notes,
    )
    contact_service.create_contact(db, contact_data)
    return RedirectResponse(url="/contacts/", status_code=303)


@router.get("/{contact_id}/edit", response_class=HTMLResponse)
def edit_contact_form(contact_id: int, request: Request, db: Session = Depends(get_db)):
    contact = contact_service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return templates.TemplateResponse("edit_contact.html", {
        "request": request,
        "contact": contact
    })


@router.post("/{contact_id}/edit")
def edit_contact(
        contact_id: int,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(None),
        phone_number: str = Form(None),
        company_name: str = Form(None),   # ⭐ ADD THIS
        birth_date: str = Form(None),
        location: str = Form(None),
        notes: str = Form(None),
        db: Session = Depends(get_db)
):
    update_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "company_name": company_name,     # ⭐ AND THIS
        "birth_date": birth_date or None,
        "location": location,
        "notes": notes,
    }

    contact_service.update_contact(db, contact_id, update_data)
    return RedirectResponse(url="/contacts/", status_code=303)


    contact_service.update_contact(db, contact_id, update_data)
    return RedirectResponse(url="/contacts/", status_code=303)


@router.get("/{contact_id}/delete")
def delete_contact_ui(contact_id: int, db: Session = Depends(get_db)):
    contact_service.delete_contact(db, contact_id)
    return RedirectResponse(url="/contacts/", status_code=303)


@router.get("/api", response_model=List[ContactRead])
def list_contacts_api(db: Session = Depends(get_db)):
    return contact_service.get_contacts(db)


@router.get("/api/{contact_id}", response_model=ContactRead)
def get_contact_api(contact_id: int, db: Session = Depends(get_db)):
    contact = contact_service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/api", response_model=ContactRead)
def create_contact_api(contact: ContactCreate, db: Session = Depends(get_db)):
    return contact_service.create_contact(db, contact)


@router.put("/api/{contact_id}", response_model=ContactRead)
def update_contact_api(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    updated = contact_service.update_contact(db, contact_id, contact)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated


@router.delete("/api/{contact_id}")
def delete_contact_api(contact_id: int, db: Session = Depends(get_db)):
    deleted = contact_service.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}
