"""Database models and schemas."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


# --- Request/Response Schemas ---


class StoreMemoryRequest(BaseModel):
    """Request to store a memory."""

    user_id: str = Field(..., min_length=1, max_length=256)
    content: str = Field(..., min_length=1, max_length=65536)
    metadata: dict[str, Any] = Field(default_factory=dict)


class StoreMemoryResponse(BaseModel):
    """Response after storing a memory."""

    id: str
    user_id: str
    content: str
    metadata: dict[str, Any]
    created_at: datetime


class RecallMemoryRequest(BaseModel):
    """Request to recall memories."""

    user_id: str = Field(..., min_length=1, max_length=256)
    query: str = Field(..., min_length=1, max_length=4096)
    limit: int = Field(default=10, ge=1, le=100)


class RecallMemoryResponse(BaseModel):
    """Response with recalled memories."""

    memories: list[StoreMemoryResponse]


class UpdateMemoryRequest(BaseModel):
    """Request to update a memory."""

    user_id: str = Field(..., min_length=1, max_length=256)
    content: str = Field(..., min_length=1, max_length=65536)


class ForgetMemoryRequest(BaseModel):
    """Request to forget (delete) a memory."""

    user_id: str = Field(..., min_length=1, max_length=256)
    memory_id: str = Field(..., min_length=1)
