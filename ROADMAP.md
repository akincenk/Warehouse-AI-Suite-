# Roadmap

Work I plan to do next, roughly in this order. Each item has an issue in the tracker.
Estimates are rough and include tests and docs.

## 1. Stock movements (about 8 h)

- Receiving a purchase order adds its quantity to the matching inventory row, in the same transaction.
- Enforce purchase order status transitions: `created -> sent -> received`, no going back, no editing a received PO.
- Add a `stock_movements` table (receipt, adjustment, issue) so every change to `on_hand` has a record.
- `POST /inventory/{id}/adjust` for manual corrections with a reason.

## 2. List endpoints that scale (about 4 h)

- `limit` / `offset` pagination on every list endpoint, with a total count.
- Filters: SKU code or name search, supplier, PO status, low stock only.
- Sorting on the common fields.

## 3. Users and roles (about 6 h)

- Replace the single shared API key with per-user keys stored hashed.
- Two roles to start: `admin` (everything) and `staff` (read, adjust stock, receive POs).
- Key create, list and revoke endpoints for admins.

## 4. Low-stock notifications (about 3 h)

- Optional webhook URL in settings; post a JSON payload when a row drops to or below its reorder point.
- Do not repeat the same alert until stock goes back above the reorder point.

## 5. Reports and export (about 3 h)

- CSV export of inventory and purchase orders.
- Simple stock valuation report (unit cost x on hand) once SKUs have a unit cost.

## 6. Housekeeping (about 2 h)

- Test coverage report in CI.
- Seed script with made-up sample data for local demos.
- Tag a first release (`v0.1.0`) with a changelog.
