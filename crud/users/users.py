from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.users.users import Users
from schemas.users.users import UpdateUserSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_
from datetime import datetime
from typing import Optional
from sqlalchemy import func


async def get_user(db: AsyncSession, id: int):
    result = await db.execute(select(Users).where(Users.id == id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        return None
    
    user_response = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "phone": db_user.phone,
        "gender": db_user.gender,
        "dob": db_user.dob,
        "image": db_user.image,
    }

    return user_response


async def get_users(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    user_id: Optional[int] = None,
    status: Optional[bool] = None,
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    offset = (page - 1) * limit
    base_query = select(Users)

    # Filters
    filters = []
    if user_id:
        filters.append(Users.id == user_id)
    if status is not None:
        filters.append(Users.is_active == status)
    if created_from:
        filters.append(Users.created_at >= created_from)
    if created_to:
        filters.append(Users.created_at <= created_to)
    if search:
        filters.append(
            or_(
                Users.name.ilike(f"%{search}%"),
                Users.email.ilike(f"%{search}%"),
                Users.phone.ilike(f"%{search}%")
            )
        )

    if filters:
        base_query = base_query.where(and_(*filters))

    # Count query
    count_query = select(func.count()).select_from(Users)
    if filters:
        count_query = count_query.where(and_(*filters))
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Sorting
    sort_column = getattr(Users, sort_by, Users.created_at)
    if sort_order == "desc":
        base_query = base_query.order_by(sort_column.desc())
    else:
        base_query = base_query.order_by(sort_column.asc())

    # Pagination
    base_query = base_query.offset(offset).limit(limit)

    result = await db.execute(base_query)
    users = result.scalars().all()

    return {
        "data": [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "dob": user.dob,
                "status": user.is_active,
                "image": user.image,
                "created_at": user.created_at
            }
            for user in users
        ],
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit  # total pages
        }
    }



async def update_user(
    db: AsyncSession, 
    id: int, user: UpdateUserSchema, 
    filePath: str
    ):
    try: 
        result = await db.execute(select(Users).where(Users.id == id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.name = user.name
        db_user.phone = user.phone
        db_user.dob = user.dob
        db_user.gender = user.gender
        db_user.image = filePath

        await db.commit()
        await db.refresh(db_user)
        
        user_response = {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "phone": db_user.phone,
            "dob": db_user.dob, 
            "gender": db_user.gender,
            "image": db_user.image
        }
        
        return user_response

    except HTTPException:
        raise  # re-raise known exceptions like 404

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