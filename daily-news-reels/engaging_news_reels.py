"""
Complete Engaging News Reels Generator
Combines RSS feeds, engaging scripts, and dynamic TTS for captivating news reels
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Optional
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from engaging_script_generator import EngagingScriptGenerator
from engaging_gtts import EngagingGTTS
from rss_news_service import RSSNewsService

class EngagingNewsReelsGenerator:
    """Complete system for generating engaging news reels"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Initialize services
        self.news_service = RSSNewsService()
        self.script_generator = EngagingScriptGenerator()
        self.tts_service = EngagingGTTS()
        
        # Output directories
        self.output_dir = "output"
        self.audio_dir = f"{self.output_dir}/audio"
        self.reports_dir = f"{self.output_dir}/reports"
        self.reels_dir = "reels"
        
        # Create directories
        for directory in [self.output_dir, self.audio_dir, self.reports_dir, self.reels_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def _setup_logger(self):
        logger = logging.getLogger('EngagingNewsReels')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def generate_engaging_reels(self, 
                              max_articles: int = 5,
                              categories: List[str] = None,
                              target_audience: str = 'general') -> Dict:
        """Generate multiple engaging news reels"""
        
        print("""
        ╔══════════════════════════════════════════════════════════════════════════════╗
        ║                                                                              ║
        ║                    🔥 ENGAGING NEWS REELS GENERATOR 🎬                       ║
        ║                                                                              ║
        ║                   Creating Catchy, Attention-Grabbing Reels                 ║
        ║                                                                              ║
        ╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'generated_reels': [],
            'success_count': 0,
            'total_articles': 0,
            'errors': []
        }
        
        try:
            # Step 1: Fetch engaging news from multiple sources
            self.logger.info("🔍 Fetching latest engaging news...")
            
            if not categories:
                categories = ['technology', 'business', 'entertainment', 'sports', 'general']
            
            articles = self.news_service.fetch_engaging_news(
                categories=categories,
                max_articles_per_source=max_articles,
                prefer_trending=True
            )
            
            results['total_articles'] = len(articles)
            self.logger.info(f"📰 Found {len(articles)} articles")
            
            if not articles:
                self.logger.warning("No articles found!")
                return results
            
            # Step 2: Process each article into an engaging reel
            for i, article in enumerate(articles[:max_articles]):
                try:
                    self.logger.info(f"\n🎬 Creating reel {i+1}/{min(len(articles), max_articles)}")
                    self.logger.info(f"📰 Title: {article['title'][:60]}...")
                    
                    reel_result = self._create_engaging_reel(article, i+1, target_audience)
                    
                    if reel_result['success']:
                        results['generated_reels'].append(reel_result)
                        results['success_count'] += 1
                        self.logger.info(f"✅ Successfully created reel {i+1}")
                    else:
                        results['errors'].append(f"Reel {i+1}: {reel_result.get('error', 'Unknown error')}")
                        self.logger.error(f"❌ Failed to create reel {i+1}")
                        
                except Exception as e:
                    error_msg = f"Error processing article {i+1}: {str(e)}"
                    results['errors'].append(error_msg)
                    self.logger.error(error_msg)
            
            # Step 3: Generate summary report
            self._generate_summary_report(results)
            
            self.logger.info(f"\n🎉 Generation complete!")
            self.logger.info(f"✅ Successfully created {results['success_count']}/{results['total_articles']} reels")
            
            return results
            
        except Exception as e:
            error_msg = f"Fatal error in reel generation: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
            return results
    
    def _create_engaging_reel(self, article: Dict, reel_number: int, target_audience: str) -> Dict:
        """Create a single engaging news reel"""
        
        result = {
            'reel_number': reel_number,
            'title': article['title'],
            'category': article.get('category', 'general'),
            'success': False,
            'files': {},
            'metrics': {}
        }
        
        try:
            # Step 1: Create engaging script
            self.logger.info("✍️ Generating engaging script...")
            
            # Create base script from article
            base_script = self._create_base_script(article)
            
            # Enhance with engaging elements
            engaging_script = self.script_generator.enhance_script(base_script, article)
            
            result['script'] = engaging_script
            result['metrics']['script_length'] = len(engaging_script)
            
            # Step 2: Determine voice style and emotion
            emotion, voice_style = self._determine_voice_characteristics(article, target_audience)
            
            result['voice_style'] = voice_style
            result['emotion'] = emotion
            
            # Step 3: Generate engaging audio
            self.logger.info(f"🎤 Generating engaging audio with {voice_style} voice...")
            
            audio_filename = f"engaging_reel_{reel_number:03d}_{article['category']}.wav"
            audio_path = os.path.join(self.audio_dir, audio_filename)
            
            audio_success = self.tts_service.generate_engaging_audio(
                text=engaging_script,
                output_path=audio_path,
                category=article.get('category', 'general'),
                emotion=emotion
            )
            
            if audio_success:
                result['files']['audio'] = audio_path
                result['metrics']['audio_generated'] = True
                
                # Get audio duration
                try:
                    import wave
                    with wave.open(audio_path, 'r') as wav_file:
                        duration = wav_file.getnframes() / wav_file.getframerate()
                        result['metrics']['audio_duration'] = duration
                except:
                    result['metrics']['audio_duration'] = 0
                
                self.logger.info(f"🔊 Audio generated: {audio_filename}")
            else:
                result['error'] = "Failed to generate audio"
                return result
            
            # Step 4: Save script and metadata
            script_filename = f"engaging_script_{reel_number:03d}_{article['category']}.txt"
            script_path = os.path.join(self.reports_dir, script_filename)
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {article['title']}\\n")
                f.write(f"Category: {article.get('category', 'general')}\\n")
                f.write(f"Voice Style: {voice_style}\\n")
                f.write(f"Emotion: {emotion}\\n")
                f.write(f"Generated: {datetime.now().isoformat()}\\n")
                f.write(f"\\n--- ENGAGING SCRIPT ---\\n")
                f.write(engaging_script)
                
                # Also include original content for reference
                f.write(f"\\n\\n--- ORIGINAL CONTENT ---\\n")
                f.write(f"Description: {article.get('description', 'N/A')}\\n")
                f.write(f"URL: {article.get('url', 'N/A')}\\n")
            
            result['files']['script'] = script_path
            result['success'] = True
            
            return result
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error creating engaging reel: {e}")
            return result
    
    def _create_base_script(self, article: Dict) -> str:
        """Create a base script from article content"""
        
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Create a concise, informative base script
        if description and len(description) > 20:
            # Use description as main content
            script = f"{title}. {description}"
        else:
            # Fallback to title expansion
            script = f"Breaking news: {title}. This developing story is capturing attention worldwide."
        
        # Keep it concise for better TTS quality
        if len(script) > 500:
            script = script[:497] + "..."
        
        return script
    
    def _determine_voice_characteristics(self, article: Dict, target_audience: str) -> tuple:
        """Determine appropriate emotion and voice style for the content"""
        
        title = article.get('title', '').lower()
        category = article.get('category', 'general').lower()
        
        # Determine emotion based on content
        urgent_keywords = ['breaking', 'urgent', 'crisis', 'attack', 'emergency', 'scandal']
        exciting_keywords = ['amazing', 'incredible', 'revolutionary', 'breakthrough', 'huge']
        shocking_keywords = ['shocking', 'unexpected', 'surprising', 'dramatic', 'explosive']
        
        if any(word in title for word in urgent_keywords):
            emotion = 'urgent'
        elif any(word in title for word in exciting_keywords):
            emotion = 'exciting'
        elif any(word in title for word in shocking_keywords):
            emotion = 'surprising'
        else:
            emotion = 'engaging'
        
        # Determine voice style based on category and audience
        if category in ['technology', 'tech']:
            voice_style = 'tech_news'
        elif category in ['business', 'finance']:
            voice_style = 'business_news'
        elif category in ['entertainment', 'celebrity']:
            voice_style = 'entertainment'
        elif category in ['sports']:
            voice_style = 'sports'
        elif emotion == 'urgent' or 'breaking' in title:
            voice_style = 'breaking_news'
        else:
            voice_style = 'default'
        
        return emotion, voice_style
    
    def _generate_summary_report(self, results: Dict):
        """Generate a comprehensive summary report"""
        
        report_path = os.path.join(self.reports_dir, f"engaging_reels_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Add additional statistics
        if results['generated_reels']:
            total_duration = sum(reel.get('metrics', {}).get('audio_duration', 0) for reel in results['generated_reels'])
            avg_script_length = sum(reel.get('metrics', {}).get('script_length', 0) for reel in results['generated_reels']) / len(results['generated_reels'])
            
            results['summary'] = {
                'total_audio_duration': total_duration,
                'average_script_length': avg_script_length,
                'success_rate': (results['success_count'] / results['total_articles']) * 100 if results['total_articles'] > 0 else 0,
                'categories_processed': list(set(reel.get('category', 'unknown') for reel in results['generated_reels'])),
                'voice_styles_used': list(set(reel.get('voice_style', 'unknown') for reel in results['generated_reels'])),
                'emotions_used': list(set(reel.get('emotion', 'unknown') for reel in results['generated_reels']))
            }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📊 Report saved: {report_path}")

def main():
    """Main function with command line interface"""
    
    parser = argparse.ArgumentParser(description="Generate Engaging News Reels")
    parser.add_argument('--max-articles', type=int, default=5, help='Maximum number of reels to generate')
    parser.add_argument('--categories', nargs='+', help='News categories to focus on')
    parser.add_argument('--audience', choices=['general', 'tech', 'business', 'entertainment'], default='general', help='Target audience')
    parser.add_argument('--test', action='store_true', help='Run quick test with 2 articles')
    
    args = parser.parse_args()
    
    if args.test:
        args.max_articles = 2
        print("🧪 Running in test mode...")
    
    generator = EngagingNewsReelsGenerator()
    
    results = generator.generate_engaging_reels(
        max_articles=args.max_articles,
        categories=args.categories,
        target_audience=args.audience
    )
    
    # Print summary
    print(f"\\n🎯 FINAL RESULTS:")
    print(f"✅ Successfully generated: {results['success_count']} reels")
    print(f"📰 Total articles processed: {results['total_articles']}")
    
    if results['success_count'] > 0:
        print(f"\\n🎵 Generated audio files:")
        for reel in results['generated_reels']:
            if 'audio' in reel.get('files', {}):
                print(f"  🔊 {os.path.basename(reel['files']['audio'])}")
    
    if results['errors']:
        print(f"\\n⚠️ Errors encountered: {len(results['errors'])}")
        for error in results['errors'][:3]:  # Show first 3 errors
            print(f"  ❌ {error}")

if __name__ == "__main__":
    main()
