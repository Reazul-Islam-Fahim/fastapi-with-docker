from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status, UploadFile, File
from models.sub_categories.sub_categories import SubCategories
from models.categories.categories import Categories
from schemas.categories.categories import CategoriesSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload


async def get_category_by_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(Categories).where(Categories.id == id).options(selectinload(Categories.sub_categories))
    )
    db_category = result.scalar_one_or_none()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    return db_category  




async def get_all_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Categories)
        .options(selectinload(Categories.sub_categories))
        .offset(skip)
        .limit(limit)
    )
    categories = result.scalars().all()
    return categories  



async def get_sub_category_by_category_id(db: AsyncSession, category_id: int):
    try:
        result = await db.execute(
            select(SubCategories).where(SubCategories.category_id == category_id)
        )
        sub_categories = result.scalars().all()

        if not sub_categories:
            raise HTTPException(status_code=404, detail="No subcategories found for this category.")

        return sub_categories

    except HTTPException:
        raise  # re-raise 404 error

    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="Error retrieving subcategories.")




async def update_category(
    db: AsyncSession,
    id: int,
    category_data: CategoriesSchema,
    filePath: str
):
    result = await db.execute(select(Categories).where(Categories.id == id))
    db_category = result.scalar_one_or_none()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db_category.name = category_data.name
    db_category.description = category_data.description
    db_category.image = filePath

    await db.commit()
    await db.refresh(db_category)

    

    category_response = {
        "name": db_category.name,
        "description": db_category.description,
        "IsActive": db_category.is_active
    }

    return category_response

async def create_category(
    db: AsyncSession, 
    category_data: CategoriesSchema,
    filePath: str
):
    try:
        result = await db.execute(
            select(Categories).where(Categories.name == category_data.name)
        )
        existing_category = result.scalar_one_or_none()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists"
            )

        new_category = Categories(
            name=category_data.name,
            description=category_data.description,
            is_active=category_data.is_active,
            image=filePath
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