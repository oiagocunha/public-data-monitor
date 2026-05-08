from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str
    url: str
    source: str
    published_at: datetime | None


class NewsPage(BaseModel):
    items: list[NewsRead]
    limit: int
    offset: int
    total: int
    has_next: bool
