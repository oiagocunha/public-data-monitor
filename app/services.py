from collections.abc import Sequence
import logging

from sqlalchemy import delete, desc, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news import News
from app.scrapers.g1 import scrape_g1_tech

logger = logging.getLogger(__name__)


async def collect_news(session: AsyncSession) -> int:
    logger.info("Iniciando coleta de noticias")
    scraped_items = await scrape_g1_tech(limit=20)
    if not scraped_items:
        logger.info("Nenhum item coletado")
        return 0

    stmt = insert(News).values(scraped_items)
    stmt = stmt.on_conflict_do_nothing(index_elements=[News.url])
    result = await session.execute(stmt)
    await session.commit()
    inserted = result.rowcount or 0
    logger.info("Coleta concluida com %s novos itens", inserted)
    return inserted


async def list_news(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[News]:
    stmt = select(News).order_by(desc(News.created_at)).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


async def count_news(session: AsyncSession) -> int:
    stmt = select(func.count(News.id))
    result = await session.execute(stmt)
    return int(result.scalar_one())


async def get_news_by_id(session: AsyncSession, news_id: int) -> News | None:
    stmt = select(News).where(News.id == news_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_news_by_id(session: AsyncSession, news_id: int) -> bool:
    stmt = delete(News).where(News.id == news_id)
    result = await session.execute(stmt)
    await session.commit()
    return (result.rowcount or 0) > 0
