import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BoxCreate(BaseModel):
    label: Optional[str] = None


class BoxOut(BaseModel):
    id: uuid.UUID
    token: str
    label: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    name: str


class ItemOut(BaseModel):
    id: uuid.UUID
    box_id: uuid.UUID
    name: str
    created_at: datetime
    removed_at: Optional[datetime]

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    item_id: uuid.UUID
    item_name: str
    box_id: uuid.UUID
    box_token: str
    box_label: Optional[str]
    score: float
