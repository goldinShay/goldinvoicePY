from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate
from app.services.invoice_item_service import create_invoice_item, delete_items_for_invoice

def calculate_totals(items, vat_percentage, outside_eu):
    subtotal = sum(item.quantity * item.unit_price for item in items)

    if outside_eu:
        vat_percentage = 0

    vat_amount = subtotal * (vat_percentage / 100)
    total = subtotal + vat_amount

    return subtotal, total

def create_invoice(db: Session, invoice: InvoiceCreate):
    subtotal, total = calculate_totals(invoice.items, invoice.vat, invoice.outside_eu)

    db_invoice = Invoice(
        contact_id=invoice.contact_id,
        invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date,
        description=invoice.description,
        currency=invoice.currency,
        vat=invoice.vat,
        outside_eu=invoice.outside_eu,
        subtotal=subtotal,
        total=total,
        payment_instructions=invoice.payment_instructions,
        note=invoice.note
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in invoice.items:
        create_invoice_item(db, db_invoice.id, item)

    return db_invoice

def update_invoice(db: Session, invoice_id: int, invoice: InvoiceUpdate):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        return None

    for key, value in invoice.dict(exclude_unset=True, exclude={"items"}).items():
        setattr(db_invoice, key, value)

    if invoice.items is not None:
        delete_items_for_invoice(db, invoice_id)
        for item in invoice.items:
            create_invoice_item(db, invoice_id, item)

    subtotal, total = calculate_totals(
        invoice.items or db_invoice.items,
        invoice.vat or db_invoice.vat,
        invoice.outside_eu or db_invoice.outside_eu
    )

    db_invoice.subtotal = subtotal
    db_invoice.total = total

    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        return None
    db.delete(db_invoice)
    db.commit()
    return True
