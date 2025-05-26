from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.users.users import Users
from schemas.users.users import UpdateUserSchema

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

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Users).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "dob": user.dob,
            "image": user.image
        }
        for user in users
    ]

async def update_user(
    db: AsyncSession, 
    id: int, user: UpdateUserSchema, 
    filePath: str
    ):
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