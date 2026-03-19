#!/usr/bin/env python3
"""
Seed a dev app and print the API key.
Run once after migration. Add the printed key to your .env or use as X-API-Key.

Usage:
    python -m scripts.seed_app
"""

import asyncio
import secrets
import sys
from pathlib import Path

_backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_backend_dir))

# Load .env - try multiple paths (module vs cwd)
from dotenv import dotenv_values

_env_paths = [
    _backend_dir / ".env",
    Path.cwd() / ".env",
    Path.cwd() / "backend" / ".env",
]
_env = {}
for p in _env_paths:
    if p.exists():
        _env = dotenv_values(p)
        break

database_url = (_env.get("DATABASE_URL") or "").strip()
if not database_url:
    print("Error: DATABASE_URL is not set in backend/.env")
    print(f"  Checked: {[str(p) for p in _env_paths]}")
    sys.exit(1)

from marrow.auth import hash_api_key


async def main():
    """Create a dev app and print the API key."""
    import asyncpg

    api_key = f"marrow_{secrets.token_urlsafe(32)}"
    key_hash = hash_api_key(api_key)

    pool = await asyncpg.create_pool(database_url, min_size=1, max_size=2)
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO apps (name, api_key_hash) VALUES ('dev', $1)",
            key_hash,
        )

    await pool.close()

    print("Dev app created successfully!")
    print()
    print("Add this to your .env or use as X-API-Key header:")
    print()
    print(f"  {api_key}")
    print()
    print("This key will not be shown again. Store it securely.")


if __name__ == "__main__":
    asyncio.run(main())
