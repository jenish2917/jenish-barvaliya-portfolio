#!/usr/bin/env python3
"""
Simplified Daily News Reel Generator
===================================

Audio-focused system that:
1. Fetches today's top news from RSS feeds
2. Generates engaging scripts with geographic context
3. Creates accent-aware TTS with location detection
4. Produces complete audio reels with regional accents

Usage: python simple_daily_reel.py
"""

import os
import sys
import json
from datetime import datetime
import logging
from typing import List, Dict, Optional

# Import our enhanced components
from enhanced_rss_service import EnhancedRSSService, ArticleContent
from engaging_script_generator import EngagingScriptGenerator
from accent_aware_tts import AccentAwareTTS

class SimpleDailyReelGenerator:
    """Audio-focused daily news reel generation system with full article summarization"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger('SimpleDailyReelGenerator')
        
        # Initialize enhanced components
        self.news_service = EnhancedRSSService()
        self.script_generator = EngagingScriptGenerator()
        self.tts_generator = AccentAwareTTS()
        
        # Create output directories
        self.ensure_directories()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('output/logs/daily_reel.log'),
                logging.StreamHandler()
            ]
        )
    
    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        directories = [
            'output/reels',
            'output/audio', 
            'output/scripts',
            'output/logs',
            'output/reports'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate_daily_reel(self, max_stories: int = 5) -> Dict:
        """Generate complete daily news reel with geographic accents"""
        
        self.logger.info("Starting Daily News Reel Generation with Geographic Accents")
        self.logger.info("=" * 70)
        
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            'session_id': session_id,
            'date': datetime.now().isoformat(),
            'stories': [],
            'audio_files': [],
            'errors': []
        }
        
        try:
            # Step 1: Fetch and summarize today's top news articles
            self.logger.info("Fetching and summarizing today's top news articles...")
            articles = self.news_service.fetch_and_summarize_news(
                max_articles=max_stories,
                category='general',
                hours_back=24,
                min_word_count=200
            )
            
            if not articles:
                raise Exception("No articles found or summarized successfully")
            
            self.logger.info(f"Successfully processed {len(articles)} articles with full summaries")
            
            # Step 2: Generate enhanced scripts with geographic context
            self.logger.info("Generating engaging scripts from comprehensive summaries...")
            
            for i, article in enumerate(articles, 1):
                story_data = self._process_enhanced_article(article, i, session_id)
                results['stories'].append(story_data)
                
                if story_data['audio_file']:
                    results['audio_files'].append(story_data['audio_file'])
                if story_data.get('error'):
                    results['errors'].append(story_data['error'])
            
            # Step 4: Create combined reel
            if results['audio_files']:
                combined_audio = self._create_combined_audio(results['audio_files'], session_id)
                results['combined_audio'] = combined_audio
            
            # Step 5: Generate session report
            report_file = self._generate_session_report(results, session_id)
            results['report_file'] = report_file
            
            self.logger.info("Daily News Reel Generation Complete!")
            self.logger.info(f"Generated {len(results['stories'])} stories with geographic accents")
            self.logger.info(f"Created {len(results['audio_files'])} accent-aware audio files")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in daily reel generation: {e}")
            results['errors'].append(str(e))
            return results
    
    def _select_diverse_stories(self, articles: List[Dict], max_stories: int) -> List[Dict]:
        """Select diverse stories from different categories and regions"""
        
        # Categorize articles by source region and topic
        categorized = {
            'breaking': [],
            'tech': [],
            'business': [],
            'international': [],
            'sports': [],
            'entertainment': [],
            'other': []
        }
        
        for article in articles:
            title = article.get('title', '').lower()
            
            # Categorize by content
            if any(word in title for word in ['breaking', 'urgent', 'alert']):
                categorized['breaking'].append(article)
            elif any(word in title for word in ['tech', 'ai', 'software', 'startup']):
                categorized['tech'].append(article)
            elif any(word in title for word in ['market', 'economic', 'financial', 'business']):
                categorized['business'].append(article)
            elif any(word in title for word in ['sports', 'football', 'basketball', 'soccer']):
                categorized['sports'].append(article)
            elif any(word in title for word in ['celebrity', 'movie', 'entertainment', 'hollywood']):
                categorized['entertainment'].append(article)
            elif any(word in title for word in ['global', 'international', 'world']):
                categorized['international'].append(article)
            else:
                categorized['other'].append(article)
        
        # Select diverse stories ensuring geographic and topical variety
        selected = []
        
        # Priority order for categories
        priority_categories = ['breaking', 'international', 'tech', 'business', 'sports', 'entertainment', 'other']
        
        for category in priority_categories:
            if len(selected) >= max_stories:
                break
                
            category_articles = categorized[category]
            if category_articles:
                # Sort by engagement score and take top article
                category_articles.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)
                selected.append(category_articles[0])
        
        # Fill remaining slots with highest engagement articles
        remaining_articles = [a for a in articles if a not in selected]
        remaining_articles.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)
        
        while len(selected) < max_stories and remaining_articles:
            selected.append(remaining_articles.pop(0))
        
        return selected[:max_stories]
    
    def _process_single_story(self, article: Dict, story_number: int, session_id: str) -> Dict:
        """Process a single story with geographic accent awareness"""
        
        story_data = {
            'number': story_number,
            'title': article.get('title', 'Unknown'),
            'source': article.get('source', 'Unknown'),
            'url': article.get('link', ''),
            'geographic_location': None,
            'detected_accent': None,
            'emotion': None,
            'script': None,
            'audio_file': None,
            'error': None
        }
        
        try:
            self.logger.info(f"Processing Story {story_number}: {story_data['title'][:60]}...")
            self.logger.info(f"Source: {story_data['source']}")
            
            # Step 1: Generate engaging script
            script_data = self.script_generator.enhance_script(
                original_script=article.get('description', ''),
                article_data={
                    'title': article.get('title', ''),
                    'category': self._detect_category(article.get('title', '')),
                    'source': article.get('source', '')
                }
            )
            
            if not script_data:
                raise Exception("Failed to generate script")
            
            story_data['script'] = script_data
            self.logger.info(f"Generated engaging script ({len(story_data['script'])} chars)")
            
            # Step 2: Detect geographic location and emotion
            location, confidence = self.tts_generator._detect_geographic_location(
                story_data['script'], 
                story_data['source']
            )
            
            emotion = self.tts_generator._detect_emotion_from_content(story_data['script'])
            
            story_data['geographic_location'] = location
            story_data['emotion'] = emotion
            
            if location in self.tts_generator.location_accent_mapping:
                story_data['detected_accent'] = self.tts_generator.location_accent_mapping[location]['accent']
            
            self.logger.info(f"Detected location: {location} (confidence: {confidence:.1%})")
            self.logger.info(f"Detected emotion: {emotion}")
            self.logger.info(f"Using accent: {story_data['detected_accent']}")
            
            # Step 3: Generate accent-aware audio
            audio_filename = f"story_{story_number:02d}_{session_id}.wav"
            audio_path = os.path.join('output/audio', audio_filename)
            
            success = self.tts_generator.generate_contextual_audio(
                text=story_data['script'],
                output_path=audio_path,
                category=self._detect_category(article.get('title', '')),
                emotion='auto',  # Auto-detect
                news_source=story_data['source']
            )
            
            if success:
                story_data['audio_file'] = audio_path
                self.logger.info(f"Generated accent-aware audio: {audio_filename}")
            else:
                raise Exception("Failed to generate audio")
            
            self.logger.info(f"Story {story_number} processed successfully")
            
        except Exception as e:
            error_msg = f"Story {story_number} error: {e}"
            self.logger.error(f"ERROR: {error_msg}")
            story_data['error'] = error_msg
        
        return story_data
    
    def _process_enhanced_article(self, article: ArticleContent, story_number: int, session_id: str) -> Dict:
        """Process a single article with comprehensive summary and geographic accents"""
        
        story_data = {
            'story_number': story_number,
            'title': article.title,
            'source': article.source,
            'summary': article.summary,
            'word_count': article.word_count,
            'url': article.url,
            'category': article.category,
            'engagement_score': article.engagement_score,
            'geographic_location': None,
            'detected_accent': 'unknown',
            'emotion': None,
            'script': None,
            'audio_file': None,
            'error': None
        }
        
        try:
            self.logger.info(f"Processing Story {story_number}: {story_data['title'][:60]}...")
            self.logger.info(f"Source: {story_data['source']}")
            self.logger.info(f"Summary length: {len(article.summary)} chars, Full article: {article.word_count} words")
            
            # Step 1: Create engaging script from comprehensive summary
            enhanced_script = self.script_generator.enhance_script(
                original_script=article.summary, 
                article_data={
                    'title': article.title,
                    'category': article.category,
                    'source': article.source
                }
            )
            
            if not enhanced_script:
                raise Exception("Failed to enhance script")
            
            story_data['script'] = enhanced_script
            self.logger.info(f"Enhanced script ({len(enhanced_script)} chars)")
            
            # Step 2: Detect geographic location and emotion from comprehensive content
            location, confidence = self.tts_generator._detect_geographic_location(
                enhanced_script, 
                story_data['source']
            )
            
            emotion = self.tts_generator._detect_emotion_from_content(enhanced_script)
            
            story_data['geographic_location'] = location
            story_data['emotion'] = emotion
            
            if location in self.tts_generator.location_accent_mapping:
                story_data['detected_accent'] = self.tts_generator.location_accent_mapping[location]['accent']
            
            self.logger.info(f"Detected location: {location} (confidence: {confidence:.1%})")
            self.logger.info(f"Detected emotion: {emotion}")
            self.logger.info(f"Using accent: {story_data['detected_accent']}")
            
            # Step 3: Generate accent-aware audio from enhanced script
            audio_filename = f"enhanced_story_{story_number:02d}_{session_id}.wav"
            audio_path = os.path.join('output/audio', audio_filename)
            
            success = self.tts_generator.generate_contextual_audio(
                text=enhanced_script,
                output_path=audio_path,
                category=article.category,
                emotion='auto',  # Auto-detect
                news_source=story_data['source']
            )
            
            if success:
                story_data['audio_file'] = audio_path
                self.logger.info(f"Generated comprehensive accent-aware audio: {audio_filename}")
            else:
                raise Exception("Failed to generate audio")
            
            self.logger.info(f"Story {story_number} processed successfully with full article content")
            
        except Exception as e:
            error_msg = f"Story {story_number} error: {e}"
            self.logger.error(f"ERROR: {error_msg}")
            story_data['error'] = error_msg
        
        return story_data
    
    def _detect_category(self, title: str) -> str:
        """Detect story category from title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['breaking', 'urgent', 'alert']):
            return 'breaking_news'
        elif any(word in title_lower for word in ['tech', 'ai', 'software', 'computer']):
            return 'tech_news'
        elif any(word in title_lower for word in ['market', 'economic', 'business', 'financial']):
            return 'business_news'
        elif any(word in title_lower for word in ['sports', 'game', 'player', 'team']):
            return 'sports'
        elif any(word in title_lower for word in ['celebrity', 'movie', 'entertainment']):
            return 'entertainment'
        else:
            return 'international'
    
    def _create_combined_audio(self, audio_files: List[str], session_id: str) -> str:
        """Combine all story audio files into a single reel"""
        try:
            from pydub import AudioSegment
            
            combined = AudioSegment.empty()
            intro_pause = AudioSegment.silent(duration=1000)  # 1 second pause
            story_pause = AudioSegment.silent(duration=2000)  # 2 second pause between stories
            
            for i, audio_file in enumerate(audio_files):
                if os.path.exists(audio_file):
                    segment = AudioSegment.from_wav(audio_file)
                    
                    if i == 0:
                        combined += intro_pause
                    else:
                        combined += story_pause
                    
                    combined += segment
            
            # Add outro pause
            combined += intro_pause
            
            # Export combined audio
            output_path = f"output/reels/daily_reel_{session_id}.wav"
            combined.export(output_path, format="wav")
            
            self.logger.info(f"🎵 Combined audio reel created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating combined audio: {e}")
            return ""
    
    def _generate_session_report(self, results: Dict, session_id: str) -> str:
        """Generate comprehensive session report"""
        
        report = {
            'session_id': session_id,
            'generation_date': datetime.now().isoformat(),
            'summary': {
                'total_stories': len(results['stories']),
                'successful_audio': len(results['audio_files']),
                'errors': len(results['errors'])
            },
            'geographic_distribution': {},
            'emotion_distribution': {},
            'accent_distribution': {},
            'stories': results['stories'],
            'errors': results['errors']
        }
        
        # Analyze geographic distribution
        for story in results['stories']:
            location = story.get('geographic_location', 'unknown')
            if location not in report['geographic_distribution']:
                report['geographic_distribution'][location] = 0
            report['geographic_distribution'][location] += 1
        
        # Analyze emotion distribution
        for story in results['stories']:
            emotion = story.get('emotion', 'unknown')
            if emotion not in report['emotion_distribution']:
                report['emotion_distribution'][emotion] = 0
            report['emotion_distribution'][emotion] += 1
        
        # Analyze accent distribution
        for story in results['stories']:
            accent = story.get('detected_accent', 'unknown')
            if accent not in report['accent_distribution']:
                report['accent_distribution'][accent] = 0
            report['accent_distribution'][accent] += 1
        
        # Save report
        report_path = f"output/reports/daily_reel_report_{session_id}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Session report generated: {report_path}")
        return report_path

