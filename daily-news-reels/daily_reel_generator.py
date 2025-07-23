#!/usr/bin/env python3
"""
Daily News Reel Generator
========================

Complete system that:
1. Fetches today's top news from RSS feeds
2. Generates engaging scripts with geographic context
3. Creates accent-aware TTS with location detection
4. Produces complete video reels with avatars and backgrounds
5. Applies emotion-based delivery and regional accents

Usage: python daily_reel_generator.py
"""

import os
import sys
import json
from datetime import datetime
import logging
from typing import List, Dict, Optional

# Import our enhanced components
from rss_news_service import RSSNewsService
from engaging_script_generator import EngagingScriptGenerator
from accent_aware_tts import AccentAwareTTS
from enhanced_avatar_system import EnhancedAvatarSystem
from video_generator import VideoGenerator

class DailyReelGenerator:
    """Complete daily news reel generation system"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger('DailyReelGenerator')
        
        # Initialize all components
        self.news_service = RSSNewsService()
        self.script_generator = EngagingScriptGenerator()
        self.tts_generator = AccentAwareTTS()
        
        # Try to initialize video components
        try:
            self.avatar_system = EnhancedAvatarSystem()
            self.video_generator = VideoGenerator()
            self.video_enabled = True
        except Exception as e:
            self.logger.warning(f"Video components not available: {e}")
            self.video_enabled = False
        
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
    
    def generate_daily_reel(self, max_stories: int = 5, include_video: bool = True) -> Dict:
        """Generate complete daily news reel with geographic accents"""
        
        self.logger.info("🌍 Starting Daily News Reel Generation with Geographic Accents")
        self.logger.info("=" * 70)
        
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            'session_id': session_id,
            'date': datetime.now().isoformat(),
            'stories': [],
            'audio_files': [],
            'video_files': [],
            'errors': []
        }
        
        try:
            # Step 1: Fetch today's top news from multiple sources
            self.logger.info("📰 Fetching today's top news from international sources...")
            articles = self.news_service.get_engaging_articles(limit=max_stories * 2)
            
            if not articles:
                raise Exception("No articles found from RSS feeds")
            
            self.logger.info(f"✅ Found {len(articles)} articles from global sources")
            
            # Step 2: Select diverse, engaging stories
            selected_stories = self._select_diverse_stories(articles, max_stories)
            self.logger.info(f"🎯 Selected {len(selected_stories)} diverse stories for the reel")
            
            # Step 3: Generate enhanced scripts with geographic context
            self.logger.info("✍️ Generating engaging scripts with geographic awareness...")
            
            for i, article in enumerate(selected_stories, 1):
                story_data = self._process_single_story(article, i, session_id, include_video)
                results['stories'].append(story_data)
                
                if story_data['audio_file']:
                    results['audio_files'].append(story_data['audio_file'])
                if story_data.get('video_file'):
                    results['video_files'].append(story_data['video_file'])
                if story_data.get('error'):
                    results['errors'].append(story_data['error'])
            
            # Step 4: Create combined reel
            if results['audio_files']:
                combined_audio = self._create_combined_audio(results['audio_files'], session_id)
                results['combined_audio'] = combined_audio
                
                if include_video and self.video_enabled and results['video_files']:
                    combined_video = self._create_combined_video(results['video_files'], session_id)
                    results['combined_video'] = combined_video
            
            # Step 5: Generate session report
            report_file = self._generate_session_report(results, session_id)
            results['report_file'] = report_file
            
            self.logger.info("🎉 Daily News Reel Generation Complete!")
            self.logger.info(f"📊 Generated {len(results['stories'])} stories with geographic accents")
            self.logger.info(f"🎵 Created {len(results['audio_files'])} accent-aware audio files")
            if include_video:
                self.logger.info(f"🎬 Created {len(results['video_files'])} video segments")
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error in daily reel generation: {e}")
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
        
        # Regional distribution tracking
        regional_sources = {
            'us': ['cnn', 'fox', 'nbc', 'usa today', 'new york times'],
            'uk': ['bbc', 'guardian', 'telegraph', 'sky news'],
            'international': ['reuters', 'bloomberg', 'ap news'],
            'tech': ['techcrunch', 'ars technica', 'the verge'],
            'other': []
        }
        
        for article in articles:
            source = article.get('source', '').lower()
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
    
    def _process_single_story(self, article: Dict, story_number: int, session_id: str, include_video: bool) -> Dict:
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
            'video_file': None,
            'error': None
        }
        
        try:
            self.logger.info(f"📰 Processing Story {story_number}: {story_data['title'][:60]}...")
            self.logger.info(f"📺 Source: {story_data['source']}")
            
            # Step 1: Generate engaging script
            script_data = self.script_generator.generate_enhanced_script(
                title=article.get('title', ''),
                content=article.get('description', ''),
                category=self._detect_category(article.get('title', '')),
                source=article.get('source', ''),
                style='engaging'
            )
            
            if not script_data or not script_data.get('enhanced_script'):
                raise Exception("Failed to generate script")
            
            story_data['script'] = script_data['enhanced_script']
            self.logger.info(f"✍️ Generated engaging script ({len(story_data['script'])} chars)")
            
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
            
            self.logger.info(f"🌍 Detected location: {location} (confidence: {confidence:.1%})")
            self.logger.info(f"🎭 Detected emotion: {emotion}")
            self.logger.info(f"🗣️ Using accent: {story_data['detected_accent']}")
            
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
                self.logger.info(f"🎵 Generated accent-aware audio: {audio_filename}")
            else:
                raise Exception("Failed to generate audio")
            
            # Step 4: Generate video (if enabled)
            if include_video and self.video_enabled:
                video_filename = f"story_{story_number:02d}_{session_id}.mp4"
                video_path = os.path.join('output/reels', video_filename)
                
                # Create video with avatar and background
                video_success = self._create_story_video(
                    audio_path=audio_path,
                    script=story_data['script'],
                    title=story_data['title'],
                    source=story_data['source'],
                    location=location,
                    emotion=emotion,
                    output_path=video_path
                )
                
                if video_success:
                    story_data['video_file'] = video_path
                    self.logger.info(f"🎬 Generated video: {video_filename}")
            
            self.logger.info(f"✅ Story {story_number} processed successfully")
            
        except Exception as e:
            error_msg = f"Story {story_number} error: {e}"
            self.logger.error(f"❌ {error_msg}")
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
    
    def _create_story_video(self, audio_path: str, script: str, title: str, source: str, 
                           location: str, emotion: str, output_path: str) -> bool:
        """Create video for a single story with appropriate visuals"""
        try:
            # Select avatar based on emotion and location
            avatar_style = self._select_avatar_style(emotion, location)
            
            # Select background based on content
            background = self._select_background(title, location)
            
            # Generate video
            return self.video_generator.create_news_video(
                audio_file=audio_path,
                script=script,
                title=title,
                output_file=output_path,
                avatar_style=avatar_style,
                background=background
            )
            
        except Exception as e:
            self.logger.error(f"Error creating video: {e}")
            return False
    
    def _select_avatar_style(self, emotion: str, location: str) -> str:
        """Select appropriate avatar style based on emotion and location"""
        
        # Map emotions to avatar styles
        emotion_avatar_map = {
            'urgent': 'serious_male',
            'exciting': 'enthusiastic_female', 
            'dramatic': 'intense_male',
            'professional': 'business_female',
            'celebratory': 'cheerful_female',
            'mysterious': 'thoughtful_male',
            'concerned': 'serious_female'
        }
        
        return emotion_avatar_map.get(emotion, 'professional_male')
    
    def _select_background(self, title: str, location: str) -> str:
        """Select appropriate background based on content and location"""
        
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['tech', 'ai', 'software']):
            return 'tech_background'
        elif any(word in title_lower for word in ['business', 'market', 'financial']):
            return 'business_background'
        elif any(word in title_lower for word in ['sports', 'game']):
            return 'sports_background'
        elif any(word in title_lower for word in ['breaking', 'urgent']):
            return 'breaking_news_background'
        else:
            return 'news_studio_background'
    
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
    
    def _create_combined_video(self, video_files: List[str], session_id: str) -> str:
        """Combine all story videos into a single reel"""
        try:
            # This would require video editing capabilities
            # For now, just return the path where it would be saved
            output_path = f"output/reels/daily_reel_{session_id}.mp4"
            self.logger.info(f"🎬 Combined video reel would be: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating combined video: {e}")
            return ""
    
    def _generate_session_report(self, results: Dict, session_id: str) -> str:
        """Generate comprehensive session report"""
        
        report = {
            'session_id': session_id,
            'generation_date': datetime.now().isoformat(),
            'summary': {
                'total_stories': len(results['stories']),
                'successful_audio': len(results['audio_files']),
                'successful_video': len(results['video_files']),
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
        
        self.logger.info(f"📊 Session report generated: {report_path}")
        return report_path

def main():
    """Main function to generate today's news reel"""
    
    print("🌍 DAILY NEWS REEL GENERATOR WITH GEOGRAPHIC ACCENTS")
    print("=" * 60)
    print("🎯 Automatically detects news location and applies appropriate accents")
    print("🗣️ Supports US, UK, Australia, India, Canada, South Africa, New Zealand, Ireland")
    print()
    
    generator = DailyReelGenerator()
    
    # Configure generation parameters
    max_stories = 5
    include_video = True  # Set to False if video components aren't available
    
    print(f"📰 Generating reel with {max_stories} stories...")
    print(f"🎬 Video generation: {'Enabled' if include_video else 'Disabled'}")
    print()
    
    # Generate the daily reel
    results = generator.generate_daily_reel(
        max_stories=max_stories,
        include_video=include_video
    )
    
    # Display results
    print("\n🎉 GENERATION COMPLETE!")
    print("=" * 40)
    print(f"✅ Stories processed: {len(results['stories'])}")
    print(f"🎵 Audio files created: {len(results['audio_files'])}")
    print(f"🎬 Video files created: {len(results['video_files'])}")
    print(f"❌ Errors encountered: {len(results['errors'])}")
    
    if results.get('combined_audio'):
        print(f"🎵 Combined audio reel: {results['combined_audio']}")
    
    if results.get('combined_video'):
        print(f"🎬 Combined video reel: {results['combined_video']}")
    
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

if __name__ == "__main__":
    main()
