from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.crud.accounts import create_account, get_account, get_account_by_email, update_account, delete_account
from app.schemas import AccountCreate, AccountRead
from app.rest.deps import get_db

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def api_create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, payload)

@router.get("/{account_id}", response_model=AccountRead)
def api_get_account(account_id: int, db: Session = Depends(get_db)):
    acct = get_account(db, account_id)
    if not acct:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    return acct

@router.get("/", response_model=AccountRead)
def api_get_account_by_email(email: Optional[str] = None, db: Session = Depends(get_db)):
    if not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email query required")
    acct = get_account_by_email(db, email)
    if not acct:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    return acct


@router.put("/{account_id}",response_model=AccountRead,summary="Update an account")
def api_update_account(account_id: int,payload: AccountCreate,db: Session = Depends(get_db)):
    return update_account(db, account_id, payload)

@router.delete("/{account_id}",status_code=status.HTTP_204_NO_CONTENT,summary="Delete an account (and its invoices)")
def api_delete_account(account_id: int,db: Session = Depends(get_db)):
    delete_account(db, account_id)
    return None
