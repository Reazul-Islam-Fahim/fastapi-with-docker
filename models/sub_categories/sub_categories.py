from sqlalchemy import Column, Integer, String, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class SubCategories(Base):
    __tablename__ = "sub_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(511), nullable=True)
    image = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(String(50), nullable=False, server_default=func.now())
    updated_at = Column(String(50), nullable=False, server_default=func.now(), onupdate=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    categories = relationship("Categories", back_populates="sub_categories")