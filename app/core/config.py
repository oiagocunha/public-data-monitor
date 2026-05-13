import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/public_data",
)

# Opcional: habilita DELETE /news/{id} quando definido (header X-API-Key deve coincidir).
NEWS_DELETE_API_KEY: str | None = os.getenv("NEWS_DELETE_API_KEY") or None
