from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from models.best_seller.best_seller import BestSeller
from schemas.best_seller.best_seller import BestSellerSchema
from models.vendor.vendors import Vendors



async def get_best_seller_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(BestSeller).where(BestSeller.id == id))
    best_seller = result.scalar_one_or_none()
    if not best_seller:
        raise HTTPException(status_code=404, detail="Best seller not found")
    return best_seller

async def get_all_best_sellers(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(BestSeller).offset(skip).limit(limit))
    return result.scalars().all()



async def create_best_seller(db: AsyncSession, vendor_id: int):
    try:
        result = await db.execute(
            select(Vendors).where(Vendors.id == vendor_id)
        )
        vendor = result.scalar_one_or_none()

        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vendor not found"
            )

        if vendor.total_orders and vendor.total_orders > 0:
            rank = vendor.total_sales / vendor.total_orders
        else:
            rank = 0  
            
        new_best_seller = BestSeller(
            vendor_id=vendor_id,
            rank=rank
        )

        db.add(new_best_seller)
        await db.commit()
        await db.refresh(new_best_seller)

        return new_best_seller

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )



async def update_best_seller(db: AsyncSession, id: int, vendor_id: int):
    try:
        result = await db.execute(select(BestSeller).where(BestSeller.id == id))
        best_seller = result.scalar_one_or_none()
        if not best_seller:
            raise HTTPException(status_code=404, detail="Best seller not found")

        vendor_result = await db.execute(
            select(Vendors).where(Vendors.id == vendor_id)
        )
        vendor = vendor_result.scalar_one_or_none()
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")

        if vendor.total_orders and vendor.total_orders > 0:
            rank = vendor.total_sales / vendor.total_orders
        else:
            rank = 0

        best_seller.vendor_id = vendor_id
        best_seller.rank = rank

        await db.commit()
        await db.refresh(best_seller)
        return best_seller

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

