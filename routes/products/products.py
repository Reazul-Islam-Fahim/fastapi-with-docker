from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from crud.products.products import create_product, get_product_by_id, get_all_products, update_product
from schemas.products.products import ProductsSchema
from database.db import get_db
from models.products.products import DiscountTypeEnum
import os
import shutil
import uuid
import json

router = APIRouter(prefix="/products", tags=["products"])

UPLOAD_DIR = "resources/products"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("")
async def list_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_products(db, skip, limit)

@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_by_id(db, product_id)



def save_file(file: UploadFile, folder: str = UPLOAD_DIR) -> str:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    os.makedirs(folder, exist_ok=True)
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(folder, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

@router.post("")
async def create_product_endpoint(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    slug: Optional[str] = Form(None),
    payable_price: float = Form(None),
    discount_type: DiscountTypeEnum = Form(...),
    discount_amount: Optional[float] = Form(None),
    total_stock: int = Form(...),
    available_stock: int = Form(None),
    quantity_sold: int = Form(...),
    variants: Optional[str] = Form(None),
    is_active: bool = Form(True),
    sub_category_id: int = Form(...),
    brand_id: int = Form(...),
    vendor_id: int = Form(...),
    features_id: int = Form(...),
    highligthed_image: Optional[UploadFile] = File(None),
    images: Optional[List[UploadFile]] = File(None),
    db: AsyncSession = Depends(get_db),
):
    highligthed_image_path = save_file(highligthed_image) if highligthed_image else None
    image_paths = [save_file(img) for img in images] if images else []
    try:
        variants_dict = json.loads(variants)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON for variants.")
    product_data = ProductsSchema(
        name=name,
        description=description,
        price=price,
        payable_price=payable_price,
        discount_type=discount_type,
        discount_amount=discount_amount,
        total_stock=total_stock,
        available_stock=available_stock,
        quantity_sold=quantity_sold,
        variants=variants_dict,
        is_active=is_active,
        sub_category_id=sub_category_id,
        brand_id=brand_id,
        vendor_id=vendor_id,
        features_id=features_id,
        slug=slug if slug else None,
    )
    return await create_product(db, product_data, highligthed_image_path, image_paths)

@router.put("/{product_id}")
async def update_product_endpoint(
    product_id: int,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    slug: Optional[str] = Form(None),
    payable_price: float = Form(...),
    discount_type: DiscountTypeEnum = Form(...),
    discount_amount: Optional[float] = Form(None),
    total_stock: int = Form(...),
    available_stock: int = Form(...),
    quantity_sold: int = Form(...),
    variants: Optional[str] = Form(None),
    is_active: bool = Form(True),
    sub_category_id: int = Form(...),
    brand_id: int = Form(...),
    vendor_id: int = Form(...),
    features_id: int = Form(...),
    highligthed_image: Optional[UploadFile] = File(None),
    images: Optional[List[UploadFile]] = File(None),
    db: AsyncSession = Depends(get_db),
):
    highligthed_image_path = save_file(highligthed_image) if highligthed_image else None
    image_paths = [save_file(img) for img in images] if images else []

    try:
        variants_dict = json.loads(variants)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON for variants.")

    product_data = ProductsSchema(
        name=name,
        description=description,
        price=price,
        payable_price=payable_price,
        discount_type=discount_type,
        discount_amount=discount_amount,
        total_stock=total_stock,
        available_stock=available_stock,
        quantity_sold=quantity_sold,
        variants=variants_dict,
        is_active=is_active,
        sub_category_id=sub_category_id,
        brand_id=brand_id,
        vendor_id=vendor_id,
        features_id=features_id,
        slug=slug if slug else None,
    )

    return await update_product(db, product_id, product_data, highligthed_image_path, image_paths)
