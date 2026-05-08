from collections.abc import Sequence

from sqlalchemy import desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news import News
from app.scrapers.g1 import scrape_g1_tech


async def collect_news(session: AsyncSession) -> int:
    scraped_items = await scrape_g1_tech(limit=20)
    if not scraped_items:
        return 0

    stmt = insert(News).values(scraped_items)
    stmt = stmt.on_conflict_do_nothing(index_elements=[News.url])
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount or 0


async def list_news(session: AsyncSession, limit: int = 50, offset: int = 0) -> Sequence[News]:
    stmt = select(News).order_by(desc(News.created_at)).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()
