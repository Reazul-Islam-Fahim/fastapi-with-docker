from pydantic import BaseModel
from typing import Optional
from typing import List
from schemas.sub_categories.sub_categories import SubCategoriesSchema

class CategoriesSchema(BaseModel):
    name: str
    description: Optional[str]
    is_active: bool = True
    sub_categories: Optional[List[SubCategoriesSchema]] = None
    
    class Config:
        orm_mode = True