from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.sku import SKU
from app.schemas.sku import SKUCreate, SKUUpdate, SKUOut

router = APIRouter()

@router.get("", response_model=list[SKUOut])
def list_skus(db: Session = Depends(get_db)):
    return db.query(SKU).order_by(SKU.id).all()

@router.post("", response_model=SKUOut, status_code=201)
def create_sku(payload: SKUCreate, db: Session = Depends(get_db)):
    exists = db.query(SKU).filter(SKU.code == payload.code).first()
    if exists:
        raise HTTPException(status_code=409, detail="SKU code already exists")
    sku = SKU(code=payload.code, name=payload.name, category=payload.category)
    db.add(sku); db.commit(); db.refresh(sku)
    return sku

@router.get("/{sku_id}", response_model=SKUOut)
def get_sku(sku_id: int, db: Session = Depends(get_db)):
    sku = db.get(SKU, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    return sku

@router.put("/{sku_id}", response_model=SKUOut)
def update_sku(sku_id: int, payload: SKUUpdate, db: Session = Depends(get_db)):
    sku = db.get(SKU, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(sku, k, v)
    db.commit(); db.refresh(sku)
    return sku

@router.delete("/{sku_id}", status_code=204)
def delete_sku(sku_id: int, db: Session = Depends(get_db)):
    sku = db.get(SKU, sku_id)
    if not sku:
        raise HTTPException(status_code=404, detail="SKU not found")
    db.delete(sku); db.commit()
    return None
