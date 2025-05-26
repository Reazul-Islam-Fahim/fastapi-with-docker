from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users.users import Users
from schemas.users.users import UserSchema
from database.db import get_db
from auth.registration import register_user, send_verification_email
from auth.security import decode_email_verification_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(
    user: UserSchema,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        new_user = await register_user(db, user)

        background_tasks.add_task(send_verification_email, new_user.email)

        return {
            "message": "Registration successful. Please check your email to verify your account."
        }

    except HTTPException as e:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/verify-email")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        email = decode_email_verification_token(token)

        result = await db.execute(select(Users).where(Users.email == email))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            return {"message": "Email already verified"}

        user.is_verified = True
        await db.commit()

        return {"message": "Email verified successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Verification failed: {str(e)}"
        )
