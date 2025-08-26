# Screenshots Guide

Take and save these PNG files into this folder:

1. FastAPI Docs
   - Open: http://localhost:8000/docs
   - Save as: fastapi_docs.png

2. Low Stock Alerts (cURL output)
   - Run: curl http://localhost:8000/api/v1/inventory/alerts/low-stock | jq .
   - Save terminal screenshot as: low_stock.png

3. SKUs List (cURL output)
   - Run: curl http://localhost:8000/api/v1/skus | jq .
   - Save terminal screenshot as: skus_list.png

4. Postman Collection
   - Open Postman, import docs/postman_collection.json
   - Send "List SKUs" request
   - Save response panel screenshot as: postman_list_skus.png

Optional:
- Health endpoint: health.png (curl http://localhost:8000/health)
- ER Diagram preview: er_preview.png (optional browser capture of README section)
