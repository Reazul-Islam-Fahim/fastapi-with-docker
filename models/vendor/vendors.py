from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from database.db import Base

class Vendors(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_name = Column(String(50), nullable=False)
    documents = Column(JSON, nullable=True)
    business_address = Column(String(255), nullable=True)
    pick_address = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)
    vendor_slug = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    is_shipping_enabled = Column(Boolean, nullable=False, default=False)
    default_shipping_rate = Column(Integer, nullable=True)
    free_shipping_threshold = Column(Integer, nullable=True)
    total_sales = Column(Integer, nullable=True, default=0)
    total_orders = Column(Integer, nullable=True, default=0)
    last_order_date = Column(String(50), nullable=True)
   
    users = relationship("Users", back_populates="vendors")
    bank_details = relationship("BankDetails", back_populates="vendors")
    best_seller = relationship("BestSeller", back_populates="vendors")
    products = relationship("Products", back_populates="vendors")
