from sqlalchemy.exc import SQLAlchemyError
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from models.bank_details.bank_details import BankDetails
from schemas.bank_details.bank_details import BankDetailsSchema

async def get_bank_details_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(BankDetails).where(BankDetails.id == id))
    db_bank_details = result.scalar_one_or_none()

    if not db_bank_details:
        return None
    
    return db_bank_details

async def get_all_bank_details(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(BankDetails).offset(skip).limit(limit)
    )
    bank_details = result.scalars().all()
    
    return [
        {
            "id": details.id,
            "vendor_id": details.vendor_id,
            "bank_account_name": details.bank_account_name,
            "bank_account_number": details.bank_account_number,
            "bank_name": details.bank_name,
            "branch_name": details.branch_name,
            "ifsc_code": details.ifsc_code,
            "paypal_email": details.paypal_email,
            "payout_pref": details.payout_pref,
            "is_active": details.is_active
        }
        for details in bank_details
    ]

async def update_bank_details(
    db: AsyncSession, 
    id: int, 
    bank_details: BankDetailsSchema
):
    result = await db.execute(select(BankDetails).where(BankDetails.id == id))
    db_bank_details = result.scalar_one_or_none()

    if not db_bank_details:
        raise HTTPException(status_code=404, detail="Bank details not found")

    db_bank_details.bank_account_name = bank_details.bank_account_name
    db_bank_details.bank_account_number = bank_details.bank_account_number
    db_bank_details.bank_name = bank_details.bank_name
    db_bank_details.branch_name = bank_details.branch_name
    db_bank_details.ifsc_code = bank_details.ifsc_code
    db_bank_details.paypal_email = bank_details.paypal_email
    db_bank_details.payout_pref = bank_details.payout_pref
    db_bank_details.is_active = bank_details.is_active

    await db.commit()
    await db.refresh(db_bank_details)

    return db_bank_details


async def create_bank_details(db: AsyncSession, bank_data: BankDetailsSchema):
    try:
        new_bank_detail = BankDetails(
            vendor_id=bank_data.vendor_id,
            bank_account_name=bank_data.bank_account_name,
            bank_account_number=bank_data.bank_account_number,
            bank_name=bank_data.bank_name,
            branch_name=bank_data.branch_name,
            ifsc_code=bank_data.ifsc_code,
            paypal_email=bank_data.paypal_email,
            payout_pref=bank_data.payout_pref,
            is_active=bank_data.is_active,
        )

        db.add(new_bank_detail)
        await db.commit()
        await db.refresh(new_bank_detail)

        return new_bank_detail

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )