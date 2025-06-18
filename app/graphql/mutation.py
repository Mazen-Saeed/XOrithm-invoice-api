from ariadne import MutationType
from app.crud.accounts import create_account, update_account, delete_account
from app.crud.invoices import create_invoice, update_invoice, delete_invoice, delete_all_invoices
from app.schemas import InvoiceCreate
from app.schemas.accounts import AccountCreate

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
