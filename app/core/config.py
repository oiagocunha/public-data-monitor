import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/public_data",
)


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _normalize_database_url(raw_url: str) -> str:
    # Algumas plataformas ainda injetam postgres://, mas SQLAlchemy espera postgresql://
    normalized = raw_url.replace("postgres://", "postgresql://", 1)

    ssl_required = _is_truthy(os.getenv("DB_SSL_REQUIRE")) or _is_truthy(os.getenv("RENDER"))
    has_ssl_hint = "ssl=" in normalized or "sslmode=" in normalized
    if ssl_required and not has_ssl_hint:
        separator = "&" if "?" in normalized else "?"
        normalized = f"{normalized}{separator}ssl=require"
    return normalized


DATABASE_URL = _normalize_database_url(DATABASE_URL)

# Opcional: habilita DELETE /news/{id} quando definido (header X-API-Key deve coincidir).
NEWS_DELETE_API_KEY: str | None = os.getenv("NEWS_DELETE_API_KEY") or None
