from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.invoices import (
    create_invoice, get_invoice, list_invoices_for_account,
    update_invoice, delete_invoice, delete_all_invoices, list_all_invoices, get_exchange_rate
)
from app.schemas import InvoiceCreate, InvoiceRead
from app.rest.deps import get_db

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def api_create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    return create_invoice(db, payload)

@router.get("/",response_model=List[InvoiceRead],summary="List All Invoices")
def api_list_all_invoices(db: Session = Depends(get_db)):
    return list_all_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceRead)
def api_get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    inv = get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invoice not found")
    return inv

@router.get("/by-account/{account_id}", response_model=List[InvoiceRead])
def api_list_invoices_for_account(account_id: int, db: Session = Depends(get_db)):
    return list_invoices_for_account(db, account_id)

@router.get("/{invoice_id}/rate", response_model=dict)
def api_get_invoice_rate(invoice_id: int, db: Session = Depends(get_db)):
    return get_exchange_rate(db, invoice_id)

@router.delete("/",status_code=status.HTTP_204_NO_CONTENT,summary="Delete all invoices and reset analytics")
def api_delete_all_invoices(db: Session = Depends(get_db)):
    delete_all_invoices(db)
    return None

@router.put("/{invoice_id}", response_model=InvoiceRead)
def api_update_invoice(invoice_id: int, payload: InvoiceCreate, db: Session = Depends(get_db)):
    return update_invoice(db, invoice_id, payload)

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    delete_invoice(db, invoice_id)
    return None
