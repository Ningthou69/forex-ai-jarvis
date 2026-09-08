import requests
from datetime import datetime, timedelta
from config import NEWS_API_KEY
import json

class GeopoliticalMonitor:
    """Monitors geopolitical events affecting forex markets"""
    
    def __init__(self):
        self.news_url = "https://newsapi.org/v2/everything"
        self.api_key = NEWS_API_KEY
        
        # Keywords that impact forex
        self.forex_keywords = [
            "forex market", "currency trading", "central bank",
            "Federal Reserve", "ECB", "Bank of Japan", "interest rates",
            "inflation", "GDP", "employment", "trade war", "sanctions",
            "geopolitical tensions", "economic crisis", "currency crisis",
            "monetary policy", "economic data"
        ]
        
        # Currency impact mapping
        self.currency_impact = {
            "USD": ["Federal Reserve", "US economy", "US inflation", "US employment"],
            "EUR": ["ECB", "European economy", "eurozone", "Europe"],
            "GBP": ["Bank of England", "UK economy", "Brexit", "UK inflation"],
            "JPY": ["Bank of Japan", "Japan economy", "BOJ", "Japanese"],
            "CNY": ["China economy", "Chinese", "PBoC", "trade war"],
        }
    
    def get_latest_news(self, keywords=None, hours=24):
        """Fetch latest news related to forex"""
        if keywords is None:
            keywords = self.forex_keywords
        
        from_date = datetime.utcnow() - timedelta(hours=hours)
        from_date_str = from_date.strftime("%Y-%m-%d")
        
        all_articles = []
        
        try:
            for keyword in keywords[:5]:  # Limit to 5 keywords per request
                params = {
                    "q": keyword,
                    "from": from_date_str,
                    "sortBy": "publishedAt",
                    "language": "en",
                    "apiKey": self.api_key
                }
                
                response = requests.get(self.news_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    all_articles.extend(data.get("articles", []))
            
            # Remove duplicates
            unique_articles = {}
            for article in all_articles:
                if article["title"] not in unique_articles:
                    unique_articles[article["title"]] = article
            
            return list(unique_articles.values())
        
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def analyze_impact(self, articles):
        """Analyze impact of news on forex pairs"""
        impact_analysis = {
            "USD": {"impact": 0, "events": []},
            "EUR": {"impact": 0, "events": []},
            "GBP": {"impact": 0, "events": []},
            "JPY": {"impact": 0, "events": []},
            "CNY": {"impact": 0, "events": []},
        }
        
        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            content = title + " " + description
            
            # Check impact on each currency
            for currency, keywords in self.currency_impact.items():
                for keyword in keywords:
                    if keyword.lower() in content:
                        # Determine if positive or negative
                        if any(word in content for word in ["crisis", "tension", "war", "collapse"]):
                            impact_analysis[currency]["impact"] -= 1
                        elif any(word in content for word in ["growth", "positive", "strong", "recovery"]):
                            impact_analysis[currency]["impact"] += 1
                        
                        impact_analysis[currency]["events"].append({
                            "title": article.get("title"),
                            "source": article.get("source", {}).get("name"),
                            "published_at": article.get("publishedAt"),
                            "url": article.get("url")
                        })
        
        return impact_analysis
    
    def get_geopolitical_summary(self):
        """Get complete geopolitical analysis"""
        articles = self.get_latest_news()
        impact = self.analyze_impact(articles)
        
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "articles_analyzed": len(articles),
            "currency_impacts": impact,
            "risk_level": self._calculate_risk_level(impact),
            "top_stories": self._get_top_stories(articles)
        }
        
        return summary
    
    def _calculate_risk_level(self, impact):
        """Calculate overall market risk level"""
        total_impact = sum(abs(data["impact"]) for data in impact.values())
        
        if total_impact > 10:
            return "HIGH"
        elif total_impact > 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_top_stories(self, articles, limit=5):
        """Get top stories by relevance"""
        return [
            {
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "url": article.get("url")
            }
            for article in articles[:limit]
        ]