from fastapi import FastAPI
from app.rest.accounts   import router as accounts_router
from app.rest.invoices   import router as invoices_router
from app.rest.analytics  import router as analytics_router
from app.graphql         import graphql_app

app = FastAPI()

app.include_router(accounts_router, prefix="/api")
app.include_router(invoices_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")

app.mount("/graphql", graphql_app)
