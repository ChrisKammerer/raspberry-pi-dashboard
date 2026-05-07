import os
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

from backend.src.db_utils import init_db


class BaseFetcher:
    """Shared fetcher functionality for all API fetchers."""

    def __init__(self) -> None:
        self.env_file = f".env.{os.getenv('APP_ENV', 'dev')}"
        self.load_environment()

    def load_environment(self) -> None:
        load_dotenv(self.env_file)

    def get_env(self, name: str, default=None, required: bool = False):
        value = os.getenv(name, default)
        if required and value is None:
            raise RuntimeError(f"Missing required environment variable: {name}")
        return value

    @staticmethod
    def init_db() -> None:
        init_db()

    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)

    @classmethod
    def expires_at(cls, minutes: int) -> datetime:
        return cls.now_utc() + timedelta(minutes=minutes)
