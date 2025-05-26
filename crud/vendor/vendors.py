import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.vendor.vendors import Vendors
from schemas.vendor.vendors import VendorsSchema
from sqlalchemy.exc import SQLAlchemyError


# async def get_vendor_by_id(db: AsyncSession, id: int):
#     result = await db.execute(select(Vendors).where(Vendors.id == id))
#     vendors = result.scalar_one_or_none()

#     response = {
#         "id": vendors.id,
#         "store_name": vendors.store_name,
#         "documents": vendors.documents,
#         "business_address": vendors.business_address,
#         "pick_address": vendors.pick_address,
#         "logo": vendors.logo,
#         "vendor_slug": vendors.vendor_slug,
#         "is_active": vendors.is_active,
#         "is_verified": vendors.is_verified,
#         "is_shipping_enabled": vendors.is_shipping_enabled,
#         "default_shipping_rate": vendors.default_shipping_rate,
#         "free_shipping_threshold": vendors.free_shipping_threshold,
#         "total_sales": vendors.total_sales,
#         "total_orders": vendors.total_orders,
#         "last_order_date": vendors.last_order_date
#     }
    
#     return response

async def get_vendor_by_id(db: AsyncSession, id: int) -> VendorsSchema:
    result = await db.execute(select(Vendors).where(Vendors.id == id))
    vendor = result.scalar_one_or_none()

    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return VendorsSchema.from_orm(vendor)

async def get_all_vendors(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Vendors).offset(skip).limit(limit)
    )
    vendors = result.scalars().all()
    
    return [
        {
            "id": vendor.id,
            "user_id": vendor.user_id,
            "store_name": vendor.store_name,
            "documents": vendor.documents,
            "business_address": vendor.business_address,
            "pick_address": vendor.pick_address,
            "logo": vendor.logo,
            "vendor_slug": vendor.vendor_slug,
            "is_active": vendor.is_active,
            "is_verified": vendor.is_verified,
            "is_shipping_enabled": vendor.is_shipping_enabled,
            "default_shipping_rate": vendor.default_shipping_rate,
            "free_shipping_threshold": vendor.free_shipping_threshold,
            "total_sales": vendor.total_sales,
            "total_orders": vendor.total_orders,
            "last_order_date": vendor.last_order_date
        }
        for vendor in vendors
    ]



async def update_vendor(
    db: AsyncSession,
    id: int,
    vendor_data: VendorsSchema,
    filePath: str
):
    result = await db.execute(select(Vendors).where(Vendors.id == id))
    db_vendor = result.scalar_one_or_none()

    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    db_vendor.store_name = vendor_data.store_name
    db_vendor.documents = vendor_data.documents
    db_vendor.business_address = vendor_data.business_address
    db_vendor.pick_address = vendor_data.pick_address
    db_vendor.logo = filePath
    db_vendor.vendor_slug = vendor_data.vendor_slug
    db_vendor.is_active = vendor_data.is_active
    db_vendor.is_verified = vendor_data.is_verified
    db_vendor.is_shipping_enabled = vendor_data.is_shipping_enabled
    db_vendor.default_shipping_rate = vendor_data.default_shipping_rate
    db_vendor.free_shipping_threshold = vendor_data.free_shipping_threshold
    db_vendor.total_sales = vendor_data.total_sales
    db_vendor.total_orders = vendor_data.total_orders
    db_vendor.last_order_date = vendor_data.last_order_date    

    await db.commit()
    await db.refresh(db_vendor)

    return db_vendor

async def create_vendor(
    db: AsyncSession, 
    vendor_data: VendorsSchema,
    filePath: str
):
    try:
        result = await db.execute(
            select(Vendors).where(Vendors.user_id == vendor_data.user_id)
        )
        existing_vendor = result.scalar_one_or_none()
        
        if existing_vendor:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vendor with this user details already exists"
            )

        new_category = Vendors(
            user_id=vendor_data.user_id,
            store_name=vendor_data.store_name,
            documents=vendor_data.documents,
            business_address=vendor_data.business_address,
            pick_address=vendor_data.pick_address,
            logo=filePath,
            vendor_slug=vendor_data.vendor_slug,
            is_active=vendor_data.is_active,
            is_verified=vendor_data.is_verified,
            is_shipping_enabled=vendor_data.is_shipping_enabled,
            default_shipping_rate=vendor_data.default_shipping_rate,
            free_shipping_threshold=vendor_data.free_shipping_threshold,
            total_sales=vendor_data.total_sales,
            total_orders=vendor_data.total_orders,
            last_order_date=vendor_data.last_order_date
        )
        

        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        
        return new_category

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )