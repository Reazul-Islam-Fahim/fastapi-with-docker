import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Pooz Store"
    DEBUG: bool = False
    BASE_URL: str = "http://localhost:8000"
    
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@192.168.0.100/postgres"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    SECRET_KEY: str = "your-secret-key-with-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24
    
    EMAIL_FROM: str = "freazulislam@gmail.com"
    EMAIL_FROM_NAME: str = "My App Team"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "freazulislam@gmail.com"
    SMTP_PASSWORD: str = "qhdp jcrw dxmy iqua "
    EMAIL_TEMPLATE_DIR: str = "email-templates"
    EMAIL_VERIFICATION_SUBJECT: str = "Verify Your Email"
    
    VERIFICATION_URL: str = "http://localhost:8000/verify-email?token={token}"
    PASSWORD_RESET_URL: str = "http://localhost:8000/reset-password?token={token}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    settings = Settings()  

EMAIL_VERIFICATION_TEMPLATE = """
<html>
<body>
    <h1>Verify Your Email</h1>
    <p>Click the link below to verify your email address:</p>
    <a href="{verification_url}">Verify Email</a>
    <p>This link expires in {expire_hours} hours.</p>
</body>
</html>
"""

PASSWORD_RESET_TEMPLATE = """
<html>
<body>
    <h1>Password Reset</h1>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_url}">Reset Password</a>
    <p>This link expires in {expire_hours} hours.</p>
</body>
</html>
"""