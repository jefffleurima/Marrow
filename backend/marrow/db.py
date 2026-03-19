"""Database connection and pool."""

import asyncpg
from asyncpg.pool import Pool

from marrow.config import get_settings


async def get_pool() -> Pool:
    """Create and return a connection pool."""
    settings = get_settings()
    if not settings.database_url:
        raise ValueError(
            "DATABASE_URL is not set. Add your Supabase connection string to backend/.env"
        )
    return await asyncpg.create_pool(
        settings.database_url,
        min_size=2,
        max_size=10,
        command_timeout=60,
    )


async def init_db(pool: Pool) -> None:
    """Verify database connection."""
    async with pool.acquire() as conn:
        await conn.fetchval("SELECT 1")


async def close_db(pool: Pool) -> None:
    """Close the connection pool."""
    await pool.close()
