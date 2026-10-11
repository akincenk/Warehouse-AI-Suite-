def test_po_crud(client, sku):
    r = client.post("/api/v1/purchase-orders", json={"sku_id": sku["id"], "qty": 20})
    assert r.status_code == 201
    po = r.json()
    assert po["status"] == "created"

    r = client.put(f"/api/v1/purchase-orders/{po['id']}", json={"status": "sent"})
    assert r.json()["status"] == "sent"
    assert len(client.get("/api/v1/purchase-orders").json()) == 1

    assert client.delete(f"/api/v1/purchase-orders/{po['id']}").status_code == 204
    assert client.get("/api/v1/purchase-orders").json() == []


def test_unknown_sku_is_400(client):
    assert client.post("/api/v1/purchase-orders", json={"sku_id": 999, "qty": 1}).status_code == 400


def test_missing_po_is_404(client):
    assert client.put("/api/v1/purchase-orders/999", json={"qty": 1}).status_code == 404
    assert client.delete("/api/v1/purchase-orders/999").status_code == 404


def test_validation(client, sku):
    assert client.post("/api/v1/purchase-orders", json={"sku_id": sku["id"], "qty": 0}).status_code == 422
    r = client.post("/api/v1/purchase-orders", json={"sku_id": sku["id"], "qty": 1, "status": "lost"})
    assert r.status_code == 422
    po = client.post("/api/v1/purchase-orders", json={"sku_id": sku["id"], "qty": 1}).json()
    assert client.put(f"/api/v1/purchase-orders/{po['id']}", json={"status": None}).status_code == 400
