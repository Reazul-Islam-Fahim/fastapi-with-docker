from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class BestSeller(Base):
    __tablename__ = "best_seller"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    rank = Column(Numeric, nullable=False)

    vendors = relationship("Vendors", back_populates="best_seller")
    
