def test_supplier_crud(client):
    r = client.post("/api/v1/suppliers", json={"name": "Acme"})
    assert r.status_code == 201
    s = r.json()
    assert s["lead_time_days"] == 7

    r = client.put(f"/api/v1/suppliers/{s['id']}", json={"lead_time_days": 3})
    assert r.json()["lead_time_days"] == 3
    assert len(client.get("/api/v1/suppliers").json()) == 1

    assert client.delete(f"/api/v1/suppliers/{s['id']}").status_code == 204
    assert client.get("/api/v1/suppliers").json() == []


def test_duplicate_supplier_conflicts(client, supplier):
    assert client.post("/api/v1/suppliers", json={"name": "Acme"}).status_code == 409


def test_rename_to_existing_name_conflicts(client, supplier):
    other = client.post("/api/v1/suppliers", json={"name": "Globex"}).json()
    r = client.put(f"/api/v1/suppliers/{other['id']}", json={"name": "Acme"})
    assert r.status_code == 409


def test_missing_supplier_returns_404(client):
    assert client.put("/api/v1/suppliers/999", json={"name": "x"}).status_code == 404
    assert client.delete("/api/v1/suppliers/999").status_code == 404


def test_negative_lead_time_rejected(client):
    assert client.post("/api/v1/suppliers", json={"name": "X", "lead_time_days": -1}).status_code == 422


def test_deleting_supplier_unlinks_inventory(client, sku, supplier):
    inv = client.post("/api/v1/inventory", json={"sku_id": sku["id"], "supplier_id": supplier["id"]}).json()
    assert client.delete(f"/api/v1/suppliers/{supplier['id']}").status_code == 204
    rows = client.get("/api/v1/inventory").json()
    assert [(r["id"], r["supplier_id"]) for r in rows] == [(inv["id"], None)]


def test_duplicate_insert_and_rename_race_return_409(client, supplier, monkeypatch):
    from sqlalchemy.orm import Query

    other = client.post("/api/v1/suppliers", json={"name": "Globex"}).json()
    monkeypatch.setattr(Query, "first", lambda self: None)  # pre-checks miss, as under a race
    assert client.post("/api/v1/suppliers", json={"name": "Acme"}).status_code == 409
    assert client.put(f"/api/v1/suppliers/{other['id']}", json={"name": "Acme"}).status_code == 409
    monkeypatch.undo()
    assert sorted(s["name"] for s in client.get("/api/v1/suppliers").json()) == ["Acme", "Globex"]
