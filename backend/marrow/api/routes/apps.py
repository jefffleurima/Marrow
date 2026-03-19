"""App registration - public endpoint for hosted API key creation."""

import secrets

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from marrow.api.deps import get_pool
from marrow.auth import hash_api_key

router = APIRouter(prefix="/apps", tags=["apps"])


class CreateAppRequest(BaseModel):
    name: str = "default"


@router.post("")
async def create_app(
    body: CreateAppRequest = CreateAppRequest(),
    pool=Depends(get_pool),
):
    """
    Create an app and get an API key. No auth required.
    Use this key for all memory operations (store, recall, update, forget).
    Store the key securely—it won't be shown again.
    """
    name = (body.name or "default")[:255] or "default"

    api_key = f"marrow_{secrets.token_urlsafe(32)}"
    key_hash = hash_api_key(api_key)

    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO apps (name, api_key_hash) VALUES ($1, $2)",
            name,
            key_hash,
        )

    return {
        "api_key": api_key,
        "message": "Store this key securely. It won't be shown again.",
    }
