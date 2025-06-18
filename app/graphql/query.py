from ariadne import QueryType, ObjectType
from app.crud.accounts import get_account, get_account_by_email
from app.crud.invoices import get_invoice, list_all_invoices, list_invoices_for_account
from app.crud.analytics import calculate_total_revenue, calculate_average_invoice

query = QueryType()
analytics = ObjectType("Analytics")
account = ObjectType("Account")

@query.field("account")
def resolve_account(_, info, id):
    db = info.context["db"]
    return get_account(db, int(id))

@query.field("accountByEmail")
def resolve_account_by_email(_, info, email):
    db = info.context["db"]
    return get_account_by_email(db, email)

@query.field("allAccounts")
def resolve_all_accounts(_, info):
    db = info.context["db"]
    return db.query().all()

@account.field("invoices")
def resolve_account_invoices(account_obj, info):
    db = info.context["db"]
    return list_invoices_for_account(db, account_obj.id)

@query.field("invoice")
def resolve_invoice(_, info, id):
    db = info.context["db"]
    return get_invoice(db, int(id))

@query.field("allInvoices")
def resolve_all_invoices(_, info):
    db = info.context["db"]
    return list_all_invoices(db)

@query.field("invoicesByAccount")
def resolve_invoices_by_account(_, info, accountId):
    db = info.context["db"]
    return list_invoices_for_account(db, int(accountId))

@query.field("analytics")
def resolve_analytics(_, info):
    return {}

@analytics.field("totalRevenue")
def resolve_total_revenue(obj, info, currency=None):
    db = info.context["db"]
    return calculate_total_revenue(db, currency)["total_revenue"]

@analytics.field("averageInvoice")
def resolve_average_invoice(obj, info, currency=None):
    db = info.context["db"]
    return calculate_total_revenue(db, currency)["total_revenue"]
