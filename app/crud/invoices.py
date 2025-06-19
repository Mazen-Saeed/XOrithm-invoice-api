from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas import InvoiceCreate
from app.models.invoice import Invoice
from app.models.summary import InvoiceSummary
from app.crud.accounts import get_account
from app.crud.exchange_rates import validate_currency_code, get_conversion_rate

def create_invoice(db: Session, invoice_in: InvoiceCreate) -> Invoice:
    # 1) check if account exists
    acct = get_account(db, invoice_in.account_id)
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found.")

    # 2) validate currency code
    validate_currency_code(invoice_in.currency)

    # 3) get exchange rate
    rate = get_conversion_rate(invoice_in.currency)
    converted = invoice_in.amount_original * rate

    # 4) store invoice
    inv = Invoice(
        amount_original=invoice_in.amount_original,
        currency=invoice_in.currency,
        account_id=invoice_in.account_id,
        amount_default=converted
    )
    db.add(inv)

    # 5) edit summary table
    summary = db.query(InvoiceSummary).first()
    summary.total_revenue += converted
    summary.invoice_count += 1
    db.commit()
    db.refresh(inv)
    return inv

def get_invoice(db: Session, invoice_id: int) -> Invoice | None:
    return db.query(Invoice).get(invoice_id)

def get_exchange_rate(db: Session, invoice_id: int) -> dict:
    inv = get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    return {"rate": round(inv.amount_default / inv.amount_original,2)}

def list_all_invoices(db: Session) -> list[type[Invoice]]:
    # Return every invoice in the database.
    return db.query(Invoice).all()

def list_invoices_for_account(db: Session, account_id: int) -> list[Invoice]:
    return db.query(Invoice).filter(Invoice.account_id == account_id).all()

def update_invoice(db: Session, invoice_id: int, invoice_in: InvoiceCreate) -> Invoice:
    # 1) ensure invoice exists
    with db.begin():
        inv = get_invoice(db, invoice_id)
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice not found.")

        old_converted = inv.amount_default

        # 2) Validate currency code
        validate_currency_code(invoice_in.currency)

        # 3) get conversion rate
        rate = get_conversion_rate(invoice_in.currency)

        # 4) store the new data
        inv.amount_original = invoice_in.amount_original
        inv.currency = invoice_in.currency
        inv.amount_default = invoice_in.amount_original * rate

        # 5) edit summary table
        diff = inv.amount_default - old_converted
        summary = db.query(InvoiceSummary).first()
        summary.total_revenue += diff

    db.refresh(inv)
    return inv

def delete_all_invoices(db: Session) -> None:
    with db.begin():
        db.query(Invoice).delete()
        summary = db.query(InvoiceSummary).first()
        summary.total_revenue = 0.0
        summary.invoice_count = 0


def delete_invoice(db: Session, invoice_id: int) -> None:
    with db.begin():
        inv = get_invoice(db, invoice_id)
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice not found.")

        # 1) edit summary table
        summary = db.query(InvoiceSummary).first()
        summary.total_revenue -= inv.amount_default
        summary.invoice_count -= 1

        # 2) delete the invoice
        db.delete(inv)


def get_invoice_rate(db: Session, invoice_id: int) -> dict:
    inv = get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    if inv.amount_original == 0:
        return {"invoice_id": invoice_id, "rate": None}
    return {
        "invoice_id": invoice_id,
        "rate": inv.amount_default / inv.amount_original
    }
