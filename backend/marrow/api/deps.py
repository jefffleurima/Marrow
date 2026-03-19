"""FastAPI dependencies."""

from uuid import UUID

from fastapi import Depends, Header, HTTPException, Request

from marrow.auth import verify_api_key


async def get_pool(request: Request):
    """Get DB pool from app state."""
    return request.app.state.pool


async def get_app_id(
    request: Request,
    authorization: str | None = Header(None),
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> UUID:
    """Dependency: require valid API key, return app_id."""
    pool = request.app.state.pool
    app_id = await verify_api_key(pool, authorization, x_api_key)
    if not app_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Use X-API-Key header or Authorization: Bearer <key>",
        )
    return app_id
