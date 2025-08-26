# Video Demo Script (Warehouse AI Suite v1)

Goal: A 90-second demo that shows value fast and proves production readiness.

0) Title Card (3s)
- Text: "Warehouse AI Suite - Inventory Intelligence API"
- Subtitle: "FastAPI + Postgres + Alembic - Low Stock Alerts in seconds"

1) Launch (10s)
- Terminal: run `./scripts/demo.sh`
- Narration: "We launch the stack, run migrations, and load demo data in one command."

2) Health + Docs (10s)
- Browser: open http://localhost:8000/health then /docs
- Narration: "Service is healthy. OpenAPI docs are generated automatically."

3) Data Walkthrough (25s)
- Terminal: `curl http://localhost:8000/api/v1/skus`
- Terminal: `curl http://localhost:8000/api/v1/inventory/alerts/low-stock`
- Narration: "We have SKUs, suppliers, inventory, and purchase orders. Alerts highlight items at or below reorder point."

4) Create SKU (15s)
- Terminal: `curl -X POST -H "Content-Type: application/json" -d '{"code":"SKU-DEMO","name":"Demo Item","category":"misc"}' http://localhost:8000/api/v1/skus`
- Narration: "CRUD is complete. Creating a SKU returns the resource payload with IDs."

5) Close (15s)
- Split-screen: Mermaid architecture diagram in README
- Narration: "Clean architecture, real migrations, CI, and seed data. Ready for a Next.js dashboard in v2."

Tips:
- Use a 1080p recording at 60fps
- Shell font size ~18-20pt; browser zoom 110-125 percent
- Keep keystrokes minimal; avoid mouse jitter
