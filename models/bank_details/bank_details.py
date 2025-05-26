from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class BankDetails(Base):
    __tablename__ = "bank_details"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    bank_account_name = Column(String, nullable=False)
    bank_account_number = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    branch_name = Column(String, nullable=False)
    ifsc_code = Column(String, nullable=False)
    paypal_email = Column(String, nullable=True)
    payout_pref = Column(String, nullable=False)  
    is_active = Column(Boolean, default=True)
   
    vendors = relationship("Vendors", back_populates="bank_details")