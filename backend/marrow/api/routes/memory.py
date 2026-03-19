"""Memory API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from marrow.api.deps import get_app_id, get_pool
from marrow.models import (
    RecallMemoryRequest,
    RecallMemoryResponse,
    StoreMemoryRequest,
    StoreMemoryResponse,
    UpdateMemoryRequest,
)
from marrow.services import memory as memory_service

router = APIRouter(prefix="/memories", tags=["memory"])


@router.post("", response_model=StoreMemoryResponse)
async def store_memory(
    body: StoreMemoryRequest,
    app_id: UUID = Depends(get_app_id),
    pool=Depends(get_pool),
):
    """Store a new memory."""
    return await memory_service.store_memory(
        pool=pool,
        app_id=app_id,
        user_id=body.user_id,
        content=body.content,
        metadata=body.metadata,
    )


@router.post("/recall", response_model=RecallMemoryResponse)
async def recall_memories(
    body: RecallMemoryRequest,
    app_id: UUID = Depends(get_app_id),
    pool=Depends(get_pool),
):
    """Recall relevant memories for a query."""
    memories = await memory_service.recall_memories(
        pool=pool,
        app_id=app_id,
        user_id=body.user_id,
        query=body.query,
        limit=body.limit,
    )
    return RecallMemoryResponse(memories=memories)


def _validate_memory_id(memory_id: str) -> None:
    """Raise 422 if memory_id is not a valid UUID."""
    try:
        UUID(memory_id)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="memory_id must be a valid UUID (e.g. from store or recall response)",
        )


@router.patch("/{memory_id}", response_model=StoreMemoryResponse)
async def update_memory(
    memory_id: str,
    body: UpdateMemoryRequest,
    app_id: UUID = Depends(get_app_id),
    pool=Depends(get_pool),
):
    """Update an existing memory."""
    _validate_memory_id(memory_id)
    result = await memory_service.update_memory(
        pool=pool,
        app_id=app_id,
        user_id=body.user_id,
        memory_id=memory_id,
        content=body.content,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Memory not found")
    return result


@router.delete("/{memory_id}")
async def forget_memory(
    memory_id: str,
    user_id: str,
    app_id: UUID = Depends(get_app_id),
    pool=Depends(get_pool),
):
    """Delete a memory."""
    _validate_memory_id(memory_id)
    deleted = await memory_service.forget_memory(
        pool=pool,
        app_id=app_id,
        user_id=user_id,
        memory_id=memory_id,
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"ok": True}
