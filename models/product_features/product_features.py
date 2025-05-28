from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base
from sqlalchemy.orm import relationship

class ProductFeatures(Base):
    __tablename__ = 'product_features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    products = relationship("Products", back_populates="product_features")
