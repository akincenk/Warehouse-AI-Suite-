def test_inventory_crud(client, sku, supplier):
    r = client.post("/api/v1/inventory", json={"sku_id": sku["id"], "supplier_id": supplier["id"], "on_hand": 40})
    assert r.status_code == 201
    inv = r.json()
    assert (inv["on_hand"], inv["reorder_point"], inv["reorder_qty"]) == (40, 10, 50)

    r = client.put(f"/api/v1/inventory/{inv['id']}", json={"on_hand": 12})
    assert r.json()["on_hand"] == 12

    assert client.delete(f"/api/v1/inventory/{inv['id']}").status_code == 204
    assert client.get("/api/v1/inventory").json() == []


def test_unknown_sku_or_supplier_is_400(client, sku):
    assert client.post("/api/v1/inventory", json={"sku_id": 999}).status_code == 400
    r = client.post("/api/v1/inventory", json={"sku_id": sku["id"], "supplier_id": 999})
    assert r.status_code == 400
    inv = client.post("/api/v1/inventory", json={"sku_id": sku["id"]}).json()
    assert client.put(f"/api/v1/inventory/{inv['id']}", json={"supplier_id": 999}).status_code == 400


def test_missing_row_is_404(client):
    assert client.put("/api/v1/inventory/999", json={"on_hand": 1}).status_code == 404
    assert client.delete("/api/v1/inventory/999").status_code == 404


def test_validation(client, sku):
    assert client.post("/api/v1/inventory", json={"sku_id": sku["id"], "on_hand": -1}).status_code == 422
    assert client.post("/api/v1/inventory", json={"sku_id": sku["id"], "reorder_qty": 0}).status_code == 422
    inv = client.post("/api/v1/inventory", json={"sku_id": sku["id"]}).json()
    assert client.put(f"/api/v1/inventory/{inv['id']}", json={"on_hand": None}).status_code == 400


def test_low_stock_alerts(client, sku):
    other = client.post("/api/v1/skus", json={"code": "SKU-2", "name": "Gadget"}).json()
    third = client.post("/api/v1/skus", json={"code": "SKU-3", "name": "Gizmo"}).json()
    below = client.post("/api/v1/inventory", json={"sku_id": sku["id"], "on_hand": 3, "reorder_point": 10}).json()
    equal = client.post("/api/v1/inventory", json={"sku_id": other["id"], "on_hand": 10, "reorder_point": 10}).json()
    above = client.post("/api/v1/inventory", json={"sku_id": third["id"], "on_hand": 11, "reorder_point": 10}).json()

    ids = [r["id"] for r in client.get("/api/v1/inventory/alerts/low-stock").json()]
    assert ids == [below["id"], equal["id"]]

    # Restocking clears the alert; draining stock raises one.
    client.put(f"/api/v1/inventory/{below['id']}", json={"on_hand": 100})
    client.put(f"/api/v1/inventory/{above['id']}", json={"on_hand": 0})
    ids = [r["id"] for r in client.get("/api/v1/inventory/alerts/low-stock").json()]
    assert ids == [equal["id"], above["id"]]
