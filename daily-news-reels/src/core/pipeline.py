"""
Enhanced Pipeline Core
Main orchestrator for the news-to-reels generation pipeline with quality control
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import json
from pathlib import Path
import time

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.news_service import EnhancedNewsService, Article
from services.content_processor import EnhancedContentProcessor, ProcessedContent
from services.audio_service import EnhancedAudioService
from services.video_service import EnhancedVideoService
from services.quality_service import QualityAnalyzer, QualityMetrics

from dotenv import load_dotenv

load_dotenv('config.env')

@dataclass
class PipelineStats:
    """Pipeline execution statistics"""
    start_time: datetime
    end_time: Optional[datetime]
    total_articles_fetched: int
    total_articles_processed: int
    total_audio_generated: int
    total_videos_created: int
    total_quality_passed: int
    average_quality_score: float
    total_duration: float
    
    def to_dict(self) -> Dict:
        return {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'execution_time_minutes': (self.end_time - self.start_time).total_seconds() / 60 if self.end_time else None,
            'total_articles_fetched': self.total_articles_fetched,
            'total_articles_processed': self.total_articles_processed,
            'total_audio_generated': self.total_audio_generated,
            'total_videos_created': self.total_videos_created,
            'total_quality_passed': self.total_quality_passed,
            'average_quality_score': self.average_quality_score,
            'total_duration': self.total_duration,
            'success_rate': (self.total_quality_passed / self.total_articles_fetched * 100) if self.total_articles_fetched > 0 else 0
        }

class EnhancedPipeline:
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Initialize services
        self.news_service = EnhancedNewsService()
        self.content_processor = EnhancedContentProcessor()
        self.audio_service = EnhancedAudioService()
        self.video_service = EnhancedVideoService()
        self.quality_analyzer = QualityAnalyzer()
        
        # Configuration
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.quality_threshold = float(os.getenv('QUALITY_THRESHOLD', '75'))
        
        # Setup output directories
        self._setup_directories()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logger = logging.getLogger('EnhancedPipeline')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # File handler
            log_dir = os.path.join(os.getenv('OUTPUT_DIR', 'output'), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            logger.info(f"Logging initialized - Log file: {log_file}")
        
        return logger
    
    def _setup_directories(self):
        """Setup output directory structure"""
        directories = [
            self.output_dir,
            os.path.join(self.output_dir, 'audio'),
            os.path.join(self.output_dir, 'videos'),
            os.path.join(self.output_dir, 'reports'),
            os.path.join(self.output_dir, 'temp'),
            os.path.join(self.output_dir, 'logs'),
            os.path.join(self.output_dir, 'sessions'),
            os.path.join(self.output_dir, 'thumbnails')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        self.logger.info("Output directories initialized")
    
    def execute_full_pipeline(self,
                            countries: List[str] = None,
                            categories: List[str] = None,
                            max_articles_per_category: int = 10) -> Tuple[PipelineStats, List[Dict]]:
        """
        Execute the complete news-to-reels pipeline with quality control
        
        Args:
            countries: List of country codes to fetch news from
            categories: List of news categories
            max_articles_per_category: Maximum articles per category
            
        Returns:
            Tuple of (pipeline_stats, successful_articles)
        """
        
        # Initialize stats
        stats = PipelineStats(
            start_time=datetime.now(),
            end_time=None,
            total_articles_fetched=0,
            total_articles_processed=0,
            total_audio_generated=0,
            total_videos_created=0,
            total_quality_passed=0,
            average_quality_score=0.0,
            total_duration=0.0
        )
        
        try:
            self.logger.info("🚀 Starting Enhanced News-to-Reels Pipeline")
            self.logger.info("=" * 80)
            
            session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
            session_dir = os.path.join(self.output_dir, 'sessions', session_id)
            os.makedirs(session_dir, exist_ok=True)
            
            # Step 1: Fetch News Articles
            self.logger.info("📰 STEP 1: Fetching Latest News Articles")
            articles = self._fetch_news(countries, categories, max_articles_per_category)
            stats.total_articles_fetched = len(articles)
            
            if not articles:
                self.logger.error("No articles fetched. Pipeline terminated.")
                return stats, []
            
            # Save fetched articles
            articles_data = [article.to_dict() for article in articles]
            self._save_session_data(session_dir, 'fetched_articles.json', articles_data)
            
            # Step 2: Process Content (Summarize + Generate Scripts)
            self.logger.info("🤖 STEP 2: Processing Content with AI")
            processed_articles = self._process_content(articles_data)
            stats.total_articles_processed = len(processed_articles)
            
            if not processed_articles:
                self.logger.error("No articles processed successfully. Pipeline terminated.")
                return stats, []
            
            self._save_session_data(session_dir, 'processed_articles.json', 
                                  [article for article in processed_articles])
            
            # Step 3: Generate Audio
            self.logger.info("🎵 STEP 3: Generating High-Quality Audio")
            articles_with_audio = self._generate_audio(processed_articles, session_dir)
            stats.total_audio_generated = len(articles_with_audio)
            
            if not articles_with_audio:
                self.logger.error("No audio generated successfully. Pipeline terminated.")
                return stats, []
            
            # Step 4: Create Videos
            self.logger.info("🎬 STEP 4: Creating High-Quality Videos")
            articles_with_videos = self._create_videos(articles_with_audio, session_dir)
            stats.total_videos_created = len(articles_with_videos)
            
            if not articles_with_videos:
                self.logger.error("No videos created successfully. Pipeline terminated.")
                return stats, []
            
            # Step 5: Quality Analysis
            self.logger.info("🔍 STEP 5: Comprehensive Quality Analysis")
            quality_results = self._analyze_quality(articles_with_videos)
            
            # Filter by quality threshold
            high_quality_articles = []
            quality_scores = []
            
            for article, quality_metrics in zip(articles_with_videos, quality_results):
                if quality_metrics.overall_quality >= self.quality_threshold:
                    article['quality_metrics'] = quality_metrics.to_dict()
                    high_quality_articles.append(article)
                    quality_scores.append(quality_metrics.overall_quality)
                else:
                    self.logger.warning(f"Article failed quality threshold: {article.get('title', 'Unknown')[:50]} (Score: {quality_metrics.overall_quality:.1f}%)")
            
            stats.total_quality_passed = len(high_quality_articles)
            stats.average_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            stats.total_duration = sum(article.get('audio_metrics', {}).get('duration', 0) for article in high_quality_articles)
            
            # Step 6: Generate Reports
            self.logger.info("📊 STEP 6: Generating Comprehensive Reports")
            self._generate_reports(stats, high_quality_articles, quality_results, session_dir)
            
            # Finalize stats
            stats.end_time = datetime.now()
            execution_time = (stats.end_time - stats.start_time).total_seconds() / 60
            
            # Final summary
            self.logger.info("✅ PIPELINE EXECUTION COMPLETE")
            self.logger.info("=" * 80)
            self.logger.info(f"📊 Execution Summary:")
            self.logger.info(f"   ⏱️  Execution Time: {execution_time:.1f} minutes")
            self.logger.info(f"   📰 Articles Fetched: {stats.total_articles_fetched}")
            self.logger.info(f"   🤖 Articles Processed: {stats.total_articles_processed}")
            self.logger.info(f"   🎵 Audio Generated: {stats.total_audio_generated}")
            self.logger.info(f"   🎬 Videos Created: {stats.total_videos_created}")
            self.logger.info(f"   ✅ Quality Passed: {stats.total_quality_passed}")
            self.logger.info(f"   📈 Average Quality: {stats.average_quality_score:.1f}%")
            self.logger.info(f"   ⏱️  Total Duration: {stats.total_duration:.1f} seconds")
            self.logger.info(f"   📂 Session Directory: {session_dir}")
            
            return stats, high_quality_articles
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {e}")
            stats.end_time = datetime.now()
            return stats, []
    
    def _fetch_news(self, countries: List[str], categories: List[str], max_articles: int) -> List[Article]:
        """Fetch news articles with error handling"""
        try:
            if countries is None:
                countries = os.getenv('DEFAULT_COUNTRIES', 'us,in,gb').split(',')
            
            if categories is None:
                categories = os.getenv('DEFAULT_CATEGORIES', 'general,business,technology').split(',')
            
            self.logger.info(f"Fetching news from {len(countries)} countries, {len(categories)} categories")
            
            articles = self.news_service.fetch_todays_news(
                countries=countries,
                categories=categories,
                max_articles_per_category=max_articles
            )
            
            # Save metadata
            metadata_path = self.news_service.save_articles_metadata(
                articles, 
                os.path.join(self.output_dir, 'reports')
            )
            
            self.logger.info(f"✅ Fetched {len(articles)} unique articles")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error fetching news: {e}")
            return []
    
    def _process_content(self, articles_data: List[Dict], max_workers: int = 4) -> List[Dict]:
        """Process articles through content pipeline in parallel"""
        try:
            self.logger.info(f"🚀 Processing {len(articles_data)} articles with AI in parallel (max_workers={max_workers})")
            
            processed_results = self.content_processor.process_batch(articles_data, max_workers=max_workers)
            
            # Combine original article data with processed content
            enhanced_articles = []
            for i, article in enumerate(articles_data):
                if i < len(processed_results):
                    processed = processed_results[i]
                    
                    # Merge data
                    enhanced_article = article.copy()
                    enhanced_article.update({
                        'summary': processed.summary,
                        'script': processed.script,
                        'keywords': processed.keywords,
                        'sentiment': processed.sentiment,
                        'estimated_duration': processed.estimated_duration,
                        'content_quality_score': processed.quality_score
                    })
                    
                    enhanced_articles.append(enhanced_article)
            
            # Save processed content
            self.content_processor.save_processed_content(
                processed_results,
                os.path.join(self.output_dir, 'reports')
            )
            
            self.logger.info(f"✅ Successfully processed {len(enhanced_articles)} articles")
            return enhanced_articles
            
        except Exception as e:
            self.logger.error(f"Error processing content: {e}")
            return []
    
    def _generate_audio(self, articles: List[Dict], session_dir: str, max_workers: int = 4) -> List[Dict]:
        """Generate audio for all articles in parallel"""
        try:
            audio_dir = os.path.join(session_dir, 'audio')
            
            self.logger.info(f"🎤 Generating audio with {max_workers} parallel workers")
            articles_with_audio = self.audio_service.generate_batch_voiceovers(
                articles, 
                audio_dir,
                max_workers=max_workers
            )
            
            # Save audio report
            self.audio_service.save_audio_report(
                articles_with_audio,
                os.path.join(self.output_dir, 'reports')
            )
            
            self.logger.info(f"✅ Generated audio for {len(articles_with_audio)} articles")
            return articles_with_audio
            
        except Exception as e:
            self.logger.error(f"Error generating audio: {e}")
            return []
    
    def _create_videos(self, articles_with_audio: List[Dict], session_dir: str, max_workers: int = 2) -> List[Dict]:
        """Create videos for all articles in parallel (limited workers for video processing)"""
        try:
            video_dir = os.path.join(session_dir, 'videos')
            
            self.logger.info(f"🎬 Generating videos with {max_workers} parallel workers")
            articles_with_videos = self.video_service.generate_batch_videos(
                articles_with_audio,
                video_dir,
                max_workers=max_workers
            )
            
            # Save video report
            self.video_service.save_video_report(
                articles_with_videos,
                os.path.join(self.output_dir, 'reports')
            )
            
            self.logger.info(f"✅ Created videos for {len(articles_with_videos)} articles")
            return articles_with_videos
            
        except Exception as e:
            self.logger.error(f"Error creating videos: {e}")
            return []
    
    def _analyze_quality(self, articles_with_videos: List[Dict]) -> List[QualityMetrics]:
        """Perform comprehensive quality analysis"""
        try:
            quality_results = self.quality_analyzer.analyze_batch_quality(articles_with_videos)
            
            # Save quality report
            self.quality_analyzer.save_quality_report(
                articles_with_videos,
                quality_results,
                os.path.join(self.output_dir, 'reports')
            )
            
            self.logger.info(f"✅ Quality analysis complete for {len(quality_results)} articles")
            return quality_results
            
        except Exception as e:
            self.logger.error(f"Error analyzing quality: {e}")
            return []
    
    def _generate_reports(self, stats: PipelineStats, articles: List[Dict], 
                         quality_results: List[QualityMetrics], session_dir: str):
        """Generate comprehensive reports"""
        try:
            reports_dir = os.path.join(self.output_dir, 'reports')
            
            # Pipeline stats report
            stats_report = {
                'pipeline_stats': stats.to_dict(),
                'session_directory': session_dir,
                'articles_summary': {
                    'total_articles': len(articles),
                    'by_country': {},
                    'by_category': {},
                    'quality_distribution': {}
                }
            }
            
            # Aggregate statistics
            for article in articles:
                country = article.get('country', 'Unknown')
                category = article.get('category', 'unknown')
                quality_score = article.get('quality_metrics', {}).get('overall_quality', 0)
                
                stats_report['articles_summary']['by_country'][country] = \
                    stats_report['articles_summary']['by_country'].get(country, 0) + 1
                
                stats_report['articles_summary']['by_category'][category] = \
                    stats_report['articles_summary']['by_category'].get(category, 0) + 1
                
                # Quality distribution
                if quality_score >= 90:
                    quality_level = 'excellent'
                elif quality_score >= 80:
                    quality_level = 'good'
                elif quality_score >= 70:
                    quality_level = 'fair'
                else:
                    quality_level = 'poor'
                
                stats_report['articles_summary']['quality_distribution'][quality_level] = \
                    stats_report['articles_summary']['quality_distribution'].get(quality_level, 0) + 1
            
            # Save pipeline report
            pipeline_report_path = os.path.join(reports_dir, f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(pipeline_report_path, 'w', encoding='utf-8') as f:
                json.dump(stats_report, f, indent=2, ensure_ascii=False)
            
            # Save final articles data
            final_articles_path = os.path.join(session_dir, 'final_articles.json')
            with open(final_articles_path, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📊 Reports generated in {reports_dir}")
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {e}")
    
    def _save_session_data(self, session_dir: str, filename: str, data):
        """Save session data for debugging and analysis"""
        try:
            filepath = os.path.join(session_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Saved session data: {filename}")
            
        except Exception as e:
            self.logger.warning(f"Could not save session data {filename}: {e}")
    
    def execute_quick_test(self, max_articles: int = 2) -> Tuple[PipelineStats, List[Dict]]:
        """Execute a quick test of the pipeline with limited articles"""
        self.logger.info("🧪 Running Quick Pipeline Test")
        
        return self.execute_full_pipeline(
            countries=['us'],
            categories=['technology'],
            max_articles_per_category=max_articles
        )
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            temp_dir = os.path.join(self.output_dir, 'temp')
            
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
                os.makedirs(temp_dir, exist_ok=True)
                
                self.logger.info("🧹 Temporary files cleaned up")
                
        except Exception as e:
            self.logger.warning(f"Could not clean up temp files: {e}")

# For backward compatibility
class NewsToReelsGenerator(EnhancedPipeline):
    """Legacy compatibility wrapper"""
    
    def run_pipeline(self, countries=['us', 'in'], categories=['general'], 
                    articles_per_country=5, topics=None):
        """Legacy method signature"""
        stats, articles = self.execute_full_pipeline(
            countries=countries,
            categories=categories,
            max_articles_per_category=articles_per_country
        )
        
        return articles
