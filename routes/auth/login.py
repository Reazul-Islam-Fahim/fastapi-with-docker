from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users.users import LoginSchema
from auth.login import login_user
from database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(user: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await login_user(db, user)