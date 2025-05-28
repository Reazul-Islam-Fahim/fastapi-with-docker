from sqlalchemy import Column, Integer, String, Boolean, func, ForeignKey, Float, Enum as senum, ARRAY, JSON
from sqlalchemy.orm import relationship
from database.db import Base
from enum import Enum

class DiscountTypeEnum(Enum):
    fixed = "fixed"
    percentage = "percentage"

class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable= True, unique=True)
    description = Column(String(511), nullable=True)
    price = Column(Float, nullable=False)
    payable_price = Column(Float, nullable=False)
    discount_type = Column(senum(DiscountTypeEnum), nullable=False)
    discount_amount = Column(Float, nullable=True, default=0.0)
    highligthed_image = Column(String(255), nullable=True)
    images = Column(ARRAY(String(255)), nullable=True)
    total_stock = Column(Integer, nullable=False, default=0)
    available_stock = Column(Integer, nullable=False, default=0)
    quantity_sold = Column(Integer, nullable=False, default=0)
    variants = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(String(50), nullable=False, server_default=func.now())
    updated_at = Column(String(50), nullable=False, server_default=func.now(), onupdate=func.now())
    
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    features_id = Column(Integer, ForeignKey("product_features.id"), nullable=False)
    
    sub_categories = relationship("SubCategories", back_populates="products")
    brands = relationship("Brands", back_populates="products")
    vendors = relationship("Vendors", back_populates="products")
    product_features = relationship("ProductFeatures", back_populates="products")