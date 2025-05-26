import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://sharif:password@localhost:5433/pooz_store"
)



# SQLALCHEMY_DATABASE_URL=f"postgresql+asyncpg://sharif:password@localhost:5432/pooz_store"
SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://postgres:password@192.168.0.100:5432/postgres"