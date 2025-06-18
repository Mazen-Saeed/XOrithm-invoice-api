from app.crud.exchange_rates import get_conversion_rate
def test_invoice_crud_and_list_by_account(client):
    res = client.post("/api/accounts/", json={
        "name": "Ahmed", "email": "Ahmed@gmail.com"
    })
    acc_id = res.json()["id"]

    r1 = client.post("/api/invoices/", json={
        "amount_original": 4000.0, "currency": "EGP", "account_id": acc_id
    })
    r2 = client.post("/api/invoices/", json={
        "amount_original": 200.0,  "currency": "USD", "account_id": acc_id
    })
    inv1 = r1.json(); inv2 = r2.json()

    assert round(inv1["amount_default"],2) == round((4000 * get_conversion_rate("EGP", "USD")), 2)
    assert inv2["amount_default"] == 200.0

    assert client.get(f"/api/invoices/{inv1['id']}").json()["amount_default"] == round((4000 * get_conversion_rate("EGP", "USD")), 2)
    acc = client.get(f"/api/invoices/by-account/{acc_id}").json()
    assert {i["id"] for i in acc} == {inv1["id"], inv2["id"]}

    client.delete(f"/api/invoices/{inv2['id']}")
    assert client.get(f"/api/invoices/{inv2['id']}").status_code == 404


def test_list_all_invoices_after_seeding(client, seeded_db):
    res = client.get("/api/invoices/")
    assert res.status_code == 200
    assert len(res.json()) == 6

    for acc in seeded_db:
        print(acc)
        arr = client.get(f"/api/invoices/by-account/{acc["id"]}").json()
        assert len(arr) == 2
