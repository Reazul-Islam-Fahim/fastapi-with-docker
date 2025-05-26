from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.product_features.product_features import (
    get_product_feature_by_id,
    get_all_product_features,
    create_product_feature,
    update_product_feature
)
from database.db import get_db
from schemas.product_features.product_features import ProductFeaturesSchema
from typing import List

router = APIRouter(prefix="/product-features", tags=["product-features"])


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_product_features(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_product_features(db, skip=skip, limit=limit)


@router.get("/{feature_id}", status_code=status.HTTP_200_OK)
async def read_product_feature_by_id(
    feature_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_product_feature_by_id(db, feature_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_feature(
    feature: ProductFeaturesSchema,
    db: AsyncSession = Depends(get_db)
):
    return await create_product_feature(db, feature)


@router.put("/{feature_id}", status_code=status.HTTP_200_OK)
async def update_feature(
    feature_id: int,
    feature: ProductFeaturesSchema,
    db: AsyncSession = Depends(get_db)
):
    return await update_product_feature(db, feature_id, feature)
