from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.brands.brands import Brands
from schemas.brands.brands import BrandSchema
from sqlalchemy.exc import SQLAlchemyError


async def get_brands_by_id(db: AsyncSession, id: int):
    try:
        result = await db.execute(select(Brands).where(Brands.id == id))
        db_brands = result.scalar_one_or_none()

        response = {
            "id": db_brands.id,
            "name": db_brands.name,
            "description": db_brands.description,
            "image": db_brands.image,
            "is_active": db_brands.is_active
        }
        
        return response
    
    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=404, detail="Brand is not found...")


async def get_all_brands(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Brands).offset(skip).limit(limit)
    )
    all_brands = result.scalars().all()
    
    return [
        {
            "id": brand.id,
            "name": brand.name,
            "description": brand.description,
            "image": brand.image,
            "is_active": brand.is_active
        }
        for brand in all_brands
    ]


from sqlalchemy.exc import SQLAlchemyError

async def update_brand(
    db: AsyncSession,
    id: int,
    brand_data: BrandSchema,
    filePath: str
):
    try:
        result = await db.execute(select(Brands).where(Brands.id == id))
        db_brand_data = result.scalar_one_or_none()

        if not db_brand_data:
            raise HTTPException(status_code=404, detail="Brand not found")

        db_brand_data.name = brand_data.name
        db_brand_data.description = brand_data.description
        db_brand_data.image = filePath
        db_brand_data.is_active = brand_data.is_active

        await db.commit()
        await db.refresh(db_brand_data)

        brand_response = {
            "name": db_brand_data.name,
            "description": db_brand_data.description,
            "image": db_brand_data.image,
            "is_active": db_brand_data.is_active
        }

        return brand_response

    except HTTPException:
        raise  # Re-raise to preserve 404
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )



async def create_brand(
    db: AsyncSession, 
    brand_data: BrandSchema,
    filePath: str
):
    try:
        result = await db.execute(
            select(Brands).where(Brands.name == brand_data.name)
        )
        existing_brand = result.scalar_one_or_none()
        
        if existing_brand:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Brand with this name already exists"
            )

        new_brand = Brands(
            name=brand_data.name,
            description=brand_data.description,
            image=filePath,
            is_active=brand_data.is_active
        )
        
        db.add(new_brand)
        await db.commit()
        await db.refresh(new_brand)
        
        return new_brand

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )