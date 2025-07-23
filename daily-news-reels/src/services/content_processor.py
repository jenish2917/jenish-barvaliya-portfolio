"""
Enhanced Content Processor
Handles article summarization, script generation, and content optimization using Ollama
"""

import os
import ollama
import json
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass
import re
import time
from datetime import datetime

load_dotenv('config.env')

@dataclass
class ProcessedContent:
    """Processed content structure"""
    original_title: str
    original_content: str
    summary: str
    script: str
    keywords: List[str]
    sentiment: str
    estimated_duration: float
    quality_score: float
    
    def to_dict(self) -> Dict:
        return {
            'original_title': self.original_title,
            'original_content': self.original_content,
            'summary': self.summary,
            'script': self.script,
            'keywords': self.keywords,
            'sentiment': self.sentiment,
            'estimated_duration': self.estimated_duration,
            'quality_score': self.quality_score
        }

class EnhancedContentProcessor:
    def __init__(self):
        self.host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'qwen2.5:latest')
        self.logger = self._setup_logger()
        
        # Quality thresholds from config
        self.min_script_length = int(os.getenv('MIN_SCRIPT_LENGTH', '10'))
        self.max_script_length = int(os.getenv('MAX_SCRIPT_LENGTH', '3000'))
        self.quality_threshold = float(os.getenv('QUALITY_THRESHOLD', '20'))
        
        # Summary length limits (more permissive)
        self.min_summary_length = 30
        self.max_summary_length = 1000
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for content processor"""
        logger = logging.getLogger('ContentProcessor')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def process_article(self, article: Dict) -> Optional[ProcessedContent]:
        """
        Process a single article through the complete pipeline
        
        Args:
            article: Article dictionary with title, content, etc.
            
        Returns:
            ProcessedContent object or None if processing fails
        """
        try:
            title = article.get('title', '')
            content = article.get('content', '') or article.get('description', '')
            country = article.get('country', 'GLOBAL')
            category = article.get('category', 'general')
            
            self.logger.info(f"Processing article: {title[:50]}...")
            
            # Step 1: Create comprehensive summary
            summary = self._create_summary(title, content, country, category)
            if not summary:
                self.logger.warning("Failed to create summary")
                return None
            
            # Step 2: Generate engaging script
            script = self._generate_script(title, summary, country, category)
            if not script:
                self.logger.warning("Failed to generate script")
                return None
            
            # Step 3: Extract keywords and analyze sentiment
            keywords = self._extract_keywords(title, content)
            sentiment = self._analyze_sentiment(title, content)
            
            # Step 4: Estimate duration and calculate quality score
            estimated_duration = self._estimate_duration(script)
            quality_score = self._calculate_quality_score(title, summary, script, content)
            
            processed_content = ProcessedContent(
                original_title=title,
                original_content=content,
                summary=summary,
                script=script,
                keywords=keywords,
                sentiment=sentiment,
                estimated_duration=estimated_duration,
                quality_score=quality_score
            )
            
            self.logger.info(f"Processed successfully - Quality: {quality_score:.1f}%, Duration: {estimated_duration:.1f}s")
            return processed_content
            
        except Exception as e:
            self.logger.error(f"Error processing article: {e}")
            return None
    
    def _create_summary(self, title: str, content: str, country: str, category: str) -> Optional[str]:
        """Create an intelligent summary using Ollama"""
        try:
            prompt = f"""Create a concise, engaging summary of this news article. The summary should be 3-4 sentences long and capture the key points while being interesting for social media audiences.

Title: {title}
Country: {country}
Category: {category}
Content: {content[:1500]}

Requirements:
- 3-4 sentences maximum
- Include key facts and numbers
- Make it engaging and accessible
- Focus on the most newsworthy aspects
- Suitable for Gen-Z and Millennial audiences

