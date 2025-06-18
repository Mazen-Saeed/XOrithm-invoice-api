from sqlalchemy.orm import Session
from app.config import settings
from app.models.summary import InvoiceSummary
from app.crud.exchange_rates import validate_currency_code,get_conversion_rate


def calculate_total_revenue(db: Session, target_currency: str | None = None) -> dict:
    # Sum all invoices for all accounts.
    base = 'USD'
    row = db.query(InvoiceSummary).first()
    total = row.total_revenue

    if target_currency is not None and target_currency != base:
        validate_currency_code(target_currency)
        rate = get_conversion_rate(base,target_currency)
        total = total * rate
    else:
        total = total
        target_currency = 'USD'

    return {"total_revenue": round(total,2), "currency": target_currency}

def calculate_average_invoice(db: Session, target_currency: str | None = None) -> dict:
    summary = db.query(InvoiceSummary).first()
    count = summary.invoice_count

    if count == 0:
        return {"average_invoice": 0.0, "currency": target_currency or settings.default_currency}

    total_info = calculate_total_revenue(db, target_currency)
    avg = total_info["total_revenue"] / count

    return {"average_invoice": round(avg,2), "currency": total_info["currency"]}