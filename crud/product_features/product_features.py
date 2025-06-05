from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from models.product_features.product_features import ProductFeatures
from schemas.product_features.product_features import ProductFeaturesSchema


async def get_product_feature_by_id(db: AsyncSession, id: int):
    try:
        result = await db.execute(select(ProductFeatures).where(ProductFeatures.id == id))
        db_feature = result.scalar_one_or_none()

        if not db_feature:
            raise HTTPException(status_code=404, detail="Product feature not found.")

        return db_feature

    except HTTPException:
        raise  
    except Exception as e:
        print("DB Error (Get by ID):", repr(e))
        raise HTTPException(status_code=500, detail="Error retrieving product feature.")


async def get_all_product_features(db: AsyncSession, skip: int = 0, limit: int = 10):
    try:
        result = await db.execute(
            select(ProductFeatures).offset(skip).limit(limit)
        )
        features = result.scalars().all()

        return features

    except Exception as e:
        print("DB Error (Get all):", repr(e))
        raise HTTPException(status_code=500, detail="Error retrieving product features.")


async def create_product_feature(db: AsyncSession, feature: ProductFeaturesSchema):
    try:
        new_feature = ProductFeatures(
            name=feature.name,
            type=feature.type,
            value=feature.value,
            is_active=feature.is_active
        )
        db.add(new_feature)
        await db.commit()
        await db.refresh(new_feature)

        return new_feature

    except SQLAlchemyError as e:
        await db.rollback()
        print("DB Error (Create):", repr(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during creation: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        print("Unexpected Error (Create):", repr(e))
        raise HTTPException(status_code=500, detail="Unexpected error while creating product feature.")


async def update_product_feature(db: AsyncSession, id: int, feature: ProductFeaturesSchema):
    try:
        result = await db.execute(select(ProductFeatures).where(ProductFeatures.id == id))
        db_feature = result.scalar_one_or_none()

        if not db_feature:
            raise HTTPException(status_code=404, detail="Product feature not found.")

        db_feature.name = feature.name
        db_feature.type = feature.type
        db_feature.value = feature.value
        db_feature.is_active = feature.is_active

        await db.commit()
        await db.refresh(db_feature)

        return db_feature

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        print("DB Error (Update):", repr(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during update: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        print("Unexpected Error (Update):", repr(e))
        raise HTTPException(status_code=500, detail="Unexpected error while updating product feature.")
