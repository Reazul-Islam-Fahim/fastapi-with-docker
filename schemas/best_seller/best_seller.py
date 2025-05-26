from pydantic import BaseModel

class BestSellerSchema(BaseModel):
    vendor_id: int
    rank: float

    class Config:
        orm_mode = True