Summary:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.3}
            )
            
            summary = response['message']['content'].strip()
            
            # Clean and validate summary
            summary = self._clean_text(summary)
            
            if len(summary) < self.min_summary_length or len(summary) > self.max_summary_length:
                self.logger.warning(f"Summary length out of range: {len(summary)} chars")
                return None
                
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating summary: {e}")
            return None
    
    def _generate_script(self, title: str, summary: str, country: str, category: str) -> Optional[str]:
        """Generate an engaging news anchor script"""
        try:
            # Determine appropriate hook based on category and country
            hooks = {
                'business': [
                    f"Breaking business news from {country}:",
                    f"Here's what's moving markets in {country}:",
                    f"Business update from {country}:"
                ],
                'technology': [
                    f"Tech news alert from {country}:",
                    f"Innovation update from {country}:",
                    f"The tech world is buzzing about this from {country}:"
                ],
                'sports': [
                    f"Sports update from {country}:",
                    f"Athletic action from {country}:",
                    f"Here's the latest from {country} sports:"
                ],
                'general': [
                    f"Breaking news from {country}:",
                    f"Here's what's happening in {country}:",
                    f"News alert from {country}:"
                ]
            }
            
            category_hooks = hooks.get(category.lower(), hooks['general'])
            
            prompt = f"""Convert this news summary into a natural, engaging 30-45 second news anchor script. Make it sound conversational and perfect for a short video reel.

Title: {title}
Summary: {summary}
Country: {country}
Category: {category}

Use one of these hooks to start: {', '.join(category_hooks)}

Requirements:
- 30-45 seconds when spoken (approximately 120-180 words)
- Natural, conversational tone
- Engaging for Gen-Z and Millennials  
- Include a compelling opening hook
- End with impact or thought-provoking statement
- Sound like a professional but friendly news anchor
- Use active voice
- Include specific details and numbers when available

Script:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.4}
            )
            
            script = response['message']['content'].strip()
            
            # Clean and validate script
            script = self._clean_script(script)
            
            if len(script) < self.min_script_length or len(script) > self.max_script_length:
                self.logger.warning(f"Script length out of range: {len(script)} chars")
                return None
                
            return script
            
        except Exception as e:
            self.logger.error(f"Error generating script: {e}")
            return None
    
    def _extract_keywords(self, title: str, content: str) -> List[str]:
        """Extract relevant keywords from article"""
        try:
            prompt = f"""Extract 5-8 relevant keywords from this news article. Focus on main topics, organizations, people, and key concepts.

Title: {title}
Content: {content[:800]}

