from pydantic import BaseModel
from typing import Optional

class BrandSchema(BaseModel):
    name: str
    description: Optional[str]
    is_active: bool = True
    
    class Config:
        orm_mode = True