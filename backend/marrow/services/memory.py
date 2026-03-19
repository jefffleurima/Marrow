"""Memory service: store, recall, forget, update."""

import json
from uuid import UUID

import asyncpg
from pgvector.asyncpg import register_vector

from marrow.models import StoreMemoryResponse
from marrow.services.embeddings import get_embedding


async def store_memory(
    pool: asyncpg.Pool,
    app_id: UUID,
    user_id: str,
    content: str,
    metadata: dict,
) -> StoreMemoryResponse:
    """Store a new memory."""
    embedding = await get_embedding(content)

    async with pool.acquire() as conn:
        await register_vector(conn)
        row = await conn.fetchrow(
            """
            INSERT INTO memories (app_id, user_id, content, embedding, metadata)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, user_id, content, metadata, created_at
            """,
            app_id,
            user_id,
            content,
            embedding,
            json.dumps(metadata or {}),
        )

    meta = row["metadata"]
    if isinstance(meta, str):
        meta = json.loads(meta) if meta else {}
    meta = meta or {}

    return StoreMemoryResponse(
        id=str(row["id"]),
        user_id=row["user_id"],
        content=row["content"],
        metadata=meta,
        created_at=row["created_at"],
    )


async def recall_memories(
    pool: asyncpg.Pool,
    app_id: UUID,
    user_id: str,
    query: str,
    limit: int = 10,
) -> list[StoreMemoryResponse]:
    """Recall relevant memories via semantic search."""
    query_embedding = await get_embedding(query)

    async with pool.acquire() as conn:
        await register_vector(conn)
        rows = await conn.fetch(
            """
            SELECT id, user_id, content, metadata, created_at,
                   1 - (embedding <=> $1) AS similarity
            FROM memories
            WHERE app_id = $2 AND user_id = $3 AND embedding IS NOT NULL
            ORDER BY embedding <=> $1
            LIMIT $4
            """,
            query_embedding,
            app_id,
            user_id,
            limit,
        )

    def _parse_meta(m):
        if isinstance(m, str):
            return json.loads(m) if m else {}
        return m or {}

    return [
        StoreMemoryResponse(
            id=str(r["id"]),
            user_id=r["user_id"],
            content=r["content"],
            metadata=_parse_meta(r["metadata"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


async def update_memory(
    pool: asyncpg.Pool,
    app_id: UUID,
    user_id: str,
    memory_id: str,
    content: str,
) -> StoreMemoryResponse | None:
    """Update an existing memory."""
    embedding = await get_embedding(content)

    async with pool.acquire() as conn:
        await register_vector(conn)
        row = await conn.fetchrow(
            """
            UPDATE memories
            SET content = $1, embedding = $2
            WHERE id = $3 AND app_id = $4 AND user_id = $5
            RETURNING id, user_id, content, metadata, created_at
            """,
            content,
            embedding,
            UUID(memory_id),
            app_id,
            user_id,
        )

    if not row:
        return None

    meta = row["metadata"]
    if isinstance(meta, str):
        meta = json.loads(meta) if meta else {}
    meta = meta or {}

    return StoreMemoryResponse(
        id=str(row["id"]),
        user_id=row["user_id"],
        content=row["content"],
        metadata=meta,
        created_at=row["created_at"],
    )


async def forget_memory(
    pool: asyncpg.Pool,
    app_id: UUID,
    user_id: str,
    memory_id: str,
) -> bool:
    """Delete a memory."""
    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE FROM memories
            WHERE id = $1 AND app_id = $2 AND user_id = $3
            """,
            UUID(memory_id),
            app_id,
            user_id,
        )

    return result == "DELETE 1"
