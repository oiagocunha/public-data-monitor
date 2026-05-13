from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

import app.core.config as core_config

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_delete_news_api_key(
    api_key: str | None = Depends(_api_key_header),
) -> None:
    expected = core_config.NEWS_DELETE_API_KEY
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Exclusao de noticias nao esta habilitada neste ambiente "
                "(defina NEWS_DELETE_API_KEY)."
            ),
        )
    if not api_key or api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key obrigatoria ou invalida (header X-API-Key).",
        )
