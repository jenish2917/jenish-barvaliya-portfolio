"""
Quality Analysis Service
Comprehensive quality assessment for news reels including content, audio, and video analysis
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass
import json
from datetime import datetime
import statistics
from pathlib import Path

# Text analysis
try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

load_dotenv('config.env')

@dataclass
class QualityMetrics:
    """Comprehensive quality metrics for a news reel"""
    content_quality: float
    audio_quality: float
    video_quality: float
    overall_quality: float
    engagement_score: float
    readability_score: float
    technical_score: float
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        return {
            'content_quality': self.content_quality,
            'audio_quality': self.audio_quality,
            'video_quality': self.video_quality,
            'overall_quality': self.overall_quality,
            'engagement_score': self.engagement_score,
            'readability_score': self.readability_score,
            'technical_score': self.technical_score,
            'recommendations': self.recommendations
        }

@dataclass
class ContentAnalysis:
    """Detailed content analysis"""
    word_count: int
    sentence_count: int
    reading_level: str
    sentiment_score: float
    keyword_density: float
    hook_quality: float
    conclusion_quality: float
    
    def to_dict(self) -> Dict:
        return {
            'word_count': self.word_count,
            'sentence_count': self.sentence_count,
            'reading_level': self.reading_level,
            'sentiment_score': self.sentiment_score,
            'keyword_density': self.keyword_density,
            'hook_quality': self.hook_quality,
            'conclusion_quality': self.conclusion_quality
        }

class QualityAnalyzer:
    def __init__(self):
        self.logger = self._setup_logger()
        self.quality_threshold = float(os.getenv('QUALITY_THRESHOLD', '75'))
        
        # Initialize text analysis tools
        self._init_text_analysis()
        
        # Quality weights
        self.content_weight = 0.4
        self.audio_weight = 0.3
        self.video_weight = 0.3
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for quality analyzer"""
        logger = logging.getLogger('QualityAnalyzer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _init_text_analysis(self):
        """Initialize text analysis tools"""
        self.nlp = None
        
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                self.logger.info("Spacy model loaded successfully")
            except OSError:
                self.logger.warning("Spacy model 'en_core_web_sm' not found. Install with: python -m spacy download en_core_web_sm")
        
        if TEXTSTAT_AVAILABLE:
            self.logger.info("Textstat available for readability analysis")
        else:
            self.logger.warning("Textstat not available. Install with: pip install textstat")
    
    def analyze_reel_quality(self, 
                           article: Dict, 
                           audio_metrics: Dict = None, 
                           video_path: str = None) -> QualityMetrics:
        """
        Perform comprehensive quality analysis of a news reel
        
        Args:
            article: Article data with content, script, etc.
            audio_metrics: Audio quality metrics
            video_path: Path to generated video file
            
        Returns:
            QualityMetrics object with detailed analysis
        """
        try:
            self.logger.info(f"Analyzing quality for: {article.get('title', 'Unknown')[:50]}...")
            
            # Analyze content quality
            content_quality, content_analysis = self._analyze_content_quality(article)
            
            # Analyze audio quality
            audio_quality = self._analyze_audio_quality(audio_metrics) if audio_metrics else 50.0
            
            # Analyze video quality
            video_quality = self._analyze_video_quality(video_path) if video_path else 50.0
            
            # Calculate derived scores
            overall_quality = self._calculate_overall_quality(content_quality, audio_quality, video_quality)
            engagement_score = self._calculate_engagement_score(article, content_analysis)
            readability_score = self._calculate_readability_score(article.get('script', ''))
            technical_score = self._calculate_technical_score(audio_metrics, video_path)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                content_quality, audio_quality, video_quality, 
                content_analysis, article
            )
            
            metrics = QualityMetrics(
                content_quality=round(content_quality, 1),
                audio_quality=round(audio_quality, 1),
                video_quality=round(video_quality, 1),
                overall_quality=round(overall_quality, 1),
                engagement_score=round(engagement_score, 1),
                readability_score=round(readability_score, 1),
                technical_score=round(technical_score, 1),
                recommendations=recommendations
            )
            
            self.logger.info(f"Quality analysis complete - Overall: {overall_quality:.1f}%")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error analyzing quality: {e}")
            return self._default_metrics()
    
    def _analyze_content_quality(self, article: Dict) -> Tuple[float, ContentAnalysis]:
        """Analyze content quality and structure"""
        title = article.get('title', '')
        summary = article.get('summary', '')
        script = article.get('script', '')
        content = article.get('content', '') or article.get('description', '')
        
        score = 0.0
        
        # Title quality (20%)
        title_score = self._analyze_title_quality(title)
        score += title_score * 0.2
        
        # Summary quality (25%)
        summary_score = self._analyze_summary_quality(summary)
        score += summary_score * 0.25
        
        # Script quality (35%)
        script_score = self._analyze_script_quality(script)
        score += script_score * 0.35
        
        # Content completeness (20%)
        content_score = self._analyze_content_completeness(content)
        score += content_score * 0.2
        
        # Detailed content analysis
        content_analysis = self._detailed_content_analysis(script)
        
        return min(score, 100.0), content_analysis
    
    def _analyze_title_quality(self, title: str) -> float:
        """Analyze title quality"""
        if not title:
            return 0.0
        
        score = 0.0
        
        # Length check (optimal: 40-60 characters)
        if 40 <= len(title) <= 60:
            score += 40
        elif 30 <= len(title) < 40 or 60 < len(title) <= 80:
            score += 30
        else:
            score += 20
        
        # Word count (optimal: 6-10 words)
        word_count = len(title.split())
        if 6 <= word_count <= 10:
            score += 30
        elif 4 <= word_count < 6 or 10 < word_count <= 12:
            score += 20
        else:
            score += 10
        
        # Engagement factors
        engagement_words = ['breaking', 'exclusive', 'urgent', 'major', 'shocking', 'revealed']
        if any(word.lower() in title.lower() for word in engagement_words):
            score += 15
        
        # Clear and specific
        if title.count(':') <= 1 and not title.endswith('...'):
            score += 15
        
        return min(score, 100.0)
    
    def _analyze_summary_quality(self, summary: str) -> float:
        """Analyze summary quality"""
        if not summary:
            return 0.0
        
        score = 0.0
        
        # Length check (optimal: 150-400 characters)
        if 150 <= len(summary) <= 400:
            score += 40
        elif 100 <= len(summary) < 150 or 400 < len(summary) <= 500:
            score += 30
        else:
            score += 20
        
        # Sentence count (optimal: 3-5 sentences)
        sentence_count = len([s for s in summary.split('.') if s.strip()])
        if 3 <= sentence_count <= 5:
            score += 30
        elif 2 <= sentence_count < 3 or 5 < sentence_count <= 7:
            score += 20
        else:
            score += 10
        
        # Information density
        if len(summary.split()) > 30:  # At least 30 words
            score += 30
        else:
            score += 15
        
        return min(score, 100.0)
    
    def _analyze_script_quality(self, script: str) -> float:
        """Analyze script quality for spoken content"""
        if not script:
            return 0.0
        
        score = 0.0
        
        # Length check (optimal: 120-250 words for 30-60 second video)
        word_count = len(script.split())
        if 120 <= word_count <= 250:
            score += 30
        elif 100 <= word_count < 120 or 250 < word_count <= 300:
            score += 25
        else:
            score += 15
        
        # Hook quality (first sentence)
        first_sentence = script.split('.')[0] if '.' in script else script[:100]
        hook_score = self._analyze_hook_quality(first_sentence)
        score += hook_score * 0.25
        
        # Conversational tone
        conversational_words = ['here\'s', 'you', 'we', 'let\'s', 'this is', 'what\'s']
        if any(word in script.lower() for word in conversational_words):
            score += 15
        
        # Clear structure
        if script.count('.') >= 2:  # At least 3 sentences
            score += 15
        
        # Avoid complex words
        if TEXTSTAT_AVAILABLE:
            flesch_score = textstat.flesch_reading_ease(script)
            if flesch_score > 60:  # Easy to read
                score += 15
            elif flesch_score > 30:
                score += 10
            else:
                score += 5
        else:
            score += 10  # Default if textstat not available
        
        return min(score, 100.0)
    
    def _analyze_content_completeness(self, content: str) -> float:
        """Analyze content completeness"""
        if not content:
            return 0.0
        
        score = 0.0
        
        # Content length
        if len(content) > 500:
            score += 50
        elif len(content) > 200:
            score += 40
        elif len(content) > 100:
            score += 30
        else:
            score += 20
        
        # Information richness
        if len(content.split()) > 100:
            score += 30
        elif len(content.split()) > 50:
            score += 20
        else:
            score += 10
        
        # Avoid placeholder content
        placeholders = ['[removed]', 'subscribe', 'login', 'paywall']
        has_placeholder = any(p in content.lower() for p in placeholders)
        if not has_placeholder:
            score += 20
        
        return min(score, 100.0)
    
    def _analyze_hook_quality(self, hook: str) -> float:
        """Analyze the quality of the opening hook"""
        if not hook:
            return 0.0
        
        score = 0.0
        
        # Length check (optimal: 10-25 words)
        word_count = len(hook.split())
        if 10 <= word_count <= 25:
            score += 40
        elif 8 <= word_count < 10 or 25 < word_count <= 30:
            score += 30
        else:
            score += 20
        
        # Engagement starters
        engagement_starters = [
            'breaking', 'here\'s what', 'this just in', 'you won\'t believe',
            'major news', 'exclusive', 'urgent update', 'happening now'
        ]
        if any(starter in hook.lower() for starter in engagement_starters):
            score += 30
        
        # Location/source mention
        if any(word in hook.lower() for word in ['from', 'in', 'at']):
            score += 15
        
        # Clear and direct
        if hook.endswith((':' )) or 'what' in hook.lower():
            score += 15
        
        return min(score, 100.0)
    
    def _detailed_content_analysis(self, script: str) -> ContentAnalysis:
        """Perform detailed content analysis"""
        if not script:
            return ContentAnalysis(0, 0, 'Unknown', 0.0, 0.0, 0.0, 0.0)
        
        word_count = len(script.split())
        sentence_count = len([s for s in script.split('.') if s.strip()])
        
        # Reading level
        reading_level = 'Unknown'
        if TEXTSTAT_AVAILABLE:
            flesch_score = textstat.flesch_reading_ease(script)
            if flesch_score >= 90:
                reading_level = 'Very Easy'
            elif flesch_score >= 80:
                reading_level = 'Easy'
            elif flesch_score >= 70:
                reading_level = 'Fairly Easy'
            elif flesch_score >= 60:
                reading_level = 'Standard'
            elif flesch_score >= 50:
                reading_level = 'Fairly Difficult'
            else:
                reading_level = 'Difficult'
        
        # Sentiment analysis (basic)
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'win', 'improve']
        negative_words = ['bad', 'terrible', 'negative', 'fail', 'crisis', 'problem', 'decline']
        
        pos_count = sum(1 for word in positive_words if word in script.lower())
        neg_count = sum(1 for word in negative_words if word in script.lower())
        sentiment_score = (pos_count - neg_count) / max(word_count / 10, 1)
        
        # Keyword density (simplified)
        unique_words = set(script.lower().split())
        keyword_density = len(unique_words) / word_count if word_count > 0 else 0
        
        # Hook and conclusion quality
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        hook_quality = self._analyze_hook_quality(sentences[0]) if sentences else 0.0
        conclusion_quality = self._analyze_conclusion_quality(sentences[-1]) if sentences else 0.0
        
        return ContentAnalysis(
            word_count=word_count,
            sentence_count=sentence_count,
            reading_level=reading_level,
            sentiment_score=round(sentiment_score, 2),
            keyword_density=round(keyword_density, 3),
            hook_quality=round(hook_quality, 1),
            conclusion_quality=round(conclusion_quality, 1)
        )
    
    def _analyze_conclusion_quality(self, conclusion: str) -> float:
        """Analyze the quality of the conclusion"""
        if not conclusion:
            return 0.0
        
        score = 0.0
        
        # Strong ending words
        strong_endings = ['impact', 'future', 'important', 'remember', 'stay tuned', 'developing']
        if any(ending in conclusion.lower() for ending in strong_endings):
            score += 40
        
        # Call to action or thought-provoking
        cta_words = ['what do you think', 'let us know', 'share', 'comment']
        if any(cta in conclusion.lower() for cta in cta_words):
            score += 30
        
        # Appropriate length
        word_count = len(conclusion.split())
        if 5 <= word_count <= 15:
            score += 30
        elif 3 <= word_count < 5 or 15 < word_count <= 20:
            score += 20
        else:
            score += 10
        
        return min(score, 100.0)
    
    def _analyze_audio_quality(self, audio_metrics: Dict) -> float:
        """Analyze audio quality from metrics"""
        if not audio_metrics:
            return 50.0
        
        return audio_metrics.get('quality_score', 50.0)
    
    def _analyze_video_quality(self, video_path: str) -> float:
        """Analyze video quality (basic implementation)"""
        if not video_path or not os.path.exists(video_path):
            return 50.0
        
        score = 0.0
        
        # File size check (rough quality indicator)
        file_size = os.path.getsize(video_path)
        if file_size > 5 * 1024 * 1024:  # > 5MB
            score += 40
        elif file_size > 2 * 1024 * 1024:  # > 2MB
            score += 30
        else:
            score += 20
        
        # File exists and is not empty
        if file_size > 0:
            score += 30
        
        # Proper extension
        if video_path.lower().endswith('.mp4'):
            score += 30
        
        return min(score, 100.0)
    
    def _calculate_overall_quality(self, content: float, audio: float, video: float) -> float:
        """Calculate weighted overall quality score"""
        return (content * self.content_weight + 
                audio * self.audio_weight + 
                video * self.video_weight)
    
    def _calculate_engagement_score(self, article: Dict, content_analysis: ContentAnalysis) -> float:
        """Calculate predicted engagement score"""
        score = 0.0
        
        # Hook quality impact
        score += content_analysis.hook_quality * 0.3
        
        # Conclusion quality impact
        score += content_analysis.conclusion_quality * 0.2
        
        # Reading level (easier = more engaging)
        reading_levels = {
            'Very Easy': 100, 'Easy': 90, 'Fairly Easy': 80,
            'Standard': 70, 'Fairly Difficult': 50, 'Difficult': 30
        }
        score += reading_levels.get(content_analysis.reading_level, 60) * 0.2
        
        # Category engagement potential
        category = article.get('category', '').lower()
        category_scores = {
            'technology': 85, 'sports': 80, 'entertainment': 90,
            'business': 70, 'health': 75, 'general': 65
        }
        score += category_scores.get(category, 65) * 0.15
        
        # Sentiment impact (slightly positive is engaging)
        sentiment_score = content_analysis.sentiment_score
        if 0.1 <= sentiment_score <= 0.5:
            score += 85 * 0.15
        elif -0.2 <= sentiment_score < 0.1:
            score += 75 * 0.15
        else:
            score += 60 * 0.15
        
        return min(score, 100.0)
    
    def _calculate_readability_score(self, script: str) -> float:
        """Calculate readability score"""
        if not script or not TEXTSTAT_AVAILABLE:
            return 60.0
        
        flesch_score = textstat.flesch_reading_ease(script)
        return min(max(flesch_score, 0), 100)
    
    def _calculate_technical_score(self, audio_metrics: Dict, video_path: str) -> float:
        """Calculate technical quality score"""
        score = 0.0
        
        # Audio technical quality (60%)
        if audio_metrics:
            audio_tech_score = 0.0
            
            # Sample rate
            sample_rate = audio_metrics.get('sample_rate', 0)
            if sample_rate >= 44100:
                audio_tech_score += 25
            elif sample_rate >= 22050:
                audio_tech_score += 20
            else:
                audio_tech_score += 10
            
            # Bit rate
            bit_rate = audio_metrics.get('bit_rate', 0)
            if bit_rate >= 192000:
                audio_tech_score += 25
            elif bit_rate >= 128000:
                audio_tech_score += 20
            else:
                audio_tech_score += 10
            
            # Duration appropriateness
            duration = audio_metrics.get('duration', 0)
            if 25 <= duration <= 60:
                audio_tech_score += 25
            elif 20 <= duration < 25 or 60 < duration <= 75:
                audio_tech_score += 20
            else:
                audio_tech_score += 10
            
            # RMS energy levels
            rms = audio_metrics.get('rms_energy', 0)
            if 0.05 <= rms <= 0.3:
                audio_tech_score += 25
            else:
                audio_tech_score += 15
            
            score += audio_tech_score * 0.6
        else:
            score += 30  # Default if no audio metrics
        
        # Video technical quality (40%)
        video_tech_score = self._analyze_video_quality(video_path)
        score += video_tech_score * 0.4
        
        return min(score, 100.0)
    
    def _generate_recommendations(self, 
                                 content_quality: float, 
                                 audio_quality: float, 
                                 video_quality: float,
                                 content_analysis: ContentAnalysis,
                                 article: Dict) -> List[str]:
        """Generate specific recommendations for improvement"""
        recommendations = []
        
        # Content recommendations
        if content_quality < 70:
            if content_analysis.word_count < 120:
                recommendations.append("Script is too short - aim for 120-250 words for better engagement")
            elif content_analysis.word_count > 300:
                recommendations.append("Script is too long - consider condensing to 120-250 words")
            
            if content_analysis.hook_quality < 60:
                recommendations.append("Improve opening hook - start with engaging phrases like 'Breaking news' or 'Here's what's happening'")
            
            if content_analysis.conclusion_quality < 60:
                recommendations.append("Strengthen conclusion - end with impact or call-to-action")
            
            if content_analysis.reading_level in ['Difficult', 'Fairly Difficult']:
                recommendations.append("Simplify language for better accessibility - use shorter sentences and common words")
        
        # Audio recommendations
        if audio_quality < 70:
            recommendations.append("Consider using a higher quality TTS service or adjusting voice settings")
            recommendations.append("Ensure script is optimized for speech - replace abbreviations and complex terms")
        
        # Video recommendations
        if video_quality < 70:
            recommendations.append("Check video generation settings - ensure high quality output")
            recommendations.append("Verify all visual elements are properly rendered")
        
        # Overall recommendations
        overall = (content_quality + audio_quality + video_quality) / 3
        if overall < self.quality_threshold:
            recommendations.append(f"Overall quality ({overall:.1f}%) is below threshold ({self.quality_threshold}%) - review all components")
        
        # Category-specific recommendations
        category = article.get('category', '').lower()
        if category == 'technology' and content_analysis.word_count < 150:
            recommendations.append("Technology news often benefits from slightly longer explanations")
        elif category == 'sports' and content_analysis.sentiment_score < 0:
            recommendations.append("Sports content performs better with enthusiastic, positive tone")
        
        return recommendations
    
    def _default_metrics(self) -> QualityMetrics:
        """Return default metrics in case of error"""
        return QualityMetrics(
            content_quality=50.0,
            audio_quality=50.0,
            video_quality=50.0,
            overall_quality=50.0,
            engagement_score=50.0,
            readability_score=60.0,
            technical_score=50.0,
            recommendations=["Unable to analyze quality - please check input data"]
        )
    
    def analyze_batch_quality(self, articles_data: List[Dict]) -> List[QualityMetrics]:
        """Analyze quality for multiple articles"""
        quality_results = []
        
        self.logger.info(f"Analyzing quality for {len(articles_data)} articles...")
        
        for i, article_data in enumerate(articles_data, 1):
            self.logger.info(f"Quality analysis {i}/{len(articles_data)}")
            
            audio_metrics = article_data.get('audio_metrics', {})
            video_path = article_data.get('video_path', '')
            
            quality_metrics = self.analyze_reel_quality(
                article_data, 
                audio_metrics, 
                video_path
            )
            
            quality_results.append(quality_metrics)
        
        # Calculate batch statistics
        if quality_results:
            avg_quality = statistics.mean(m.overall_quality for m in quality_results)
            self.logger.info(f"Batch quality analysis complete - Average quality: {avg_quality:.1f}%")
        
        return quality_results
    
    def save_quality_report(self, 
                           articles_data: List[Dict], 
                           quality_metrics: List[QualityMetrics], 
                           output_dir: str) -> str:
        """Save comprehensive quality report"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Combine article data with quality metrics
        detailed_results = []
        for article, metrics in zip(articles_data, quality_metrics):
            detailed_results.append({
                'title': article.get('title', ''),
                'country': article.get('country', ''),
                'category': article.get('category', ''),
                'audio_path': article.get('audio_path', ''),
                'video_path': article.get('video_path', ''),
                'quality_metrics': metrics.to_dict()
            })
        
        # Calculate summary statistics
        if quality_metrics:
            summary_stats = {
                'total_articles': len(quality_metrics),
                'average_overall_quality': round(statistics.mean(m.overall_quality for m in quality_metrics), 1),
                'average_content_quality': round(statistics.mean(m.content_quality for m in quality_metrics), 1),
                'average_audio_quality': round(statistics.mean(m.audio_quality for m in quality_metrics), 1),
                'average_video_quality': round(statistics.mean(m.video_quality for m in quality_metrics), 1),
                'average_engagement_score': round(statistics.mean(m.engagement_score for m in quality_metrics), 1),
                'articles_above_threshold': len([m for m in quality_metrics if m.overall_quality >= self.quality_threshold]),
                'quality_distribution': {
                    'excellent (90-100%)': len([m for m in quality_metrics if m.overall_quality >= 90]),
                    'good (80-89%)': len([m for m in quality_metrics if 80 <= m.overall_quality < 90]),
                    'fair (70-79%)': len([m for m in quality_metrics if 70 <= m.overall_quality < 80]),
                    'poor (60-69%)': len([m for m in quality_metrics if 60 <= m.overall_quality < 70]),
                    'very_poor (<60%)': len([m for m in quality_metrics if m.overall_quality < 60])
                }
            }
        else:
            summary_stats = {'total_articles': 0}
        
        report = {
            'analysis_time': datetime.now().isoformat(),
            'quality_threshold': self.quality_threshold,
            'summary_statistics': summary_stats,
            'detailed_results': detailed_results
        }
        
        report_path = os.path.join(output_dir, f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved quality report to {report_path}")
        
        # Also save a human-readable summary
        summary_path = os.path.join(output_dir, f"quality_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        self._save_human_readable_summary(summary_stats, detailed_results, summary_path)
        
        return report_path
    
    def _save_human_readable_summary(self, summary_stats: Dict, detailed_results: List[Dict], output_path: str):
        """Save a human-readable quality summary"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("📊 NEWS REELS QUALITY ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📰 Total Articles Analyzed: {summary_stats.get('total_articles', 0)}\n\n")
            
            if summary_stats.get('total_articles', 0) > 0:
                f.write("📈 AVERAGE QUALITY SCORES\n")
                f.write("-" * 30 + "\n")
                f.write(f"Overall Quality: {summary_stats.get('average_overall_quality', 0)}%\n")
                f.write(f"Content Quality: {summary_stats.get('average_content_quality', 0)}%\n")
                f.write(f"Audio Quality: {summary_stats.get('average_audio_quality', 0)}%\n")
                f.write(f"Video Quality: {summary_stats.get('average_video_quality', 0)}%\n")
                f.write(f"Engagement Score: {summary_stats.get('average_engagement_score', 0)}%\n\n")
                
                f.write("📊 QUALITY DISTRIBUTION\n")
                f.write("-" * 30 + "\n")
                distribution = summary_stats.get('quality_distribution', {})
                for level, count in distribution.items():
                    f.write(f"{level}: {count} articles\n")
                
                f.write(f"\n✅ Articles Above Threshold: {summary_stats.get('articles_above_threshold', 0)}\n\n")
                
                f.write("🔍 TOP RECOMMENDATIONS\n")
                f.write("-" * 30 + "\n")
                
                # Collect all recommendations
                all_recommendations = []
                for result in detailed_results:
                    recommendations = result.get('quality_metrics', {}).get('recommendations', [])
                    all_recommendations.extend(recommendations)
                
                # Count frequency of recommendations
                rec_counts = {}
                for rec in all_recommendations:
                    rec_counts[rec] = rec_counts.get(rec, 0) + 1
                
                # Show top 5 most common recommendations
                sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                for i, (rec, count) in enumerate(sorted_recs, 1):
                    f.write(f"{i}. {rec} ({count} articles)\n")
        
        self.logger.info(f"Saved human-readable summary to {output_path}")

# Legacy compatibility
class VideoAnalyzer(QualityAnalyzer):
    """Backward compatibility wrapper"""
    pass
