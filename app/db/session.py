from sqlalchemy.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker[AsyncSession](engine, expire_on_commit=False)
