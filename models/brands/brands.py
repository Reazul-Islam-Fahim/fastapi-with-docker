from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from database.db import Base

class Brands(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(511), nullable=True)
    image = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(String(50), nullable=False, server_default=func.now())
    updated_at = Column(String(50), nullable=False, server_default=func.now(), onupdate=func.now())
    
