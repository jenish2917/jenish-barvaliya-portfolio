"""
RSS News Service - Unlimited news fetching from RSS feeds
No API keys required, truly unlimited access to global news
"""

import feedparser
import requests
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import json
import hashlib
from urllib.parse import urljoin, urlparse
import time
import random

class RSSNewsService:
    """Enhanced RSS news service for global news aggregation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Major international RSS feeds - focusing on influential/resource-rich/populated countries
        self.rss_feeds = {
            # United States (Superpower)
            'us': {
                'cnn': 'http://rss.cnn.com/rss/edition.rss',
                'nytimes': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.rss',
                'washington_post': 'https://feeds.washingtonpost.com/rss/national',
                'reuters_us': 'https://feeds.reuters.com/reuters/USdomesticNews',
                'ap_news': 'https://feeds.apnews.com/rss/apf-topnews',
                'bloomberg': 'https://feeds.bloomberg.com/politics/news.rss'
            },
            
            # China (Most populated, economic powerhouse)
            'cn': {
                'xinhua': 'http://www.xinhuanet.com/english/rss/worldrss.xml',
                'cgtn': 'https://www.cgtn.com/subscribe/rss/section/world.xml',
                'china_daily': 'http://www.chinadaily.com.cn/rss/world_rss.xml'
            },
            
            # India (Most populated democracy, emerging superpower)
            'in': {
                'times_of_india': 'https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
                'ndtv': 'https://feeds.feedburner.com/ndtvnews-top-stories',
                'hindustan_times': 'https://www.hindustantimes.com/feeds/rss/india-news/index.xml',
                'indian_express': 'https://indianexpress.com/section/india/feed/'
            },
            
            # European Union (Economic powerhouse)
            'eu': {
                'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
                'euronews': 'https://feeds.feedburner.com/euronews/en/home',
                'dw': 'https://rss.dw.com/rdf/rss-en-all',
                'france24': 'https://www.france24.com/en/rss',
                'rt': 'https://www.rt.com/rss/'
            },
            
            # Russia (Resource-rich, major influence)
            'ru': {
                'tass': 'https://tass.com/rss/v2.xml',
                'sputnik': 'https://sputniknews.com/export/rss2/archive/index.xml'
            },
            
            # Japan (Tech powerhouse, major economy)
            'jp': {
                'nhk': 'https://www3.nhk.or.jp/rss/news/cat0.xml',
                'japan_times': 'https://www.japantimes.co.jp/feed/'
            },
            
            # Brazil (Largest Latin American economy)
            'br': {
                'folha': 'https://feeds.folha.uol.com.br/folha/brasil/rss091.xml'
            },
            
            # Middle East (Resource-rich region)
            'me': {
                'al_jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
                'al_arabiya': 'https://english.alarabiya.net/en.rss'
            },
            
            # Global/International
            'global': {
                'reuters_world': 'https://feeds.reuters.com/reuters/worldNews',
                'ap_world': 'https://feeds.apnews.com/rss/apf-worldnews',
                'un_news': 'https://news.un.org/feed/subscribe/en/news/all/rss.xml'
            }
        }
        
        # Cache for avoiding duplicate articles
        self.article_cache = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def fetch_global_news(self, max_articles_per_region: int = 5, max_total_articles: int = 50) -> List[Dict]:
        """
        Fetch news from major global sources, prioritizing influential countries
        
        Args:
            max_articles_per_region: Maximum articles per region
            max_total_articles: Maximum total articles to return
            
        Returns:
            List of news articles with metadata
        """
        all_articles = []
        
        # Priority order: US, China, India, EU, then others
        priority_regions = ['us', 'cn', 'in', 'eu', 'global', 'me', 'jp', 'ru', 'br']
        
        for region in priority_regions:
            if len(all_articles) >= max_total_articles:
                break
                
            region_articles = self._fetch_region_news(region, max_articles_per_region)
            all_articles.extend(region_articles)
            
            # Rate limiting - be respectful to RSS feeds
            time.sleep(random.uniform(0.5, 1.0))
        
        # Sort by publish date (most recent first) and remove duplicates
        unique_articles = self._deduplicate_articles(all_articles)
        sorted_articles = sorted(unique_articles, key=lambda x: x.get('published_date', datetime.now()), reverse=True)
        
        return sorted_articles[:max_total_articles]
    
    def _fetch_region_news(self, region: str, max_articles: int) -> List[Dict]:
        """Fetch news from a specific region"""
        region_articles = []
        
        if region not in self.rss_feeds:
            self.logger.warning(f"Unknown region: {region}")
            return region_articles
        
        for source_name, feed_url in self.rss_feeds[region].items():
            try:
                self.logger.info(f"Fetching from {source_name} ({region})")
                
                # Fetch and parse RSS feed
                response = self.session.get(feed_url, timeout=10)
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                
                if feed.bozo:
                    self.logger.warning(f"Feed parsing issues for {source_name}: {feed.bozo_exception}")
                    continue
                
                # Process entries
                for entry in feed.entries[:max_articles]:
                    article = self._parse_rss_entry(entry, source_name, region)
                    if article and self._is_article_valid(article):
                        region_articles.append(article)
                        
                        if len(region_articles) >= max_articles:
                            break
                
                # Rate limiting
                time.sleep(random.uniform(0.2, 0.5))
                
            except Exception as e:
                self.logger.error(f"Error fetching from {source_name}: {e}")
                continue
        
        return region_articles
    
    def _parse_rss_entry(self, entry, source_name: str, region: str) -> Optional[Dict]:
        """Parse RSS entry into standardized article format"""
        try:
            # Extract publish date
            published_date = datetime.now()
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published_date = datetime(*entry.updated_parsed[:6])
            
            # Get content
            content = ""
            if hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description
            elif hasattr(entry, 'content'):
                content = entry.content[0].value if isinstance(entry.content, list) else str(entry.content)
            
            # Clean HTML tags from content
            import re
            content = re.sub(r'<[^>]+>', '', content)
            content = content.strip()
            
            article = {
                'title': getattr(entry, 'title', 'No Title'),
                'content': content,
                'url': getattr(entry, 'link', ''),
                'published_date': published_date,
                'source': source_name,
                'region': region,
                'author': getattr(entry, 'author', 'Unknown'),
                'category': self._infer_category(entry.title + " " + content),
                'language': 'en',  # Most feeds are in English
                'id': hashlib.md5((getattr(entry, 'link', '') + getattr(entry, 'title', '')).encode()).hexdigest()
            }
            
            return article
            
        except Exception as e:
            self.logger.error(f"Error parsing RSS entry: {e}")
            return None
    
    def _infer_category(self, text: str) -> str:
        """Infer article category based on content"""
        text_lower = text.lower()
        
        business_keywords = ['economy', 'market', 'stock', 'business', 'finance', 'trade', 'company', 'corporate']
        tech_keywords = ['technology', 'tech', 'ai', 'artificial intelligence', 'software', 'digital', 'cyber']
        politics_keywords = ['politics', 'government', 'election', 'policy', 'minister', 'president', 'parliament']
        health_keywords = ['health', 'medical', 'hospital', 'disease', 'medicine', 'covid', 'vaccine']
        sports_keywords = ['sports', 'football', 'soccer', 'basketball', 'olympics', 'championship', 'game']
        
        if any(keyword in text_lower for keyword in business_keywords):
            return 'business'
        elif any(keyword in text_lower for keyword in tech_keywords):
            return 'technology'
        elif any(keyword in text_lower for keyword in politics_keywords):
            return 'politics'
        elif any(keyword in text_lower for keyword in health_keywords):
            return 'health'
        elif any(keyword in text_lower for keyword in sports_keywords):
            return 'sports'
        else:
            return 'general'
    
    def _is_article_valid(self, article: Dict) -> bool:
        """Validate article quality and relevance"""
        # Check for minimum content length
        if len(article.get('content', '')) < 50:
            return False
        
        # Check for duplicate (based on title similarity)
        article_id = article.get('id', '')
        if article_id in self.article_cache:
            return False
        
        self.article_cache.add(article_id)
        
        # Check publish date (only recent articles - last 3 days)
        if article.get('published_date'):
            days_old = (datetime.now() - article['published_date']).days
            if days_old > 3:
                return False
        
        return True
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title = article.get('title', '').lower().strip()
            # Create a simplified version for duplicate detection
            title_key = ''.join(char for char in title if char.isalnum())
            
            if title_key not in seen_titles and len(title_key) > 10:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        return unique_articles
    
    def get_trending_topics(self, articles: List[Dict]) -> List[str]:
        """Extract trending topics from articles"""
        from collections import Counter
        import re
        
        # Extract keywords from titles and content
        all_text = " ".join([
            article.get('title', '') + " " + article.get('content', '')
            for article in articles
        ]).lower()
        
        # Simple keyword extraction (you could use more sophisticated NLP)
        words = re.findall(r'\b[a-z]{4,}\b', all_text)
        
        # Filter out common words
        stop_words = {'that', 'this', 'with', 'from', 'they', 'have', 'will', 'been', 'said', 'would', 'their', 'were', 'what', 'more', 'could', 'about', 'after', 'first', 'time', 'very', 'when', 'much', 'than', 'some', 'into', 'only', 'know', 'just', 'also', 'other', 'many'}
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 4]
        
        # Get most common words
        word_counts = Counter(filtered_words)
        trending = [word for word, count in word_counts.most_common(10) if count > 2]
        
        return trending
