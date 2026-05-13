import pytest

import app.core.config as core_config
from app.api import deps


@pytest.mark.asyncio
async def test_require_delete_news_api_key_rejects_when_not_configured(monkeypatch):
    monkeypatch.setattr(core_config, "NEWS_DELETE_API_KEY", None)

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await deps.require_delete_news_api_key(api_key="anything")

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_require_delete_news_api_key_rejects_invalid_key(monkeypatch):
    monkeypatch.setattr(core_config, "NEWS_DELETE_API_KEY", "secret")

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await deps.require_delete_news_api_key(api_key="wrong")

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_require_delete_news_api_key_accepts_valid(monkeypatch):
    monkeypatch.setattr(core_config, "NEWS_DELETE_API_KEY", "secret")
    await deps.require_delete_news_api_key(api_key="secret")
