from fastapi import APIRouter, Depends, HTTPException, Query, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from crud.categories.categories import get_category_by_id, get_all_categories, get_sub_category_by_category_id, update_category, create_category
from database.db import get_db
from schemas.categories.categories import CategoriesSchema
from typing import Optional
import os
import shutil

router = APIRouter(prefix="/categories", tags=["categories"])

UPLOAD_DIR = "resources/categories"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("")
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_categories(db, skip, limit)


@router.get("/{id}")
async def get_category_by_id_data(id: int, db: AsyncSession = Depends(get_db)):
    return await get_category_by_id(db, id)


@router.get("/get_sub_categories/{category_id}")
async def read_subcategories_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await get_sub_category_by_category_id(db, category_id)




@router.put("/{id}")
async def update_category_info(
    id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    category_data = CategoriesSchema(
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
    
    return await update_category(db, id, category_data, file_path)

@router.post("", response_model=CategoriesSchema)
async def create_category_data(
    name: str = Form(...),
    description: str = Form(None),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        category_data = CategoriesSchema(
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
            
            return await create_category(db, category_data, file_path)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )