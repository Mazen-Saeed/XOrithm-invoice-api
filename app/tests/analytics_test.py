def test_analytics_empty_and_after_invoices(client):
    empty = client.get("/api/analytics/total").json()
    assert empty == {"total_revenue": 0.0, "currency": "USD"}

    res = client.post("/api/accounts/", json={"name":"Ahmed","email":"ahmed@gmail.com"})
    aid = res.json()["id"]
    client.post("/api/invoices/", json={"amount_original":10,"currency":"USD","account_id":aid})
    client.post("/api/invoices/", json={"amount_original":30,"currency":"USD","account_id":aid})

    tot = client.get("/api/analytics/total?currency=USD").json()
    avg = client.get("/api/analytics/average?currency=USD").json()
    assert tot["total_revenue"] == 40.0
    assert avg["average_invoice"] == 20.0

def test_analytics_on_seeded_db(client, seeded_db):
    stats = client.get("/api/analytics/total?currency=USD").json()
    assert stats["total_revenue"] == 180.0

    avg = client.get("/api/analytics/average?currency=USD").json()
    assert avg["average_invoice"] == 30.0
