from pydantic import BaseModel
from typing import Optional

class SubCategoriesSchema(BaseModel):
    name: str
    description: Optional[str]
    category_id: int
    is_active: bool = True
    
    class Config:
        orm_mode = True