def main():
    """Main function to generate today's news reel"""
    
    print("🌍 DAILY NEWS REEL GENERATOR WITH GEOGRAPHIC ACCENTS")
    print("=" * 60)
    print("🎯 Automatically detects news location and applies appropriate accents")
    print("🗣️ Supports US, UK, Australia, India, Canada, South Africa, New Zealand, Ireland")
    print()
    
    generator = SimpleDailyReelGenerator()
    
    # Configure generation parameters
    max_stories = 5
    
    print(f"📰 Generating reel with {max_stories} stories...")
    print()
    
    # Generate the daily reel
    results = generator.generate_daily_reel(max_stories=max_stories)
    
    # Display results
    print("\n🎉 GENERATION COMPLETE!")
    print("=" * 40)
    print(f"✅ Stories processed: {len(results['stories'])}")
    print(f"🎵 Audio files created: {len(results['audio_files'])}")
    print(f"❌ Errors encountered: {len(results['errors'])}")
    
    if results.get('combined_audio'):
        print(f"🎵 Combined audio reel: {results['combined_audio']}")
    
    if results.get('report_file'):
        print(f"📊 Detailed report: {results['report_file']}")
    
    print(f"\n🌍 Geographic Accent Distribution:")
    location_counts = {}
    for story in results['stories']:
        location = story.get('geographic_location', 'unknown')
        location_counts[location] = location_counts.get(location, 0) + 1
    
    for location, count in location_counts.items():
        accent = 'unknown'
        if location in generator.tts_generator.location_accent_mapping:
            accent = generator.tts_generator.location_accent_mapping[location]['accent']
        print(f"   {location}: {count} stories → {accent} accent")
    
    print(f"\n🎭 Emotion Distribution:")
    emotion_counts = {}
    for story in results['stories']:
        emotion = story.get('emotion', 'unknown')
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    for emotion, count in emotion_counts.items():
        print(f"   {emotion}: {count} stories")
    
    if results['errors']:
        print(f"\n⚠️ Errors:")
        for error in results['errors']:
            print(f"   • {error}")
    
    print(f"\n📝 Story Details:")
    for story in results['stories']:
        if not story.get('error'):
            print(f"   {story['number']}. {story['title'][:60]}...")
            print(f"      📺 {story['source']} | 🌍 {story['geographic_location']} | 🎭 {story['emotion']} | 🗣️ {story['detected_accent']}")

if __name__ == "__main__":
    main()
