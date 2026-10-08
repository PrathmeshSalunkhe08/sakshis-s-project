import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CURRENTS_API_KEY = os.getenv("Current_NEWS_API")


async def fetch_gnews(client, query):
    """1. Fetch article URLs from GNews API."""
    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&max=2&apikey={GNEWS_API_KEY}"
    try:
        res = await client.get(url, timeout=10.0)
        data = res.json()
        articles = data.get("articles", [])
        return [a["url"] for a in articles if "url" in a]
    except Exception:
        return []


async def fetch_newsdata(client, query):
    """2. Fetch article URLs from NewsData.io API."""
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={query}&language=en"
    try:
        res = await client.get(url, timeout=10.0)
        data = res.json()
        results = data.get("results", [])
        return [a["link"] for a in results[:2] if "link" in a]
    except Exception:
        return []


async def fetch_currents(client, query):
    """3. Fetch article URLs from Currents News API."""
    url = f"https://api.currentsapi.services/v1/search?apiKey={CURRENTS_API_KEY}&keywords={query}"
    try:
        res = await client.get(url, timeout=10.0)
        data = res.json()
        news = data.get("news", [])
        return [a["url"] for a in news[:2] if "url" in a]
    except Exception:
        return []


async def fetch_multi_source_urls(query):
    """Hits 3 DIFFERENT News APIs concurrently using asyncio.gather()."""
    async with httpx.AsyncClient() as client:
        # Fire requests to all 3 News APIs at the same time concurrently!
        tasks = [
            fetch_gnews(client, query),
            fetch_newsdata(client, query),
            fetch_currents(client, query)
        ]
        results = await asyncio.gather(*tasks)

    # Combine URLs returned from GNews, NewsData, and Currents News
    all_urls = []
    for url_list in results:
        all_urls.extend(url_list)

    return all_urls