from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def get_contacts(db: Session):
    # Stable ordering by creation time
    return db.query(Contact).order_by(Contact.created_at.asc()).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(
        first_name=contact.first_name,
        middle_name=contact.middle_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        company_name=contact.company_name,   # ⭐ ADDED
        birth_date=contact.birth_date,
        location=contact.location,
        notes=contact.notes,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, update_data: dict):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None

    for field, value in update_data.items():
        setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None

    db.delete(db_contact)
    db.commit()
    return True
