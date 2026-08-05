from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from nanoid import generate

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/boxes", tags=["boxes"])

TOKEN_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


@router.post("", response_model=schemas.BoxOut)
def create_box(payload: schemas.BoxCreate, db: Session = Depends(get_db)):
    box = models.Box(
        token=generate(alphabet=TOKEN_ALPHABET, size=8),
        label=payload.label,
    )
    db.add(box)
    db.commit()
    db.refresh(box)
    return box


@router.get("/{token}", response_model=schemas.BoxOut)
def get_box(token: str, db: Session = Depends(get_db)):
    box = db.query(models.Box).filter(models.Box.token == token).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
    return box


@router.get("/{token}/items", response_model=list[schemas.ItemOut])
def list_items(token: str, db: Session = Depends(get_db)):
    box = db.query(models.Box).filter(models.Box.token == token).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
    return (
        db.query(models.Item)
        .filter(models.Item.box_id == box.id, models.Item.removed_at.is_(None))
        .order_by(models.Item.created_at.desc())
        .all()
    )
@router.patch("/{token}", response_model=schemas.BoxOut)
def rename_box(token: str, payload: schemas.BoxUpdate, db: Session = Depends(get_db)):
    box = db.query(models.Box).filter(models.Box.token == token).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")
    box.label = payload.label
    db.commit()
    db.refresh(box)
    return box