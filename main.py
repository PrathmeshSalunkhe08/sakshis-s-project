import asyncio
import sys
import httpx

from news_api import fetch_multi_source_urls
from article_fetcher import fetch_article
from models import ArticleInput
from llm_analyzer import analyze_article
from output import save_insights


async def main():
    # User's topic keyword
    topic = "artificial intelligence"

    print(f"1. Fetching topic '{topic}' concurrently from DIFFERENT News APIs (GNews, NewsData, Currents)...")

    # 1. Hit multiple News APIs concurrently using asyncio.gather()
    urls = await fetch_multi_source_urls(topic)

    # Add an invalid test URL for error handling requirement
    urls.append("https://invalid-url-example-12345.com")

    print(f"\nFound {len(urls)} article URLs from different sources:")
    for i, url in enumerate(urls, 1):
        print(f"  [{i}] {url}")

    print("\n2. Fetching article content concurrently using asyncio.gather()...")

    # 2. Fetch full article content concurrently from all URLs
    async with httpx.AsyncClient() as client:
        tasks = [fetch_article(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # 3. Validate fetched results using Pydantic ArticleInput model
    print("\n3. Validating fetched data with Pydantic...")
    validated_articles = []
    for item in results:
        article = ArticleInput(
            url=item["url"],
            content=item["content"],
            fetch_status=item["fetch_status"]
        )
        validated_articles.append(article)

    # 4. LLM Analysis for successful articles using LangChain
    print("\n4. Analyzing articles with LLM...")
    insights = []
    for article in validated_articles:
        if article.fetch_status == "success" and article.content.strip():
            print(f"Analyzing: {article.url}")
            try:
                insight = analyze_article(article.content)
                insights.append(insight)
            except Exception as e:
                insights.append({
                    "url": article.url,
                    "fetch_status": "failed",
                    "error": f"LLM Error: {str(e)}"
                })
        else:
            print(f"Skipping failed article: {article.url}")
            insights.append({
                "url": article.url,
                "fetch_status": article.fetch_status,
                "error": "Failed to fetch content"
            })

    # 5. Export results to final_insights.json
    print("\n5. Saving results to final_insights.json...")
    save_insights(insights)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())