from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from models.users.users import Users
from schemas.users.users import UserSchema
from fastapi import HTTPException
from auth.security import hash_password, create_email_verification_token
from datetime import datetime
from typing import Optional
from email.mime.text import MIMEText
import smtplib
from config import settings  

async def register_user(db: AsyncSession, user: UserSchema) -> Users:
    try:
        result = await db.execute(
            select(Users).where(Users.email == user.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            return None

        new_user = Users(
            name=user.name,
            email=user.email,
            password=hash_password(user.password),
            phone=user.phone,
            dob=user.dob,
            gender=user.gender,
            role=user.role,
            isChecked=user.isChecked,
            is_verified=False,
        )

        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)  
        await db.commit()

        return new_user

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

async def send_verification_email(email: str):
    token = create_email_verification_token(email)
    # verification_url = f"{settings.BASE_URL}/auth/verify-email?token={token}"
    
    verification_url = f"http://www.localhost:3000/auth/verify-email?token={token}"
    
    message = MIMEText(
        f"Please verify your email by clicking: {verification_url}\n\n"
        f"This link expires in 24 hours."
    )
    message['Subject'] = "Verify Your Email"
    message['From'] = settings.EMAIL_FROM
    message['To'] = email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
