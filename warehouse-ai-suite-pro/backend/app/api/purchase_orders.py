from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.purchase_order import PurchaseOrder
from app.models.sku import SKU
from app.schemas.purchase_order import POCreate, POUpdate, POOut

router = APIRouter()

@router.get("", response_model=list[POOut])
def list_pos(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).order_by(PurchaseOrder.id).all()

@router.post("", response_model=POOut, status_code=201)
def create_po(payload: POCreate, db: Session = Depends(get_db)):
    if db.get(SKU, payload.sku_id) is None:
        raise HTTPException(status_code=400, detail="SKU does not exist")
    po = PurchaseOrder(**payload.model_dump())
    db.add(po); db.commit(); db.refresh(po)
    return po

@router.put("/{po_id}", response_model=POOut)
def update_po(po_id: int, payload: POUpdate, db: Session = Depends(get_db)):
    po = db.get(PurchaseOrder, po_id)
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(po, k, v)
    db.commit(); db.refresh(po)
    return po

@router.delete("/{po_id}", status_code=204)
def delete_po(po_id: int, db: Session = Depends(get_db)):
    po = db.get(PurchaseOrder, po_id)
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    db.delete(po); db.commit()
    return None
