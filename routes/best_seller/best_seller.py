from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from schemas.best_seller.best_seller import BestSellerSchema
from crud.best_seller.best_seller import (
    create_best_seller,
    get_best_seller_by_id,
    get_all_best_sellers,
    update_best_seller
)

router = APIRouter(prefix="/best-sellers", tags=["best-sellers"])

@router.post("", response_model=BestSellerSchema)
async def create(vendor_id : int, db: AsyncSession = Depends(get_db)):
    return await create_best_seller(db, vendor_id)

@router.get("/{id}", response_model=BestSellerSchema)
async def read(id: int, db: AsyncSession = Depends(get_db)):
    return await get_best_seller_by_id(db, id)

@router.get("", response_model=list[BestSellerSchema])
async def read_all(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_best_sellers(db, skip, limit)

@router.put("/{id}", response_model=BestSellerSchema)
async def update(id: int, vendor_id : int, db: AsyncSession = Depends(get_db)):
    return await update_best_seller(db, id, vendor_id)

