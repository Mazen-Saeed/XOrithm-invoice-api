from sqlalchemy import Column, Integer, Float

from app.db import Base

class InvoiceSummary(Base):
    __tablename__ = "invoice_summary"

    id = Column(Integer, primary_key=True, index=True)
    total_revenue  = Column(Float,   nullable=False, default=0.0)
    invoice_count  = Column(Integer, nullable=False, default=0)

