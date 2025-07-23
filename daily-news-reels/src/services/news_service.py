"""
Enhanced News Service
Fetches today's news from multiple sources with comprehensive article data
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dotenv import load_dotenv
import logging
from urllib.parse import urlparse
import time
from dataclasses import dataclass
from newsapi import NewsApiClient
import json

load_dotenv('config.env')

@dataclass
class Article:
    """Enhanced article data structure"""
    title: str
    description: str
    content: str
    url: str
    url_to_image: str
    published_at: str
    source_name: str
    country: str
    category: str
    author: Optional[str] = None
    language: str = 'en'
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'url': self.url,
            'urlToImage': self.url_to_image,
            'publishedAt': self.published_at,
            'source': self.source_name,
            'country': self.country,
            'category': self.category,
            'author': self.author,
            'language': self.language
        }

class EnhancedNewsService:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = os.getenv('NEWS_API_URL', 'https://newsapi.org/v2')
        
        if not self.api_key:
            raise ValueError("NEWS_API_KEY not found in config.env")
            
        self.client = NewsApiClient(api_key=self.api_key)
        self.logger = self._setup_logger()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds between requests
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for news service"""
        logger = logging.getLogger('NewsService')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _rate_limit(self):
        """Implement rate limiting for API calls"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def fetch_todays_news(self, 
                         countries: List[str] = None, 
                         categories: List[str] = None,
                         max_articles_per_category: int = 10) -> List[Article]:
        """
        Fetch today's news articles from multiple countries and categories
        
        Args:
            countries: List of country codes (e.g., ['us', 'in', 'gb'])
            categories: List of news categories
            max_articles_per_category: Maximum articles per category
            
        Returns:
            List of Article objects
        """
        if countries is None:
            countries = os.getenv('DEFAULT_COUNTRIES', 'us,in,gb').split(',')
        
        if categories is None:
            categories = os.getenv('DEFAULT_CATEGORIES', 'general,business,technology').split(',')
            
        self.logger.info(f"Fetching news for countries: {countries}")
        self.logger.info(f"Categories: {categories}")
        
        all_articles = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        for country in countries:
            for category in categories:
                try:
                    self._rate_limit()
                    
                    self.logger.info(f"Fetching {category} news from {country.upper()}")
                    
                    # Fetch top headlines
                    response = self.client.get_top_headlines(
                        country=country.strip(),
                        category=category.strip(),
                        page_size=max_articles_per_category
                    )
                    
                    if response['status'] == 'ok':
                        articles = response.get('articles', [])
                        
                        for article_data in articles:
                            # Filter for today's articles
                            if self._is_today_article(article_data.get('publishedAt', '')):
                                article = self._process_article(article_data, country, category)
                                if article and self._is_valid_article(article):
                                    all_articles.append(article)
                                    
                        self.logger.info(f"Found {len([a for a in all_articles if a.country == country and a.category == category])} valid articles")
                        
                    else:
                        self.logger.warning(f"API error for {country}/{category}: {response.get('message', 'Unknown error')}")
                        
                except Exception as e:
                    self.logger.error(f"Error fetching news for {country}/{category}: {e}")
                    continue
        
        # Remove duplicates based on title similarity
        unique_articles = self._remove_duplicates(all_articles)
        
        self.logger.info(f"Total unique articles fetched: {len(unique_articles)}")
        return unique_articles
    
    def _is_today_article(self, published_at: str) -> bool:
        """Check if article was published today"""
        try:
            if not published_at:
                return False
                
            # Parse the published date
            article_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            today = datetime.now().date()
            
            # Consider articles from today and yesterday (for timezone differences)
            yesterday = today - timedelta(days=1)
            
            return article_date.date() >= yesterday
            
        except Exception as e:
            self.logger.warning(f"Error parsing date {published_at}: {e}")
            return False
    
    def _process_article(self, article_data: Dict, country: str, category: str) -> Optional[Article]:
        """Process raw article data into Article object"""
        try:
            # Extract full content if available
            content = article_data.get('content', '')
            description = article_data.get('description', '')
            
            # If no content, try to fetch from URL
            if not content or len(content) < 100:
                content = self._fetch_full_content(article_data.get('url', ''))
            
            # Use description as fallback content
            if not content:
                content = description
            
            article = Article(
                title=article_data.get('title', '').strip(),
                description=description or '',
                content=content or '',
                url=article_data.get('url', ''),
                url_to_image=article_data.get('urlToImage', ''),
                published_at=article_data.get('publishedAt', ''),
                source_name=article_data.get('source', {}).get('name', 'Unknown'),
                country=country.upper(),
                category=category.lower(),
                author=article_data.get('author', ''),
                language='en'
            )
            
            return article
            
        except Exception as e:
            self.logger.error(f"Error processing article: {e}")
            return None
    
    def _fetch_full_content(self, url: str) -> str:
        """Attempt to fetch full article content from URL"""
        try:
            if not url:
                return ""
                
            # Simple content extraction (you might want to use a library like newspaper3k)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Basic content extraction - in production, use proper web scraping
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Return first 1000 characters
            return text[:1000] if text else ""
            
        except Exception as e:
            self.logger.warning(f"Could not fetch content from {url}: {e}")
            return ""
    
    def _is_valid_article(self, article: Article) -> bool:
        """Validate article quality and completeness"""
        # Check required fields
        if not article.title or len(article.title) < 10:
            return False
            
        if not article.content and not article.description:
            return False
            
        # Check content length
        content_text = article.content or article.description
        if len(content_text) < 50:
            return False
        
        # Check for placeholder content
        invalid_content = [
            '[Removed]', 
            'This content is not available',
            'Subscribe to read',
            'Login required'
        ]
        
        for invalid in invalid_content:
            if invalid.lower() in content_text.lower():
                return False
        
        return True
    
    def _remove_duplicates(self, articles: List[Article]) -> List[Article]:
        """Remove duplicate articles based on title similarity"""
        from difflib import SequenceMatcher
        
        unique_articles = []
        
        for article in articles:
            is_duplicate = False
            
            for existing in unique_articles:
                # Check title similarity
                similarity = SequenceMatcher(None, article.title.lower(), existing.title.lower()).ratio()
                
                if similarity > 0.8:  # 80% similarity threshold
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_articles.append(article)
        
        return unique_articles
    
    def save_articles_metadata(self, articles: List[Article], output_dir: str):
        """Save articles metadata for tracking and analysis"""
        os.makedirs(output_dir, exist_ok=True)
        
        metadata = {
            'fetch_time': datetime.now().isoformat(),
            'total_articles': len(articles),
            'by_country': {},
            'by_category': {},
            'articles': [article.to_dict() for article in articles]
        }
        
        # Count by country and category
        for article in articles:
            metadata['by_country'][article.country] = metadata['by_country'].get(article.country, 0) + 1
            metadata['by_category'][article.category] = metadata['by_category'].get(article.category, 0) + 1
        
        # Save metadata
        metadata_path = os.path.join(output_dir, f"articles_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved articles metadata to {metadata_path}")
        return metadata_path

# Legacy compatibility
class NewsFetcher(EnhancedNewsService):
    """Backward compatibility wrapper"""
    pass
