import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.main import app
from app.rest.deps import get_db

# 1) throwaway SQLite file
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
if os.path.exists("test.db"):
    os.remove("test.db")

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# create tables and seed summary row once per session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # create all tables
    Base.metadata.create_all(bind=engine)
    from app.models.summary import InvoiceSummary
    db = TestingSessionLocal()
    db.add(InvoiceSummary(total_revenue=0.0, invoice_count=0))
    db.commit()
    db.close()
    yield
    # Teardown
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")

# 3) clear all data before each test
@pytest.fixture(autouse=True)
def clear_db():
    db = TestingSessionLocal()
    db.execute(text("DELETE FROM invoices"))
    db.execute(text("DELETE FROM accounts"))
    db.execute(text("UPDATE invoice_summary SET total_revenue=0.0, invoice_count=0"))
    db.commit()
    db.close()

# 4) session per request
@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# 5) seed data to test with: 3 accounts + 6 invoices
@pytest.fixture()
def seeded_db(client):
    accounts = []
    for i in range(1, 4):
        email = f"ahmed{i}@gmail.com"
        res = client.post(
            "/api/accounts/",
            json={"name": f"ahmed{i}", "email": email}
        )
        acc = res.json()
        accounts.append(acc)
        client.post(
            "/api/invoices/",
            json={
                "amount_original": 10.0 * i,
                "currency": "USD",
                "account_id": acc["id"],
            },
        )
        client.post(
            "/api/invoices/",
            json={
                "amount_original": 20.0 * i,
                "currency": "USD",
                "account_id": acc["id"],
            },
        )
    return accounts
