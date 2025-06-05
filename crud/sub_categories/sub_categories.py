from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.sub_categories.sub_categories import SubCategories
from schemas.sub_categories.sub_categories import SubCategoriesSchema
from sqlalchemy.exc import SQLAlchemyError
from models.products.products import Products

async def get_products_by_sub_category_id(db: AsyncSession, sub_category_id: int):
    try:
        result = await db.execute(
            select(Products).where(Products.sub_category_id == sub_category_id)
        )
        products = result.scalars().all()

        return [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "payable_price": p.payable_price,
                "description": p.description,
                "available_stock": p.available_stock,
                "images": p.images,
                "highlighted_image": p.highligthed_image,
                "is_active": p.is_active,
                "created_at": p.created_at
            }
            for p in products
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving products: {str(e)}")



async def get_sub_category_by_id(db: AsyncSession, id: int):
    try:
        result = await db.execute(select(SubCategories).where(SubCategories.id == id))
        db_sub_categories = result.scalar_one_or_none()

        response = {
            "id": db_sub_categories.id,
            "category_id": db_sub_categories.category_id,
            "name": db_sub_categories.name,
            "description": db_sub_categories.description,
            "image": db_sub_categories.image,
            "is_active": db_sub_categories.is_active
        }
        
        # return
    
        return response
    
    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=404, detail="Sub categories is not found...")


async def get_all_sub_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(SubCategories).offset(skip).limit(limit)
    )
    all_sub_categories = result.scalars().all()
    
    return [
        {
            "id": sub_categories.id,
            "category_id": sub_categories.category_id,
            "name": sub_categories.name,
            "description": sub_categories.description,
            "image": sub_categories.image,
            "is_active": sub_categories.is_active
        }
        for sub_categories in all_sub_categories
    ]



# async def update_sub_category(
#     db: AsyncSession,
#     id: int,
#     sub_category_data: SubCategoriesSchema,
#     filePath: str
# ):
#     result = await db.execute(select(SubCategories).where(SubCategories.id == id))
#     db_sub_category = result.scalar_one_or_none()

#     if not db_sub_category:
#         raise HTTPException(status_code=404, detail="Sub Category is not found")

#     db_sub_category.name = sub_category_data.name
#     db_sub_category.category_id = sub_category_data.category_id
#     db_sub_category.description = sub_category_data.description
#     db_sub_category.image = filePath
#     db_sub_category.is_active = sub_category_data.is_active

#     await db.commit()
#     await db.refresh(db_sub_category)

    

#     category_response = {
#         "name": db_sub_category.name,
#         "category_id": db_sub_category.category_id,
#         "description": db_sub_category.description,
#         "image": db_sub_category.image,
#         "is_active": db_sub_category.is_active
#     }

#     return category_response

async def update_sub_category(
    db: AsyncSession,
    id: int,
    sub_category_data: SubCategoriesSchema,
    filePath: str
):
    try:
        result = await db.execute(select(SubCategories).where(SubCategories.id == id))
        db_sub_category = result.scalar_one_or_none()

        if not db_sub_category:
            raise HTTPException(status_code=404, detail="Sub Category not found")

        db_sub_category.name = sub_category_data.name
        db_sub_category.category_id = sub_category_data.category_id
        db_sub_category.description = sub_category_data.description
        db_sub_category.image = filePath
        db_sub_category.is_active = sub_category_data.is_active

        await db.commit()
        await db.refresh(db_sub_category)

        sub_category_response = {
            "name": db_sub_category.name,
            "category_id": db_sub_category.category_id,
            "description": db_sub_category.description,
            "image": db_sub_category.image,
            "is_active": db_sub_category.is_active
        }

        return sub_category_response

    except HTTPException:
        raise  # Re-raise known HTTP errors (like 404)
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

async def create_sub_category(
    db: AsyncSession, 
    sub_category_data: SubCategoriesSchema,
    filePath: str
):
    try:
        result = await db.execute(
            select(SubCategories).where(SubCategories.name == sub_category_data.name)
        )
        existing_sub_category = result.scalar_one_or_none()
        
        if existing_sub_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sub Category with this name already exists"
            )

        new_sub_category = SubCategories(
            name=sub_category_data.name,
            category_id = sub_category_data.category_id,
            description=sub_category_data.description,
            image=filePath,
            is_active=sub_category_data.is_active
        )
        

        db.add(new_sub_category)
        await db.commit()
        await db.refresh(new_sub_category)
        
        return new_sub_category

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )