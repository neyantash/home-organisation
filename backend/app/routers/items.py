from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.embeddings import embed_text

router = APIRouter(tags=["items"])


@router.post("/boxes/{token}/items", response_model=schemas.ItemOut)
def add_item(token: str, payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    box = db.query(models.Box).filter(models.Box.token == token).first()
    if not box:
        raise HTTPException(status_code=404, detail="Box not found")

    vector = embed_text(payload.name)
    item = models.Item(box_id=box.id, name=payload.name, embedding=vector)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/items/{item_id}/remove", response_model=schemas.ItemOut)
def remove_item(item_id: str, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.removed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item
