from sqlalchemy.orm import Session
from app.models.invoice_item import InvoiceItem
from app.schemas.invoice_item import InvoiceItemCreate

def create_invoice_item(db: Session, invoice_id: int, item: InvoiceItemCreate):
    subtotal = item.quantity * item.unit_price

    db_item = InvoiceItem(
        invoice_id=invoice_id,
        description=item.description,
        quantity=item.quantity,
        unit_price=item.unit_price,
        subtotal=subtotal
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_items_for_invoice(db: Session, invoice_id: int):
    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
    db.commit()
