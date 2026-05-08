from datetime import datetime
from email.utils import parsedate_to_datetime

import httpx
from bs4 import BeautifulSoup


async def scrape_g1_tech(limit: int = 20) -> list[dict]:
    url = "https://g1.globo.com/tecnologia/"

    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.select("a.feed-post-link")

    items: list[dict] = []
    for card in cards[:limit]:
        title = card.get_text(strip=True)
        link = card.get("href", "").strip()

        if not title or not link:
            continue

        date_str = card.get("data-publication")
        published_at = _parse_g1_date(date_str) if date_str else None

        items.append(
            {
                "title": title,
                "summary": title,
                "url": link,
                "source": "g1",
                "published_at": published_at,
            }
        )

    return items


def _parse_g1_date(date_str: str) -> datetime | None:
    try:
        return parsedate_to_datetime(date_str)
    except (TypeError, ValueError):
        return None
