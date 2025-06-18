from fastapi import APIRouter, Depends
from typing import Optional

from sqlalchemy.orm import Session
from app.crud.analytics import calculate_total_revenue, calculate_average_invoice
from app.rest.deps import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/total")
def api_total_revenue(
    currency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return calculate_total_revenue(db, currency)

@router.get("/average")
def api_average_invoice(
    currency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return calculate_average_invoice(db, currency)
