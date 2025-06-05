from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.products.products import Products
from schemas.products.products import ProductsSchema
from utils.slug import generate_unique_slug
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

def calc_payable_price(
    price: float,
    discount_type: str,
    discount_amount: Optional[float] = None
) -> float:
    if discount_type == "percentage" and discount_amount is not None and 0 < discount_amount <= 100:
        return price * (1 - discount_amount / 100)
    elif discount_type == "fixed" and discount_amount is not None and 0 < discount_amount <= price:
        return price - discount_amount
    else:
        return price

async def get_product_by_id(db: AsyncSession, product_id: int) -> Products:
    result = await db.execute(select(Products).where(Products.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

async def get_all_products(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Products]:
    result = await db.execute(select(Products).offset(skip).limit(limit))
    return result.scalars().all()

async def create_product(
    db: AsyncSession,
    product_data: ProductsSchema,
    highligthed_image_path: Optional[str] = None,
    image_paths: Optional[List[str]] = None
):
    try:
        new_slug = await generate_unique_slug(db, product_data.name)

        product_data.payable_price = calc_payable_price(
            product_data.price,
            product_data.discount_type.value,
            product_data.discount_amount
        )

        new_product = Products(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            payable_price=product_data.payable_price,
            discount_type=product_data.discount_type,
            discount_amount=product_data.discount_amount,
            total_stock=product_data.total_stock,
            available_stock=product_data.total_stock - product_data.quantity_sold,
            quantity_sold=product_data.quantity_sold,
            variants=product_data.variants,
            is_active=product_data.is_active,
            sub_category_id=product_data.sub_category_id,
            brand_id=product_data.brand_id,
            vendor_id=product_data.vendor_id,
            features_id=product_data.features_id,
            highligthed_image=highligthed_image_path,
            images=image_paths or [],
            slug=new_slug,
        )

        if new_product.available_stock > new_product.total_stock:
            new_product.available_stock = new_product.total_stock

        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def update_product(
    db: AsyncSession,
    product_id: int,
    product_data: ProductsSchema,
    highligthed_image_path: Optional[str] = None,
    image_paths: Optional[List[str]] = None
):
    try:
        new_slug = await generate_unique_slug(db, product_data.name)
        product = await get_product_by_id(db, product_id)

        product_data.payable_price = calc_payable_price(
            product_data.price,
            product_data.discount_type.value,
            product_data.discount_amount
        )

        product.name = product_data.name
        product.description = product_data.description
        product.price = product_data.price
        product.payable_price = product_data.payable_price
        product.discount_type = product_data.discount_type
        product.discount_amount = product_data.discount_amount
        product.total_stock = product_data.total_stock
        product.available_stock = product_data.total_stock - product_data.quantity_sold
        product.quantity_sold = product_data.quantity_sold
        product.variants = product_data.variants
        product.is_active = product_data.is_active
        product.sub_category_id = product_data.sub_category_id
        product.brand_id = product_data.brand_id
        product.vendor_id = product_data.vendor_id
        product.features_id = product_data.features_id
        product.slug = new_slug

        if highligthed_image_path:
            product.highligthed_image = highligthed_image_path
        if image_paths:
            product.images = image_paths

        if product.available_stock > product.total_stock:
            product.available_stock = product.total_stock

        await db.commit()
        await db.refresh(product)
        return product

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
