def test_sku_crud(client):
    r = client.post("/api/v1/skus", json={"code": "A-1", "name": "Bolt"})
    assert r.status_code == 201
    sku = r.json()
    assert sku["code"] == "A-1" and sku["category"] is None

    assert client.get(f"/api/v1/skus/{sku['id']}").json()["name"] == "Bolt"
    assert [s["code"] for s in client.get("/api/v1/skus").json()] == ["A-1"]

    r = client.put(f"/api/v1/skus/{sku['id']}", json={"category": "hardware"})
    assert r.status_code == 200
    assert r.json()["category"] == "hardware" and r.json()["name"] == "Bolt"

    assert client.delete(f"/api/v1/skus/{sku['id']}").status_code == 204
    assert client.get(f"/api/v1/skus/{sku['id']}").status_code == 404


def test_duplicate_code_conflicts(client, sku):
    r = client.post("/api/v1/skus", json={"code": sku["code"], "name": "Other"})
    assert r.status_code == 409


def test_missing_sku_returns_404(client):
    assert client.get("/api/v1/skus/999").status_code == 404
    assert client.put("/api/v1/skus/999", json={"name": "x"}).status_code == 404
    assert client.delete("/api/v1/skus/999").status_code == 404


def test_sku_validation(client):
    assert client.post("/api/v1/skus", json={"name": "no code"}).status_code == 422
    assert client.post("/api/v1/skus", json={"code": "", "name": "x"}).status_code == 422
    assert client.post("/api/v1/skus", json={"code": "x" * 65, "name": "x"}).status_code == 422


def test_null_name_rejected(client, sku):
    assert client.put(f"/api/v1/skus/{sku['id']}", json={"name": None}).status_code == 400


def test_deleting_sku_cascades_to_inventory_and_pos(client, sku):
    client.post("/api/v1/inventory", json={"sku_id": sku["id"]})
    client.post("/api/v1/purchase-orders", json={"sku_id": sku["id"], "qty": 5})
    assert client.delete(f"/api/v1/skus/{sku['id']}").status_code == 204
    assert client.get("/api/v1/inventory").json() == []
    assert client.get("/api/v1/purchase-orders").json() == []
