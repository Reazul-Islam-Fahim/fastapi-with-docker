from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from models.users.users import Users
from schemas.users.users import LoginSchema
from fastapi import HTTPException, status
from auth.security import verify_password, create_access_token

async def login_user(db: AsyncSession, user: LoginSchema) -> dict:
    try:
        # Async query to find user
        result = await db.execute(
            select(Users).where(Users.email == user.email)
        )
        db_user = result.scalars().first()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = create_access_token(
            data={
                "sub": db_user.email,
                "id": db_user.id,
                "role": db_user.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )