from ariadne import MutationType
from app.crud.accounts import create_account, update_account, delete_account
from app.crud.invoices import create_invoice, update_invoice, delete_invoice, delete_all_invoices
from app.schemas import InvoiceCreate
from app.schemas.accounts import AccountCreate
from app.crud.accounts import get_account_by_email

mutation = MutationType()

@mutation.field("createAccount")
def resolve_create_account(_, info, input):
    db = info.context["db"]
    acct_in = AccountCreate(**input)
    return create_account(db, acct_in)

@mutation.field("updateAccount")
def resolve_update_account(_, info, id, input):
    db = info.context["db"]
    acct_in = AccountCreate(**input)
    return update_account(db, int(id), acct_in)

@mutation.field("deleteAccount")
def resolve_delete_account(_, info, id):
    db = info.context["db"]
    delete_account(db, int(id))
    return True

@mutation.field("createInvoice")
def resolve_create_invoice(_, info, input):
    db = info.context["db"]
    invoice_in = InvoiceCreate(**input)
    return create_invoice(db, invoice_in)

@mutation.field("updateInvoice")
def resolve_update_invoice(_, info, id, input):
    db = info.context["db"]
    invoice_in = InvoiceCreate(**input)
    return update_invoice(db, int(id), invoice_in)

@mutation.field("deleteInvoice")
def resolve_delete_invoice(_, info, id):
    db = info.context["db"]
    delete_invoice(db, int(id))
    return True

@mutation.field("deleteAllInvoices")
def resolve_delete_all(_, info):
    db = info.context["db"]
    delete_all_invoices(db)
    return True

@mutation.field("createInvoiceByEmail")
def resolve_create_invoice_by_email(_, info, input):
    db = info.context["db"]
    account = get_account_by_email(db, input["email"])
    if not account:
        raise Exception("Account with this email does not exist")
    invoice_in = InvoiceCreate(
        amount_original=input["amount_original"],
        currency=input["currency"],
        account_id=account.id
    )
    return create_invoice(db, invoice_in)
