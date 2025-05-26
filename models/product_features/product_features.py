from sqlalchemy import Column, Integer, String, Boolean, Float
from database.db import Base

class ProductFeatures(Base):
    __tablename__ = 'product_features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
