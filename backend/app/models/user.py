from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
from app.models.enums import Role

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(Role), default=Role.USER)
