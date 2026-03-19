"""Application configuration."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Load .env from backend directory (works when run from project root or backend)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path, override=True)


@dataclass
class Settings:
    """Marrow API settings."""

    database_url: str
    openai_api_key: str
    marrow_dev_api_key: str


@lru_cache
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings(
        database_url=os.environ.get("DATABASE_URL", ""),
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        marrow_dev_api_key=os.environ.get("MARROW_DEV_API_KEY", ""),
    )
