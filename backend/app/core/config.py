import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr


load_dotenv()


class Settings(BaseModel):
    openrouter_api_key: SecretStr
    openrouter_model: str


@lru_cache
def get_settings() -> Settings:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY belum tersedia di file .env")

    return Settings(
        openrouter_api_key=SecretStr(api_key),
        openrouter_model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    )