from pydantic import BaseModel, EmailStr
from models.users.users import genders
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    dob: str
    gender: genders
    isChecked: Optional[bool] = False
    role: Optional[str] = "user"
    
    class Config:
        orm_mode = True
        

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True
        
class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[genders] = None
    
    class Config:
        orm_mode = True