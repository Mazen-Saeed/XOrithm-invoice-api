def test_account_crud(client):
    res = client.post("/api/accounts/", json={
        "name": "Ahmed Wael",
        "email": "ahmed@gmail.com"
    })
    assert res.status_code == 201
    acc = res.json()
    acc_id = acc["id"]

    res = client.get(f"/api/accounts/{acc_id}")
    assert res.status_code == 200
    assert res.json()["email"] == "ahmed@gmail.com"

    res = client.put(f"/api/accounts/{acc_id}", json={
        "name": "Mohamed",
        "email": "Mohamed@gmail.com"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Mohamed"

    res = client.get(f"/api/accounts/?email={data["email"]}")

    assert res.status_code == 200
    assert res.json()["id"] == acc_id

    res = client.get(f"/api/accounts/?email=Mohammed@gmail.com")

    assert res.status_code == 404

    res = client.delete(f"/api/accounts/{acc_id}")
    assert res.status_code == 204

    res = client.get(f"/api/accounts/{acc_id}")
    assert res.status_code == 404
