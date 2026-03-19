"""API key authentication."""

import hashlib
from uuid import UUID

import asyncpg


def hash_api_key(key: str) -> str:
    """Hash an API key for storage/lookup."""
    return hashlib.sha256(key.encode()).hexdigest()


def extract_api_key(authorization: str | None, x_api_key: str | None) -> str | None:
    """Extract API key from Authorization header or X-API-Key."""
    if x_api_key:
        return x_api_key.strip()
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:].strip()
    return None


async def get_app_id_from_key(pool: asyncpg.Pool, api_key: str) -> UUID | None:
    """Look up app_id by API key. Returns None if invalid."""
    key_hash = hash_api_key(api_key)
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id FROM apps WHERE api_key_hash = $1",
            key_hash,
        )
    return row["id"] if row else None


async def verify_api_key(
    pool: asyncpg.Pool,
    authorization: str | None,
    x_api_key: str | None,
) -> UUID | None:
    """Verify API key and return app_id."""
    key = extract_api_key(authorization, x_api_key)
    if not key:
        return None
    return await get_app_id_from_key(pool, key)
