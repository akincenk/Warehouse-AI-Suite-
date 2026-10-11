from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.inventory import Inventory
from app.models.sku import SKU
from app.models.supplier import Supplier
from app.schemas.inventory import InventoryCreate, InventoryOut, InventoryUpdate

router = APIRouter()


def _check_supplier(db: Session, supplier_id: int | None) -> None:
    if supplier_id is not None and db.get(Supplier, supplier_id) is None:
        raise HTTPException(status_code=400, detail="Supplier does not exist")


@router.get("", response_model=list[InventoryOut])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).order_by(Inventory.id).all()

@router.post("", response_model=InventoryOut, status_code=201)
def create_row(payload: InventoryCreate, db: Session = Depends(get_db)):
    sku = db.get(SKU, payload.sku_id)
    if not sku:
        raise HTTPException(status_code=400, detail="SKU does not exist")
    _check_supplier(db, payload.supplier_id)
    inv = Inventory(**payload.model_dump())
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.put("/{inv_id}", response_model=InventoryOut)
def update_row(inv_id: int, payload: InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.get(Inventory, inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory row not found")
    data = payload.model_dump(exclude_unset=True)
    if any(data.get(k, 0) is None for k in ("on_hand", "reorder_point", "reorder_qty")):
        raise HTTPException(status_code=400, detail="Only supplier_id can be null")
    _check_supplier(db, data.get("supplier_id"))
    for k, v in data.items():
        setattr(inv, k, v)
    db.commit()
    db.refresh(inv)
    return inv

@router.delete("/{inv_id}", status_code=204)
def delete_row(inv_id: int, db: Session = Depends(get_db)):
    inv = db.get(Inventory, inv_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory row not found")
    db.delete(inv)
    db.commit()
    return None

@router.get("/alerts/low-stock", response_model=list[InventoryOut])
def low_stock_alerts(db: Session = Depends(get_db)):
    """Rows whose on-hand quantity is at or below their reorder point."""
    return (
        db.query(Inventory)
        .filter(Inventory.on_hand <= Inventory.reorder_point)
        .order_by(Inventory.id)
        .all()
    )
