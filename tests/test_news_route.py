from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.api import routes


@pytest.mark.asyncio
async def test_get_news_returns_pagination_metadata(monkeypatch):
    fake_items = [
        SimpleNamespace(
            id=1,
            title="Titulo",
            summary="Resumo",
            url="https://example.com/news",
            source="g1",
            published_at=datetime.now(timezone.utc),
        )
    ]

    async def fake_list_news(session, limit, offset):  # noqa: ANN001
        return fake_items

    async def fake_count_news(session):  # noqa: ANN001
        return 120

    monkeypatch.setattr(routes, "list_news", fake_list_news)
    monkeypatch.setattr(routes, "count_news", fake_count_news)

    response = await routes.get_news(limit=20, offset=0, session=None)

    assert response.limit == 20
    assert response.offset == 0
    assert response.total == 120
    assert response.has_next is True
    assert len(response.items) == 1
