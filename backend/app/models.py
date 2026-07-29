import uuid
from sqlalchemy import Column, Text, ForeignKey, ARRAY, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.database import Base


class Box(Base):
    __tablename__ = "boxes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(Text, unique=True, nullable=False)
    label = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    box_id = Column(UUID(as_uuid=True), ForeignKey("boxes.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    aliases = Column(ARRAY(Text))
    embedding = Column(Vector(1536))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    removed_at = Column(TIMESTAMP(timezone=True), nullable=True)
