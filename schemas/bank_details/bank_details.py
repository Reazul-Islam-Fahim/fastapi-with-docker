from pydantic import BaseModel, EmailStr
from typing import Optional


class BankDetailsSchema(BaseModel):
    vendor_id: int
    bank_account_name: str
    bank_account_number: str
    bank_name: str
    branch_name: str
    ifsc_code: str
    paypal_email: Optional[EmailStr] = None
    payout_pref: str
    is_active: Optional[bool] = True
    
    class Config:
        orm_mode = True