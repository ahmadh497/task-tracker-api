# app/core/config.py
# Loads environment variables (from .env, if present) and exposes
# them as a simple, typed settings object used across the app.

import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root, if one exists.
# This does nothing (and doesn't error) if .env is missing, which is
# fine for environments where variables are set another way (CI, shell, etc.)
load_dotenv()


class Settings:
    """
    Minimal application settings loaded from environment variables.

    Values fall back to sensible defaults so the app can still start
    if no .env file is present.
    """

    def __init__(self) -> None:
        self.app_env: str = os.getenv("APP_ENV", "development")
        self.port: int = int(os.getenv("PORT", "8000"))


# Single shared settings instance, imported elsewhere as `from app.core.config import settings`
settings = Settings()