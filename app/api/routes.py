from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal
from app.schemas.news import NewsRead
from app.services import collect_news, list_news

router = APIRouter()


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/collect")
async def collect(session: AsyncSession = Depends(get_session)) -> dict[str, int]:
    inserted = await collect_news(session)
    return {"inserted": inserted}


@router.get("/news", response_model=list[NewsRead])
async def get_news(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> list[NewsRead]:
    news = await list_news(session=session, limit=limit, offset=offset)
    return list(news)
