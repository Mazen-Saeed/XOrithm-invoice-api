from sqlalchemy import Column, Integer, Float, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base


class Invoice(Base):
    __tablename__ = "invoices"

    # Primary key(auto incrementing)
    id = Column(Integer, primary_key=True, index=True)

    # invoice amount
    amount_original = Column(Float, nullable=False)

    # amount in default currency (USD)
    amount_default = Column(Float, nullable=False)

    # original currency
    currency = Column(String(3), nullable=False)

    # Timestamp
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # account that created the invoice
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    account = relationship("Account", back_populates="invoices")
