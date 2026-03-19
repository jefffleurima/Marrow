"""Marrow API - Entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from marrow.api.routes import apps, memory
from marrow.db import close_db, get_pool, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle: startup and shutdown."""
    pool = await get_pool()
    app.state.pool = pool
    await init_db(pool)
    yield
    await close_db(pool)


app = FastAPI(
    title="Marrow",
    description="AI Memory Infrastructure — Store, recall, forget. The memory layer for AI.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"persistAuthorization": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apps.router, prefix="/v1")
app.include_router(memory.router, prefix="/v1")


# Add API key auth to OpenAPI so "Authorize" button appears in /docs
def custom_openapi():
    from fastapi.openapi.utils import get_openapi

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"}
    }
    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    # POST /v1/apps is public - no auth required
    if "/v1/apps" in openapi_schema.get("paths", {}):
        openapi_schema["paths"]["/v1/apps"]["post"]["security"] = []
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
