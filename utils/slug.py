import re
from unidecode import unidecode
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.products.products import Products

async def generate_unique_slug(db: AsyncSession, name: str) -> str:
    """
    Generate a URL-friendly slug and ensure it's unique
    """
    # Basic slugification
    slug = unidecode(name.lower())
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    
    # Check for uniqueness
    counter = 1
    original_slug = slug
    while True:
        result = await db.execute(select(Products).where(Products.slug == slug))
        if not result.scalar_one_or_none():
            return slug
        slug = f"{original_slug}-{counter}"
        counter += 1