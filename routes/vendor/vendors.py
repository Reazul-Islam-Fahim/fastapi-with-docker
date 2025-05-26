import json
from fastapi import APIRouter, Depends, HTTPException, Query, status, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from crud.vendor.vendors import get_vendor_by_id, get_all_vendors, update_vendor, create_vendor
from database.db import get_db
from schemas.vendor.vendors import VendorsSchema
from typing import Optional
import os
import shutil

router = APIRouter(prefix="/vendors", tags=["vendors"])

UPLOAD_DIR = "resources/vendors"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("")
async def get_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_vendors(db, skip, limit)

@router.get("/{id}")
async def get_vendor_by_id_data(id: int, db: AsyncSession = Depends(get_db)):
    vendor = await get_vendor_by_id(db, id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor is not found")
    return vendor

@router.put("/{id}")
async def update_sub_category_info(
    id: int,
    user_id: int = Form(...),
    vendor_slug: str = Form(...),
    store_name: Optional[str] = Form(None),
    documents: Optional[str] = Form(None), 
    business_address: Optional[str] = Form(None),
    pick_address: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    is_verified: Optional[bool] = Form(None),
    is_shipping_enabled: Optional[bool] = Form(None),
    default_shipping_rate: Optional[int] = Form(None),
    free_shipping_threshold: Optional[int] = Form(None),
    total_sales: Optional[int] = Form(None),
    total_orders: Optional[int] = Form(None),
    last_order_date: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        documents_dict = None
        if documents:
            try:
                documents_dict = json.loads(documents)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON format in 'documents'")

        file_path = None
        if image:
            if not image.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="File must be an image.")

            filename = f"{store_name}_{image.filename.replace(' ', '_')}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            os.makedirs(UPLOAD_DIR, exist_ok=True)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

        vendor_data = VendorsSchema(
            user_id=user_id,
            vendor_slug=vendor_slug,
            store_name=store_name,
            documents=documents_dict,
            business_address=business_address,
            pick_address=pick_address,
            is_active=is_active,
            is_verified=is_verified,
            is_shipping_enabled=is_shipping_enabled,
            default_shipping_rate=default_shipping_rate,
            free_shipping_threshold=free_shipping_threshold,
            total_sales=total_sales,
            total_orders=total_orders,
            last_order_date=last_order_date
        )

        return await update_vendor(db, id, vendor_data, file_path)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("", response_model=VendorsSchema)
async def create_vendor_data(
    user_id: int = Form(...),
    store_name: str = Form(...),
    vendor_slug: str = Form(...),
    documents: Optional[str] = Form(None),  # Accept JSON string
    business_address: Optional[str] = Form(None),
    pick_address: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(True),
    is_verified: Optional[bool] = Form(False),
    is_shipping_enabled: Optional[bool] = Form(False),
    default_shipping_rate: Optional[int] = Form(None),
    free_shipping_threshold: Optional[int] = Form(None),
    total_sales: Optional[int] = Form(0),
    total_orders: Optional[int] = Form(0),
    last_order_date: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        import json
        parsed_documents = None
        if documents:
            try:
                parsed_documents = json.loads(documents)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON in documents")

        vendor_data = VendorsSchema(
            user_id=user_id,
            store_name=store_name,
            vendor_slug=vendor_slug,
            documents=parsed_documents,
            business_address=business_address,
            pick_address=pick_address,
            is_active=is_active,
            is_verified=is_verified,
            is_shipping_enabled=is_shipping_enabled,
            default_shipping_rate=default_shipping_rate,
            free_shipping_threshold=free_shipping_threshold,
            total_sales=total_sales,
            total_orders=total_orders,
            last_order_date=last_order_date
        )

        file_path = None
        if image:
            if not image.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="File must be an image.")
            filename = f"{store_name}_{image.filename.replace(' ', '_')}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

        new_vendor = await create_vendor(db, vendor_data, file_path)
        return new_vendor

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
