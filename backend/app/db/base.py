from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.contact import Contact
from app.models.invoice import Invoice
