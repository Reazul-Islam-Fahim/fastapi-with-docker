from pydantic import BaseModel
from typing import Optional

class VendorsSchema(BaseModel):
    user_id : Optional[int]
    store_name: str
    documents: Optional[dict] = None
    business_address: Optional[str] = None
    pick_address: Optional[str] = None
    vendor_slug: str
    is_active: bool = True
    is_verified: bool = False
    is_shipping_enabled: bool = False
    default_shipping_rate: Optional[int] = None
    free_shipping_threshold: Optional[int] = None
    total_sales: Optional[int] = 0
    total_orders: Optional[int] = 0
    last_order_date: Optional[str] = None
    
    class Config:
        from_attributes = True