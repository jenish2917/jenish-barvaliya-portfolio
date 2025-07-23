"""
Enhanced RSS News Service with Full Article Fetching and Summarization
Fetches complete article content, creates comprehensive summaries, and prevents duplicates
"""

import os
import sys
import requests
import feedparser
import json
import time
import logging
import hashlib
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from urllib.parse import urlparse
from dataclasses import dataclass
import re
from bs4 import BeautifulSoup

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

@dataclass
class ArticleContent:
    """Complete article data structure"""
    title: str
    description: str
    full_content: str
    summary: str
    url: str
    source: str
    category: str
    published: str
    content_hash: str
    word_count: int
    engagement_score: float

class EnhancedRSSService:
    """Enhanced RSS service with full article fetching and summarization"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.logger = self._setup_logger()
        self.ollama_url = ollama_url
        self.processed_hashes: Set[str] = set()  # Track processed articles
        self.ollama_available = self._check_ollama_status()
        
        if not self.ollama_available:
            self.logger.warning("Ollama not available - will use fallback summaries")
        
        # Enhanced RSS feeds with better coverage
        self.rss_feeds = {
            'general': [
                'http://feeds.bbci.co.uk/news/rss.xml',
                'https://feeds.npr.org/1001/rss.xml',
                'https://feeds.reuters.com/reuters/topNews',
                'https://rss.cnn.com/rss/edition.rss',
                'https://feeds.washingtonpost.com/rss/national',
                'https://www.theguardian.com/world/rss',
                'https://feeds.bloomberg.com/economics/news.rss',
                'https://feeds.ap.org/ApTopHeadlines'
            ],
            'technology': [
                'https://feeds.feedburner.com/techcrunch/startups',
                'https://feeds.arstechnica.com/arstechnica/technology-lab',
                'https://feeds.engadget.com/engadget',
                'https://feeds.reuters.com/reuters/technologyNews'
            ],
            'business': [
                'https://feeds.bloomberg.com/markets/news.rss',
                'https://feeds.reuters.com/reuters/businessNews',
                'https://feeds.fortune.com/fortune/headlines'
            ]
        }
        
        # Headers for web scraping
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the service"""
        logger = logging.getLogger('EnhancedRSSService')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _check_ollama_status(self) -> bool:
        """Check if Ollama is running and responsive"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def fetch_and_summarize_news(
        self, 
        max_articles: int = 10,
        category: str = 'general',
        hours_back: int = 24,
        min_word_count: int = 100
    ) -> List[ArticleContent]:
        """
        Fetch articles, get full content, and create comprehensive summaries
        
        Args:
            max_articles: Maximum number of articles to process
            category: News category to fetch
            hours_back: How many hours back to look for articles
            min_word_count: Minimum words in article to include
            
        Returns:
            List of ArticleContent with full summaries
        """
        self.logger.info(f"Starting enhanced news fetch: {max_articles} articles from {category}")
        
        # Fetch RSS articles
        rss_articles = self._fetch_rss_articles(category, hours_back)
        self.logger.info(f"Found {len(rss_articles)} RSS articles")
        
        # Process articles with full content
        processed_articles = []
        processed_count = 0
        
        for article in rss_articles:
            if processed_count >= max_articles:
                break
                
            try:
                # Check for duplicates
                article_hash = self._generate_content_hash(article['title'], article['url'])
                if article_hash in self.processed_hashes:
                    self.logger.debug(f"Skipping duplicate: {article['title'][:50]}...")
                    continue
                
                # Fetch full article content
                full_content = self._fetch_article_content(article['url'])
                if not full_content or len(full_content.split()) < min_word_count:
                    self.logger.debug(f"Skipping article with insufficient content: {article['title'][:50]}...")
                    continue
                
                # Create comprehensive summary
                summary = self._create_comprehensive_summary(
                    title=article['title'],
                    content=full_content,
                    source=article['source']
                )
                
                if not summary:
                    self.logger.warning(f"Failed to create summary for: {article['title'][:50]}...")
                    continue
                
                # Create ArticleContent object
                article_content = ArticleContent(
                    title=article['title'],
                    description=article['description'],
                    full_content=full_content,
                    summary=summary,
                    url=article['url'],
                    source=article['source'],
                    category=article['category'],
                    published=article['published'],
                    content_hash=article_hash,
                    word_count=len(full_content.split()),
                    engagement_score=self._calculate_engagement_score(article['title'], summary)
                )
                
                processed_articles.append(article_content)
                self.processed_hashes.add(article_hash)
                processed_count += 1
                
                self.logger.info(f"Processed article {processed_count}/{max_articles}: {article['title'][:50]}... ({article_content.word_count} words)")
                
                # Small delay to be respectful
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error processing article '{article['title'][:50]}...': {e}")
                continue
        
        # Sort by engagement score
        processed_articles.sort(key=lambda x: x.engagement_score, reverse=True)
        
        self.logger.info(f"Successfully processed {len(processed_articles)} articles with full summaries")
        return processed_articles
    
    def _fetch_rss_articles(self, category: str, hours_back: int) -> List[Dict]:
        """Fetch articles from RSS feeds"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        feeds = self.rss_feeds.get(category, self.rss_feeds['general'])
        all_articles = []
        
        for feed_url in feeds:
            try:
                self.logger.debug(f"Fetching from {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:  # Limit per feed
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
                        
                        article = {
                            'title': self._clean_text(entry.get('title', '')),
                            'description': self._clean_text(entry.get('description', '') or entry.get('summary', '')),
                            'url': entry.get('link', ''),
                            'category': category,
                            'source': urlparse(feed_url).netloc,
                            'published': pub_date.isoformat() if pub_date else datetime.now().isoformat()
                        }
                        
                        if article['title'] and article['url'] and len(article['title']) > 10:
                            all_articles.append(article)
                            
                    except Exception as e:
                        self.logger.debug(f"Error processing RSS entry: {e}")
                        continue
                        
            except Exception as e:
                self.logger.warning(f"Error fetching from {feed_url}: {e}")
                continue
        
        return all_articles
    
    def _fetch_article_content(self, url: str) -> Optional[str]:
        """Fetch full article content from URL"""
        try:
            self.logger.debug(f"Fetching content from: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
                tag.decompose()
            
            # Try different content selectors
            content_selectors = [
                'article',
                '.article-content',
                '.story-content',
                '.post-content',
                '.entry-content',
                '.content',
                'main',
                '.article-body',
                '.story-body'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = ' '.join([elem.get_text(strip=True) for elem in elements])
                    if len(content) > 500:  # Good content found
                        break
            
            # Fallback to all paragraphs
            if not content or len(content) < 500:
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            # Clean and return
            content = self._clean_text(content)
            
            if len(content) < 200:
                self.logger.debug(f"Insufficient content extracted from {url}")
                return None
                
            return content
            
        except Exception as e:
            self.logger.debug(f"Error fetching content from {url}: {e}")
            return None
    
    def _create_comprehensive_summary(self, title: str, content: str, source: str) -> Optional[str]:
        """Create comprehensive summary using Ollama with fallback"""
        try:
            # First try Ollama for AI summary
            ai_summary = self._try_ollama_summary(title, content)
            if ai_summary:
                return ai_summary
            
            # Fallback to intelligent extraction
            self.logger.info(f"Using fallback summary for: {title[:50]}...")
            return self._create_fallback_summary(title, content)
            
        except Exception as e:
            self.logger.error(f"Error creating summary for '{title[:50]}...': {e}")
            return self._create_fallback_summary(title, content)
    
    def _try_ollama_summary(self, title: str, content: str) -> Optional[str]:
        """Try to create summary using Ollama API"""
        # Skip Ollama if not available
        if not self.ollama_available:
            return None
            
        try:
            # Prepare much shorter content for faster processing
            content_snippet = content[:1500]  # Reduced from 4000
            
            prompt = f"""Summarize this news article in 2-3 engaging sentences for a news reel:

Title: {title}
Content: {content_snippet}

Summary:"""

            # Call Ollama API with shorter timeout
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.6,
                        "max_tokens": 150
                    }
                },
                timeout=15  # Reduced timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get('response', '').strip()
                
                if summary and len(summary) > 30:
                    self.logger.debug(f"AI summary created for: {title[:50]}...")
                    return summary
                    
            return None
            
        except Exception as e:
            self.logger.debug(f"Ollama summary failed: {e}")
            return None
    
    def _create_fallback_summary(self, title: str, content: str) -> str:
        """Create fallback summary when AI fails"""
        try:
            # Extract first few sentences that contain key information
            sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
            
            # Take first 2-3 meaningful sentences
            summary_sentences = []
            for sentence in sentences[:5]:
                if len(sentence) > 30 and any(word in sentence.lower() for word in 
                    ['said', 'reported', 'announced', 'revealed', 'according', 'officials', 'sources']):
                    summary_sentences.append(sentence)
                    if len(summary_sentences) >= 2:
                        break
            
            if not summary_sentences:
                # Fallback to first few sentences
                summary_sentences = sentences[:2]
            
            # Create engaging summary
            summary = '. '.join(summary_sentences)
            if summary and len(summary) > 50:
                # Add engaging ending
                summary += "."
                return summary
            
            # Last resort - use title + first sentence
            first_sentence = sentences[0] if sentences else ""
            return f"{title}. {first_sentence}." if first_sentence else title
            
        except Exception:
            # Ultimate fallback
            return title
    
    def _generate_content_hash(self, title: str, url: str) -> str:
        """Generate hash for duplicate detection"""
        combined = f"{title.lower().strip()}{url.strip()}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _calculate_engagement_score(self, title: str, summary: str) -> float:
        """Calculate engagement score for ranking"""
        score = 0.0
        
        # Title factors
        engaging_words = ['breaking', 'urgent', 'shocking', 'exclusive', 'major', 'huge', 'crisis', 'dramatic']
        score += sum(2 for word in engaging_words if word in title.lower())
        
        # Summary length and quality
        if summary:
            score += min(len(summary) / 100, 3)  # Longer summaries up to 3 points
            
        # Content indicators
        if any(word in title.lower() for word in ['trump', 'biden', 'china', 'russia', 'ai', 'climate']):
            score += 1.5
            
        return score
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities
        import html
        text = html.unescape(text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove extra punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
        
        return text

def test_enhanced_service():
    """Test the enhanced RSS service"""
    service = EnhancedRSSService()
    
    print("🌍 TESTING ENHANCED RSS SERVICE WITH FULL ARTICLE SUMMARIZATION")
    print("=" * 70)
    
    # Test with 3 articles
    articles = service.fetch_and_summarize_news(max_articles=3, category='general')
    
    print(f"\n✅ Successfully processed {len(articles)} articles")
    
    for i, article in enumerate(articles, 1):
        print(f"\n📰 ARTICLE {i}")
        print("-" * 40)
        print(f"Title: {article.title}")
        print(f"Source: {article.source}")
        print(f"Words: {article.word_count}")
        print(f"Score: {article.engagement_score:.1f}")
        print(f"Summary: {article.summary}")
        print(f"URL: {article.url}")

if __name__ == "__main__":
    test_enhanced_service()
