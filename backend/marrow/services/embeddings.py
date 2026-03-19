"""Embedding generation via OpenAI."""

from openai import AsyncOpenAI

from marrow.config import get_settings

# OpenAI text-embedding-3-small dimension
EMBEDDING_DIM = 1536


async def get_embedding(text: str) -> list[float]:
    """Generate embedding for text using OpenAI."""
    settings = get_settings()
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding
