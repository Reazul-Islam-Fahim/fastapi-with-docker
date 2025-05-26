from pydantic import BaseModel

class ProductFeaturesSchema(BaseModel):
    name: str
    type: str
    value: float
    is_active: bool
    
    class Config:
        orm_mode = True
