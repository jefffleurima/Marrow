-- Marrow: AI Memory Infrastructure
-- Initial schema for Supabase (Postgres + pgvector)

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Apps: developer applications with their own memory namespace
CREATE TABLE apps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    api_key_hash TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Memories: app-scoped, user-scoped memory storage
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    app_id UUID NOT NULL REFERENCES apps(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small dimension
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for fast lookups
CREATE INDEX idx_memories_app_user ON memories(app_id, user_id);
CREATE INDEX idx_memories_created_at ON memories(created_at DESC);

-- Vector similarity search index (HNSW - no training required, good for MVP)
CREATE INDEX idx_memories_embedding ON memories 
    USING hnsw (embedding vector_cosine_ops);

-- Optional: GIN index for metadata JSONB queries
CREATE INDEX idx_memories_metadata ON memories USING gin(metadata);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER memories_updated_at
    BEFORE UPDATE ON memories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Seed a dev app (run manually or via dashboard)
-- INSERT INTO apps (name, api_key_hash) VALUES ('dev', 'hash_of_your_api_key');
