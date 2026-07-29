from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app import models, schemas
from app.embeddings import embed_text

router = APIRouter(tags=["search"])


@router.get("/search", response_model=list[schemas.SearchResult])
def search_items(q: str = Query(..., min_length=1), limit: int = 8, db: Session = Depends(get_db)):
    query_vector = embed_text(q)
    distance = models.Item.embedding.cosine_distance(query_vector)
    stmt = (
        select(models.Item, models.Box, distance.label("distance"))
        .join(models.Box, models.Item.box_id == models.Box.id)
        .where(models.Item.removed_at.is_(None))
        .order_by(distance)
        .limit(limit)
    )

    rows = db.execute(stmt).all()
    results = []
    for item, box, dist in rows:
        score = round(1 - dist, 3)
        if score < 0.25:
            break
        results.append(
            schemas.SearchResult(
                item_id=item.id,
                item_name=item.name,
                box_id=box.id,
                box_token=box.token,
                box_label=box.label,
                score=round(1 - dist, 3),
            )
        )
    return results
