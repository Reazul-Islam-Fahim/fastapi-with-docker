from typing import Optional
from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from models.users.users import genders
from crud.users.users import get_user, get_users, update_user
from database.db import get_db
from schemas.users.users import UpdateUserSchema
import os
import shutil
from datetime import datetime


router = APIRouter(prefix="/users", tags=["users"])

UPLOAD_DIR = "resources/users"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: Optional[str] = None,
    user_id: Optional[int] = None,
    status: Optional[bool] = None,
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "name"]),
    sort_order: str = Query("desc", enum=["asc", "desc"])
):
    return await get_users(
        db=db,
        page=page,
        limit=limit,
        search=search,
        user_id=user_id,
        status=status,
        created_from=created_from,
        created_to=created_to,
        sort_by=sort_by,
        sort_order=sort_order
    )



@router.get("/{user_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
async def update_user_info(
    user_id: int,
    name: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    dob: Optional[str] = Form(None),
    gender: Optional[genders] = Form(None),
    image: Optional[UploadFile] = File(None),
    fileName : Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):   
    user = UpdateUserSchema(
        name=name,
        phone=phone,
        dob=dob,
        gender= gender
    )
    
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    filename = f"{fileName}_{image.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return await update_user(db, user_id, user, file_path)
