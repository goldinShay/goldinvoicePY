from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceRead
from app.services import invoice_service

router = APIRouter(prefix="/invoices", tags=["Invoices"])
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def invoices_page(request: Request, db: Session = Depends(get_db)):
    invoices = invoice_service.get_invoices(db)
    return templates.TemplateResponse("invoices_list.html", {
        "request": request,
        "invoices": invoices
    })


@router.get("/api", response_model=List[InvoiceRead])
def list_invoices(db: Session = Depends(get_db)):
    return invoice_service.get_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = invoice_service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return invoice_service.create_invoice(db, invoice)


@router.put("/{invoice_id}", response_model=InvoiceRead)
def update_invoice(invoice_id: int, invoice: InvoiceUpdate, db: Session = Depends(get_db)):
    updated = invoice_service.update_invoice(db, invoice_id, invoice)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return updated


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    deleted = invoice_service.delete_invoice(db, invoice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted"}
