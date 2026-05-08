from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Public Data Monitor", lifespan=lifespan)
app.include_router(router)
