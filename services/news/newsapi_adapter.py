"""
NewsAPI Adapter (FREE)
======================
100 requests/day on free tier.
To upgrade: replace with Refinitiv adapter
"""

import requests
from services.base import NewsDataProvider
import config


class NewsAPIAdapter(NewsDataProvider):

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self):
        self.api_key = config.NEWS_API_KEY

    def get_market_news(self, query: str = "stock market India", limit: int = 10) -> list:
        try:
            if not self.api_key:
                return self._get_rss_news(query, limit)

            r = requests.get(
                f"{self.BASE_URL}/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": limit,
                    "apiKey": self.api_key,
                },
                timeout=5,
            )
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                return [
                    {
                        "title": a["title"],
                        "description": a.get("description", ""),
                        "url": a["url"],
                        "source": a["source"]["name"],
                        "published_at": a["publishedAt"],
                        "image": a.get("urlToImage", ""),
                    }
                    for a in articles if a.get("title")
                ]
            return self._get_rss_news(query, limit)
        except Exception as e:
            return self._get_rss_news(query, limit)

    def get_stock_news(self, symbol: str, limit: int = 5) -> list:
        company_name = symbol.replace(".NS", "").replace(".BO", "")
        return self.get_market_news(query=f"{company_name} stock", limit=limit)

    def _get_rss_news(self, query: str, limit: int) -> list:
        """Fallback: Economic Times RSS — no API key needed"""
        try:
            import xml.etree.ElementTree as ET
            url = "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
            r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            root = ET.fromstring(r.content)
            items = root.findall(".//item")
            news = []
            for item in items[:limit]:
                title = item.findtext("title", "")
                desc = item.findtext("description", "")
                link = item.findtext("link", "")
                pub = item.findtext("pubDate", "")
                news.append({
                    "title": title,
                    "description": desc,
                    "url": link,
                    "source": "Economic Times",
                    "published_at": pub,
                    "image": "",
                })
            return news
        except:
            return []


# ============================================
# PAID ADAPTER — Refinitiv (~$500/month)
# Real-time financial news with NLP tags
# ============================================

# import refinitiv.data as rd, os
# from services.base import NewsDataProvider
#
# class RefinitivAdapter(NewsDataProvider):
#
#     def __init__(self):
#         rd.open_session(app_key=os.getenv("REFINITIV_API_KEY"))
#
#     def get_market_news(self, query: str, limit: int = 10) -> list:
#         headlines = rd.news.get_headlines(query=query, count=limit)
#         # process headlines...
