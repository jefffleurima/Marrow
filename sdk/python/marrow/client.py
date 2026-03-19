"""Marrow API client."""

from typing import Any

import httpx


class MarrowError(Exception):
    """Raised when an API request fails."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class Marrow:
    """
    Marrow API client. Store, recall, update, and forget memories.

    Example:
        client = Marrow(api_key="marrow_...", base_url="https://your-api.up.railway.app")
        client.store("user_123", "Prefers window seats")
        memories = client.recall("user_123", "travel preferences")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:8000",
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
            timeout=60.0,
        )

    def _request(
        self,
        method: str,
        path: str,
        json: dict | None = None,
        params: dict | None = None,
    ) -> dict | list:
        response = self._client.request(method, path, json=json, params=params)
        if response.status_code >= 400:
            raise MarrowError(
                f"API error: {response.text or response.reason_phrase}",
                status_code=response.status_code,
            )
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()

    def store(
        self,
        user_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Store a memory. Returns the created memory with id, content, metadata, created_at.
        """
        return self._request(
            "POST",
            "/v1/memories",
            json={
                "user_id": user_id,
                "content": content,
                "metadata": metadata or {},
            },
        )

    def recall(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Recall relevant memories via semantic search. Returns a list of memories.
        """
        result = self._request(
            "POST",
            "/v1/memories/recall",
            json={
                "user_id": user_id,
                "query": query,
                "limit": limit,
            },
        )
        return result.get("memories", [])

    def update(
        self,
        user_id: str,
        memory_id: str,
        content: str,
    ) -> dict[str, Any]:
        """
        Update an existing memory. Returns the updated memory.
        """
        return self._request(
            "PATCH",
            f"/v1/memories/{memory_id}",
            json={"user_id": user_id, "content": content},
        )

    def forget(
        self,
        user_id: str,
        memory_id: str,
    ) -> bool:
        """
        Delete a memory. Returns True on success.
        """
        self._request(
            "DELETE",
            f"/v1/memories/{memory_id}",
            params={"user_id": user_id},
        )
        return True

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "Marrow":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
