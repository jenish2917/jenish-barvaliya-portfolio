"""
RSS News Service
Fetches news from multiple RSS feeds without API limitations
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import random
from urllib.parse import urljoin, urlparse
import time

class RSSNewsService:
    """RSS-based news service for unlimited news access"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Major RSS feeds by category
        self.rss_feeds = {
            'technology': [
                'https://feeds.bbci.co.uk/news/technology/rss.xml',
                'https://rss.cnn.com/rss/edition.rss',
                'https://techcrunch.com/feed/',
                'https://www.theverge.com/rss/index.xml',
                'https://feeds.reuters.com/reuters/technologyNews',
            ],
            'business': [
                'https://feeds.bbci.co.uk/news/business/rss.xml',
                'https://rss.cnn.com/rss/money_latest.rss',
                'https://feeds.reuters.com/reuters/businessNews',
                'https://feeds.bloomberg.com/markets/news.rss',
            ],
            'entertainment': [
                'https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
                'https://rss.cnn.com/rss/edition_entertainment.rss',
                'https://feeds.reuters.com/reuters/entertainment',
            ],
            'sports': [
                'https://feeds.bbci.co.uk/sport/rss.xml',
                'https://rss.cnn.com/rss/edition_sport.rss',
                'https://feeds.reuters.com/reuters/sportsNews',
            ],
            'general': [
                'https://feeds.bbci.co.uk/news/rss.xml',
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.reuters.com/reuters/topNews',
                'https://feeds.npr.org/1001/rss.xml',
            ]
        }
        
        # Keywords that indicate engaging/trending content
        self.engaging_keywords = [
            'breaking', 'exclusive', 'reveals', 'shocking', 'amazing', 
            'incredible', 'revolutionary', 'breakthrough', 'huge', 'massive',
            'unprecedented', 'dramatic', 'explosive', 'controversial', 'viral'
        ]
        
        # Request headers to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _setup_logger(self):
        logger = logging.getLogger('RSSNewsService')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def fetch_engaging_news(self, 
                          categories: List[str] = None,
                          max_articles_per_source: int = 5,
                          prefer_trending: bool = True,
                          max_age_hours: int = 24) -> List[Dict]:
        """Fetch engaging news from RSS feeds"""
        
        if not categories:
            categories = ['general']
        
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for category in categories:
            self.logger.info(f"Fetching {category} news...")
            
            feeds = self.rss_feeds.get(category, self.rss_feeds['general'])
            
            for feed_url in feeds:
                try:
                    articles = self._fetch_from_feed(
                        feed_url, 
                        category, 
                        max_articles_per_source,
                        cutoff_time
                    )
                    
                    all_articles.extend(articles)
                    self.logger.info(f"Got {len(articles)} articles from {urlparse(feed_url).netloc}")
                    
                    # Small delay to be respectful
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.logger.warning(f"❌ Failed to fetch from {feed_url}: {e}")
                    continue
        
        # Remove duplicates and sort by engagement score
        unique_articles = self._deduplicate_articles(all_articles)
        
        if prefer_trending:
            unique_articles = self._score_and_sort_articles(unique_articles)
        
        self.logger.info(f"Total unique articles found: {len(unique_articles)}")
        
        return unique_articles
    
    def _fetch_from_feed(self, 
                        feed_url: str, 
                        category: str, 
                        max_articles: int,
                        cutoff_time: datetime) -> List[Dict]:
        """Fetch articles from a single RSS feed"""
        
        articles = []
        
        try:
            # Set timeout and headers
            response = requests.get(feed_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse RSS feed
            feed = feedparser.parse(response.content)
            
            if not hasattr(feed, 'entries') or not feed.entries:
                self.logger.warning(f"No entries found in feed: {feed_url}")
                return articles
            
            for entry in feed.entries[:max_articles * 2]:  # Get extra to filter
                try:
                    # Parse publication date
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])
                    
                    # Skip if too old
                    if pub_date and pub_date < cutoff_time:
                        continue
                    
                    # Extract article data
                    article = {
                        'title': self._clean_text(entry.get('title', '')),
                        'description': self._clean_text(entry.get('description', '') or entry.get('summary', '')),
                        'url': entry.get('link', ''),
                        'category': category,
                        'source': urlparse(feed_url).netloc,
                        'published': pub_date.isoformat() if pub_date else datetime.now().isoformat(),
                        'engagement_score': 0  # Will be calculated later
                    }
                    
                    # Skip if missing essential data
                    if not article['title'] or len(article['title']) < 10:
                        continue
                    
                    articles.append(article)
                    
                    if len(articles) >= max_articles:
                        break
                        
                except Exception as e:
                    self.logger.debug(f"Error processing entry: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching from {feed_url}: {e}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove HTML tags
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities
        import html
        text = html.unescape(text)
        
        # Clean whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title = article['title'].lower()
            
            # Create a simplified version for comparison
            simplified_title = ''.join(c for c in title if c.isalnum() or c.isspace())
            words = set(simplified_title.split())
            
            # Check if this is too similar to existing articles
            is_duplicate = False
            for seen_title in seen_titles:
                seen_words = set(seen_title.split())
                
                # Calculate word overlap
                if words and seen_words:
                    overlap = len(words.intersection(seen_words))
                    similarity = overlap / min(len(words), len(seen_words))
                    
                    if similarity > 0.8:  # 80% word overlap = duplicate
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                unique_articles.append(article)
                seen_titles.add(simplified_title)
        
        return unique_articles
    
    def _score_and_sort_articles(self, articles: List[Dict]) -> List[Dict]:
        """Score articles by engagement potential and sort"""
        
        for article in articles:
            score = 0
            title = article['title'].lower()
            description = article.get('description', '').lower()
            
            # Score based on engaging keywords
            for keyword in self.engaging_keywords:
                if keyword in title:
                    score += 10  # Title keywords worth more
                elif keyword in description:
                    score += 5
            
            # Score based on recency (newer = better)
            try:
                pub_date = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
                hours_old = (datetime.now() - pub_date.replace(tzinfo=None)).total_seconds() / 3600
                
                if hours_old < 1:
                    score += 20  # Very recent
                elif hours_old < 6:
                    score += 10  # Recent
                elif hours_old < 24:
                    score += 5   # Today
                
            except:
                pass
            
            # Score based on title length (not too short, not too long)
            title_length = len(article['title'])
            if 30 <= title_length <= 100:
                score += 5
            
            # Score based on description availability
            if article.get('description') and len(article['description']) > 50:
                score += 3
            
            # Random factor for variety
            score += random.randint(0, 5)
            
            article['engagement_score'] = score
        
        # Sort by engagement score (descending)
        return sorted(articles, key=lambda x: x['engagement_score'], reverse=True)
    
    def get_trending_topics(self, category: str = 'general', limit: int = 10) -> List[str]:
        """Extract trending topics from recent news"""
        
        articles = self.fetch_engaging_news(
            categories=[category],
            max_articles_per_source=20,
            max_age_hours=6  # Very recent
        )
        
        # Extract key terms from titles
        topics = []
        for article in articles[:limit]:
            title = article['title']
            
            # Extract potential topics (simple approach)
            words = title.split()
            for i, word in enumerate(words):
                if word.isupper() and len(word) > 2:  # Likely acronym/name
                    topics.append(word)
                elif len(word) > 6 and word[0].isupper():  # Likely proper noun
                    topics.append(word)
        
        # Return most common topics
        from collections import Counter
        topic_counts = Counter(topics)
        return [topic for topic, count in topic_counts.most_common(limit)]

def test_rss_service():
    """Test the RSS news service"""
    
    print("🧪 Testing RSS News Service...")
    
    service = RSSNewsService()
    
    # Test fetching news
    articles = service.fetch_engaging_news(
        categories=['technology', 'business'],
        max_articles_per_source=3,
        prefer_trending=True
    )
    
    print(f"\\n📰 Found {len(articles)} articles:")
    
    for i, article in enumerate(articles[:5]):
        print(f"\\n{i+1}. {article['title']}")
        print(f"   📂 {article['category']} | 🌐 {article['source']}")
        print(f"   🎯 Engagement Score: {article['engagement_score']}")
        if article.get('description'):
            desc = article['description'][:100] + "..." if len(article['description']) > 100 else article['description']
            print(f"   📝 {desc}")
    
    # Test trending topics
    print(f"\\n🔥 Trending topics:")
    topics = service.get_trending_topics('technology', 5)
    for topic in topics:
        print(f"  • {topic}")

if __name__ == "__main__":
    test_rss_service()
