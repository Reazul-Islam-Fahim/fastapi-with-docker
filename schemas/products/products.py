from pydantic import BaseModel
from typing import Optional, List
from models.products.products import DiscountTypeEnum

class ProductsSchema(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: float
    payable_price: float
    discount_type: Optional[DiscountTypeEnum] = None 
    discount_amount: Optional[float] = 0.0
    highligthed_image: Optional[str] = None
    images: Optional[List[str]] = None
    total_stock: int = 0
    available_stock: int = 0
    quantity_sold: int = 0
    variants: Optional[dict] = None
    is_active: bool = True
    sub_category_id: int
    brand_id: int
    vendor_id: int
    features_id: int
    
    class Config:
        orm_mode = True
