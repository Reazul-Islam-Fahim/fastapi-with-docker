from fastapi import APIRouter, Depends, HTTPException, Query, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from crud.sub_categories.sub_categories import get_products_by_sub_category_id, get_sub_category_by_id, get_all_sub_categories, update_sub_category, create_sub_category
from database.db import get_db
from schemas.sub_categories.sub_categories import SubCategoriesSchema
from typing import Optional
import os
import shutil

router = APIRouter(prefix="/sub-categories", tags=["sub-categories"])

UPLOAD_DIR = "resources/sub-categories"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("")
async def get_sub_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_sub_categories(db, skip, limit)

@router.get("/{id}")
async def get_sub_category_by_id_data(id: int, db: AsyncSession = Depends(get_db)):
    sub_category = await get_sub_category_by_id(db, id)
    if not sub_category:
        raise HTTPException(status_code=404, detail="Sub Category is not found")
    return sub_category


@router.put("/{id}")
async def update_sub_category_info(
    id: int,
    name: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    sub_category_data = SubCategoriesSchema(
        name=name,
        category_id=category_id,
        description=description,
        is_active=is_active
    )
    
    if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

    filename = f"{name}_{image.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return await update_sub_category(db, id, sub_category_data, file_path)

@router.post("", response_model=SubCategoriesSchema)
async def create_sub_category_data(
    name: str = Form(...),
    category_id: Optional[int] = Form(None),
    description: str = Form(None),
    is_active: Optional[bool] = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        sub_category_data = SubCategoriesSchema(
            name=name,
            category_id=category_id,
            description=description,
            is_active=is_active
        )
        
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image.")

        filename = f"{name}_{image.filename.replace(' ', '_')}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
            return await create_sub_category(db, sub_category_data, file_path)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
        
        
@router.get("/{id}/products")
async def get_products_by_sub_category(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_products_by_sub_category_id(db, id)
