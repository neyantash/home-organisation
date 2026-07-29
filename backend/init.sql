CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS boxes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token VARCHAR(16) UNIQUE NOT NULL,
    label TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    box_id UUID NOT NULL REFERENCES boxes(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    aliases TEXT[],
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT now(),
    removed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_items_box_id ON items(box_id);
CREATE INDEX IF NOT EXISTS idx_items_not_removed ON items(box_id) WHERE removed_at IS NULL;
