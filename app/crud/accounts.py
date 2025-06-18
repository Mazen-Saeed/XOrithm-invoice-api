from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from app.schemas import AccountCreate
from app.models.account import Account
from app.models.invoice import Invoice
from app.models.summary import InvoiceSummary

def create_account(db: Session, account_in: AccountCreate) -> Account:
    # Create and return a new Account.
    with db.begin():
        # Check no duplicate account
        existing = db.query(Account).filter(Account.email == account_in.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered.")
        acct = Account(name=account_in.name, email=account_in.email)
        db.add(acct)

    db.refresh(acct)
    return acct

def get_account(db: Session, account_id: int) -> Account | None:
    return db.query(Account).get(account_id)

def get_account_by_email(db: Session, email: str) -> Account | None:
    return db.query(Account).filter(Account.email == email).first()

def update_account(db: Session, account_id: int, acc_in: AccountCreate) -> type[Account]:
    acc = db.get(Account, account_id)
    if not acc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    acc.name = acc_in.name
    acc.email = acc_in.email
    db.commit()
    db.refresh(acc)
    return acc


def delete_account(db: Session, account_id: int) -> None:
    with db.begin():
        acc = db.get(Account, account_id)
        if not acc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Account not found")

        # 1. get the invoices for this account
        invoices = db.query(Invoice).filter(Invoice.account_id == account_id).all()
        total_to_remove = sum(inv.amount_default for inv in invoices)
        count_to_remove = len(invoices)

        # 2. edit summary table
        summary = db.query(InvoiceSummary).first()
        summary.total_revenue -= total_to_remove
        summary.invoice_count -= count_to_remove

        # 3. Delete the account (cascades invoices)
        db.delete(acc)