from sqlalchemy import Column, Integer, String, Boolean, Enum as senum, func
from sqlalchemy.orm import relationship
from enum import Enum
from database.db import Base

class roles(str, Enum):
    admin = "admin"
    user = "user"
    
class genders(str, Enum):
    M = 'M'
    F = 'F'
    O = 'O'
    

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    dob = Column(String(15), nullable=False)
    gender = Column(senum(genders), nullable=False)
    image = Column(String(255), nullable=True)
    role = Column(senum(roles), nullable=False, default=roles.user)
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    isChecked = Column(Boolean, nullable=False, default=False)
    created_at = Column(String(50), nullable=False, server_default=func.now())
    updated_at = Column(String(50), nullable=False, server_default=func.now(), onupdate=func.now())

    vendors = relationship("Vendors", back_populates="users")