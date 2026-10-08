import httpx


async def fetch_article(client, url):
    """Fetches article content asynchronously using httpx."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = await client.get(url, headers=headers, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
        return {
            "url": url,
            "content": response.text,
            "fetch_status": "success"
        }
    except httpx.TimeoutException:
        return {
            "url": url,
            "content": "",
            "fetch_status": "failed",
            "error": "Request timed out"
        }
    except httpx.HTTPError:
        return {
            "url": url,
            "content": "",
            "fetch_status": "failed",
            "error": "HTTP error"
        }
    except Exception as e:
        return {
            "url": url,
            "content": "",
            "fetch_status": "failed",
            "error": str(e)
        }