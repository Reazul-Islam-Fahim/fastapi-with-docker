from fastapi import APIRouter, Depends, HTTPException, Query, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from crud.brands.brands import get_brands_by_id, get_all_brands, update_brand, create_brand
from database.db import get_db
from schemas.brands.brands import BrandSchema
from typing import Optional
import os
import shutil

router = APIRouter(prefix="/brands", tags=["brands"])

UPLOAD_DIR = "resources/brands"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("")
async def get_sub_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_brands(db, skip, limit)

@router.get("/{id}")
async def get_brands_by_id_data(id: int, db: AsyncSession = Depends(get_db)):
    brand = await get_brands_by_id(db, id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.put("/{id}")
async def update_brand_info(
    id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    brand_data = BrandSchema(
        name=name,
        description=description,
        is_active=is_active
    )
    
    if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

    filename = f"{name}_{image.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return await update_brand(db, id, brand_data, file_path)

@router.post("", response_model=BrandSchema)
async def create_brand_data(
    name: str = Form(...),
    description: str = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        brand_data = BrandSchema(
            name=name,
            description=description,
            is_active=is_active
        )
        
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

        filename = f"{name}_{image.filename.replace(' ', '_')}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
            return await create_brand(db, brand_data, file_path)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )