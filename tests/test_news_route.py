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


@pytest.mark.asyncio
async def test_get_news_by_id_returns_item(monkeypatch):
    fake = SimpleNamespace(
        id=7,
        title="Titulo",
        summary="Resumo",
        url="https://example.com/news",
        source="g1",
        published_at=datetime.now(timezone.utc),
    )

    async def fake_get_news_by_id(session, news_id):  # noqa: ANN001
        assert news_id == 7
        return fake

    monkeypatch.setattr(routes, "get_news_by_id", fake_get_news_by_id)

    response = await routes.get_news_by_id_route(news_id=7, session=None)

    assert response.id == 7
    assert response.title == "Titulo"


@pytest.mark.asyncio
async def test_get_news_by_id_raises_when_missing(monkeypatch):
    async def fake_get_news_by_id(session, news_id):  # noqa: ANN001
        return None

    monkeypatch.setattr(routes, "get_news_by_id", fake_get_news_by_id)

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await routes.get_news_by_id_route(news_id=99, session=None)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_news_route_returns_204_when_deleted(monkeypatch):
    async def fake_delete(session, news_id):  # noqa: ANN001
        assert news_id == 3
        return True

    monkeypatch.setattr(routes, "delete_news_by_id", fake_delete)

    response = await routes.delete_news_route(news_id=3, session=None)

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_news_route_raises_when_not_found(monkeypatch):
    async def fake_delete(session, news_id):  # noqa: ANN001
        return False

    monkeypatch.setattr(routes, "delete_news_by_id", fake_delete)

    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        await routes.delete_news_route(news_id=99, session=None)

    assert exc_info.value.status_code == 404