Return only the keywords separated by commas, no explanations:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2}
            )
            
            keywords_text = response['message']['content'].strip()
            keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
            
            return keywords[:8]  # Limit to 8 keywords
            
        except Exception as e:
            self.logger.warning(f"Error extracting keywords: {e}")
            return []
    
    def _analyze_sentiment(self, title: str, content: str) -> str:
        """Analyze sentiment of the article"""
        try:
            prompt = f"""Analyze the sentiment of this news article. Respond with only one word: positive, negative, or neutral.

Title: {title}
Content: {content[:500]}

Sentiment:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1}
            )
            
            sentiment = response['message']['content'].strip().lower()
            
            if sentiment in ['positive', 'negative', 'neutral']:
                return sentiment
            else:
                return 'neutral'
                
        except Exception as e:
            self.logger.warning(f"Error analyzing sentiment: {e}")
            return 'neutral'
    
    def _estimate_duration(self, script: str) -> float:
        """Estimate speaking duration for script"""
        # Average speaking rate: ~150 words per minute
        words = len(script.split())
        duration = (words / 150) * 60  # Convert to seconds
        return round(duration, 1)
    
    def _calculate_quality_score(self, title: str, summary: str, script: str, content: str) -> float:
        """Calculate overall quality score for the content"""
        score = 0.0
        
        # Title quality (20%)
        if len(title) > 10 and len(title) < 100:
            score += 20
        elif len(title) >= 100:
            score += 15
        else:
            score += 10
        
        # Summary quality (25%)
        if 100 <= len(summary) <= 800:
            score += 25
        elif 50 <= len(summary) < 100 or 800 < len(summary) <= 1000:
            score += 20
        else:
            score += 15  # More permissive scoring
        
        # Script quality (30%)
        if self.min_script_length <= len(script) <= self.max_script_length:
            score += 30
        elif len(script) > self.max_script_length:
            score += 20
        else:
            score += 10
        
        # Content completeness (15%)
        if len(content) > 200:
            score += 15
        elif len(content) > 100:
            score += 10
        else:
            score += 5
        
        # Duration appropriateness (10%)
        duration = self._estimate_duration(script)
        if 25 <= duration <= 60:
            score += 10
        elif 20 <= duration < 25 or 60 < duration <= 75:
            score += 7
        else:
            score += 3
        
        return round(score, 1)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove quotes that might wrap the entire response
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        
        return text.strip()
    
    def _clean_script(self, script: str) -> str:
        """Clean and optimize script for TTS"""
        script = self._clean_text(script)
        
        # Fix common TTS issues
        replacements = {
            '&': 'and',
            '%': 'percent',
            '$': 'dollars',
            '€': 'euros',
            '£': 'pounds',
            '@': 'at',
            '#': 'number',
            'w/': 'with',
            'w/o': 'without',
            'vs.': 'versus',
            'vs': 'versus',
            'etc.': 'etcetera'
        }
        
        for old, new in replacements.items():
            script = script.replace(old, new)
        
        # Fix abbreviations that might not be pronounced correctly
        script = re.sub(r'\bUS\b', 'United States', script)
        script = re.sub(r'\bUK\b', 'United Kingdom', script)
        script = re.sub(r'\bAI\b', 'artificial intelligence', script)
        script = re.sub(r'\bCEO\b', 'C E O', script)
        script = re.sub(r'\bFBI\b', 'F B I', script)
        script = re.sub(r'\bNASA\b', 'NASA', script)
        script = re.sub(r'\bCOVID-19\b', 'COVID nineteen', script)
        
        return script
    
    def process_batch(self, articles: List[Dict], max_workers: int = 4) -> List[ProcessedContent]:
        """Process multiple articles in parallel for maximum speed"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import threading
        
        processed_articles = []
        
        self.logger.info(f"🚀 Processing {len(articles)} articles in parallel with {max_workers} workers...")
        
        # Create a thread-safe list for results
        results_lock = threading.Lock()
        
        def process_single_article(article_data):
            """Process a single article (thread-safe)"""
            article, index = article_data
            try:
                processed = self.process_article(article)
                if processed and processed.quality_score >= self.quality_threshold:
                    return (index, processed, True)
                else:
                    quality = processed.quality_score if processed else 0
                    self.logger.warning(f"Article {index+1} failed quality threshold ({quality:.1f}% < {self.quality_threshold}%)")
                    return (index, None, False)
            except Exception as e:
                self.logger.error(f"Error processing article {index+1}: {e}")
                return (index, None, False)
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all articles for processing
            article_data = [(article, i) for i, article in enumerate(articles)]
            future_to_article = {executor.submit(process_single_article, data): data for data in article_data}
            
            # Collect results as they complete
            completed_count = 0
            for future in as_completed(future_to_article):
                completed_count += 1
                index, processed, success = future.result()
                
                if success and processed:
                    with results_lock:
                        processed_articles.append(processed)
                
                # Log progress
                self.logger.info(f"✅ Completed {completed_count}/{len(articles)} articles")
        
        self.logger.info(f"🎉 Successfully processed {len(processed_articles)}/{len(articles)} articles in parallel")
        return processed_articles
    
    def save_processed_content(self, processed_content: List[ProcessedContent], output_dir: str) -> str:
        """Save processed content for later use"""
        os.makedirs(output_dir, exist_ok=True)
        
        content_data = {
            'processing_time': datetime.now().isoformat(),
            'total_processed': len(processed_content),
            'average_quality': sum(c.quality_score for c in processed_content) / len(processed_content) if processed_content else 0,
            'content': [c.to_dict() for c in processed_content]
        }
        
        output_path = os.path.join(output_dir, f"processed_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved processed content to {output_path}")
        return output_path

# Legacy compatibility
class NewsSummarizer(EnhancedContentProcessor):
    """Backward compatibility wrapper"""
    
    def summarize_article(self, article: Dict) -> str:
        """Legacy method for summarization"""
        processed = self.process_article(article)
        return processed.summary if processed else ""

class ScriptGenerator(EnhancedContentProcessor):
    """Backward compatibility wrapper"""
    
    def generate_news_script(self, article: Dict) -> str:
        """Legacy method for script generation"""
        processed = self.process_article(article)
        return processed.script if processed else ""
