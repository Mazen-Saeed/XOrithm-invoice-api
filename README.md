# XOrithm Invoice Analytics API

**Live Demo:** [http://13.62.71.198:8000/](http://13.62.71.198:8000/)

---

## Overview

XOrithm Invoice Analytics API is a robust backend for managing and analyzing invoices in multiple currencies. Built with **FastAPI** and **PostgreSQL**, it provides REST and GraphQL endpoints for CRUD, analytics, and advanced business intelligence, all with automatic real-time currency conversion.

---

## Features

- **Invoice CRUD**: Create, retrieve, update, and delete invoices with multi-currency support.
- **Currency Conversion**: Converts invoice amounts to USD (or any currency) using live rates.
- **Analytics**: Instantly calculate total revenue, average invoice size, and revenue trends.
- **GraphQL API**: Query accounts and invoices efficiently in one call.
- **Swagger Docs**: Explore the API interactively at `/docs`.
- **Error Handling**: Clear feedback for invalid data and external API issues.
- **Unit Tests**: Quality-checked endpoints for reliability.

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Migrations:** Alembic
- **GraphQL:** Ariadne
- **Testing:** Pytest, Nose
- **Deployment:** Docker, Docker Compose, AWS EC2

---

## API Reference
Full API documentation: http://13.62.71.198:8000/docs

### Accounts

- `POST   /api/accounts/` — Create account
- `GET    /api/accounts/` — Get account by email
- `GET    /api/accounts/{account_id}` — Get account by ID
- `PUT    /api/accounts/{account_id}` — Update account
- `DELETE /api/accounts/{account_id}` — Delete account and invoices

### Invoices

- `GET    /api/invoices/` — List all invoices
- `POST   /api/invoices/` — Create invoice
- `DELETE /api/invoices/` — Delete all invoices/reset analytics
- `GET    /api/invoices/{invoice_id}` — Get invoice by ID
- `PUT    /api/invoices/{invoice_id}` — Update invoice
- `DELETE /api/invoices/{invoice_id}` — Delete invoice
- `GET    /api/invoices/by-account/{account_id}` — List invoices for account
- `GET    /api/invoices/{invoice_id}/rate` — Get invoice exchange rate

### Analytics

- `GET    /api/analytics/total` — Total revenue
- `GET    /api/analytics/average` — Average invoice

### GraphQL

- [http://13.62.71.198:8000/graphql](http://13.62.71.198:8000/graphql) — Playground for advanced queries

**Example GraphQL Query:**

```graphql
{
  account(id: 1) {
    id
    name
    invoices {
      id
      amount
      currency
      converted_amount
    }
  }
}
```

## Project Structure

```plaintext
.
├── app/
│   ├── crud/           # Database operations
│   ├── graphql/        # GraphQL schema, queries, mutations
│   ├── models/         # SQLAlchemy models
│   ├── rest/           # REST endpoints
│   ├── schemas/        # Pydantic schemas
│   └── tests/          # Unit tests
├── alembic/            # Migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

```
