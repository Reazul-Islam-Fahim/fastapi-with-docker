from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database.db import get_db
from schemas.bank_details.bank_details import BankDetailsSchema
from crud.bank_details.bank_details import (
    get_bank_details_by_id,
    get_all_bank_details,
    update_bank_details,
    create_bank_details
)

router = APIRouter(prefix="/bank-details", tags=["bank-details"])


@router.get("/{id}", response_model=BankDetailsSchema)
async def read_bank_detail(id: int, db: AsyncSession = Depends(get_db)):
    bank_detail = await get_bank_details_by_id(db, id)
    if not bank_detail:
        raise HTTPException(status_code=404, detail="Bank details not found")
    return bank_detail

@router.get("", response_model=List[BankDetailsSchema])
async def read_all_bank_details(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_all_bank_details(db, skip, limit)


@router.put("/{id}", response_model=BankDetailsSchema)
async def update_bank_detail(id: int, bank_data: BankDetailsSchema, db: AsyncSession = Depends(get_db)):
    return await update_bank_details(db, id, bank_data)

@router.post("", response_model=BankDetailsSchema)
async def add_bank_details(bank_data: BankDetailsSchema, db: AsyncSession = Depends(get_db)):
    return await create_bank_details(db, bank_data)
