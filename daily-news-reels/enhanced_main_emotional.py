#!/usr/bin/env python3
"""
Enhanced Main Script with Emotional Voices
Now with human-like voices, emotions, humor, and personality!
"""

import os
import sys
import argparse
import time
from datetime import datetime

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Import services
from src.services.news_service import NewsService
from src.services.enhanced_funny_content_processor import EnhancedFunnyContentProcessor
from enhanced_emotional_audio import EnhancedEmotionalAudioService

def print_banner():
    """Print enhanced banner"""
    print("    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print("    ║                                                                              ║")
    print("    ║                🎭 EMOTIONAL AI NEWS-TO-REELS GENERATOR 🎬                   ║")
    print("    ║                                                                              ║")
    print("    ║              High-Quality Video Reels with HUMAN-LIKE VOICES                ║")
    print("    ║                  ✨ NOW WITH EMOTIONS & PERSONALITY! ✨                      ║")
    print("    ║                                                                              ║")
    print("    ║              🎤 Exciting! 😄 Funny! 🎭 Dramatic! 💫 Engaging!               ║")
    print("    ║                                                                              ║")
    print("    ╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

def run_emotional_pipeline(args):
    """Run the enhanced pipeline with emotional voices"""
    
    print_banner()
    
    print("🚀 Initializing Enhanced Emotional Pipeline...")
    print("✨ Features: Human-like voices, emotions, humor, personality!")
    print()
    
    # Initialize services
    news_service = NewsService()
    content_processor = EnhancedFunnyContentProcessor()
    audio_service = EnhancedEmotionalAudioService()
    
    start_time = time.time()
    
    try:
        # Step 1: Fetch News
        print("📰 STEP 1: Fetching Latest News Articles")
        print("-" * 50)
        
        countries = args.countries.split(',') if args.countries else ['us', 'in', 'gb']
        categories = args.categories.split(',') if args.categories else ['technology', 'business', 'sports', 'entertainment']
        
        print(f"🌍 Countries: {', '.join(countries)}")
        print(f"📂 Categories: {', '.join(categories)}")
        print(f"📊 Max articles per category: {args.max_articles}")
        print()
        
        articles = []
        for country in countries:
            for category in categories:
                country_articles = news_service.get_articles(country, category, args.max_articles)
                articles.extend(country_articles)
        
        print(f"✅ Fetched {len(articles)} articles")
        print()
        
        # Step 2: Process Content with Humor and Emotions
        print("🎭 STEP 2: Processing Content with AI + Humor + Emotions")
        print("-" * 50)
        print(f"🚀 Processing {len(articles)} articles with enhanced humor and emotions...")
        
        processed_articles = content_processor.process_batch(articles, args.max_workers)
        
        print(f"✅ Successfully processed {len(processed_articles)} articles")
        print()
        
        # Show processing results
        if processed_articles:
            print("📊 PROCESSING RESULTS:")
            emotions = {}
            humor_levels = {}
            personalities = {}
            
            for article in processed_articles:
                emotion = article.emotion
                humor = article.humor_level
                personality = article.personality_traits[0] if article.personality_traits else 'unknown'
                
                emotions[emotion] = emotions.get(emotion, 0) + 1
                humor_levels[humor] = humor_levels.get(humor, 0) + 1
                personalities[personality] = personalities.get(personality, 0) + 1
            
            print(f"🎭 Emotions: {dict(emotions)}")
            print(f"😄 Humor Styles: {dict(humor_levels)}")
            print(f"🎪 Personalities: {dict(personalities)}")
            print(f"📈 Average Quality: {sum(a.quality_score for a in processed_articles) / len(processed_articles):.1f}%")
            print(f"💫 Average Engagement: {sum(a.engagement_score for a in processed_articles) / len(processed_articles):.1f}%")
            print()
        
        # Step 3: Generate Emotional Audio
        print("🎤 STEP 3: Generating Emotional Human-Like Audio")
        print("-" * 50)
        print(f"🎭 Generating emotional voiceovers with {args.audio_workers} parallel workers...")
        
        # Convert to format expected by audio service
        audio_articles = [
            {
                'title': article.original_title,
                'script': article.script,
                'category': 'general'  # You might want to preserve category from original
            }
            for article in processed_articles
        ]
        
        audio_results = audio_service.generate_batch_emotional_voiceovers(audio_articles, args.audio_workers)
        
        print(f"✅ Generated {len(audio_results)} emotional audio files")
        print()
        
        # Show audio results
        if audio_results:
            print("🎤 AUDIO RESULTS:")
            emotions_used = {}
            personalities_used = {}
            total_duration = 0
            
            for result in audio_results:
                emotion = result['emotion']
                personalities = result.get('personality', [])
                duration = result['metrics']['duration']
                
                emotions_used[emotion] = emotions_used.get(emotion, 0) + 1
                total_duration += duration
                
                for personality in personalities:
                    personalities_used[personality] = personalities_used.get(personality, 0) + 1
            
            print(f"🎭 Voice Emotions Used: {dict(emotions_used)}")
            print(f"🎪 Voice Personalities: {dict(personalities_used)}")
            print(f"⏱️ Total Audio Duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
            print(f"🎯 Average Audio Quality: {sum(r['metrics']['quality_score'] for r in audio_results) / len(audio_results):.1f}%")
            print()
        
        # Summary
        total_time = time.time() - start_time
        
        print("🎉 EMOTIONAL PIPELINE COMPLETE!")
        print("="*80)
        print(f"⏱️ Total Processing Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"📰 Articles Processed: {len(processed_articles)}")
        print(f"🎤 Audio Files Generated: {len(audio_results)}")
        print(f"🎭 Emotional Voices: {'✅ ACTIVE' if audio_results else '❌ FAILED'}")
        print(f"😄 Humor & Personality: {'✅ ACTIVE' if processed_articles else '❌ FAILED'}")
        print()
        
        print("💡 NEW FEATURES ACTIVE:")
        print("✅ Human-like emotional voices (excited, playful, dramatic, etc.)")
        print("✅ Funny, engaging scripts with personality")
        print("✅ Speed and pitch modulation for natural sound")
        print("✅ Multiple voice personalities (influencer, narrator, reporter)")
        print("✅ Category-aware emotion and humor selection")
        print("✅ Parallel processing for maximum speed")
        print()
        
        if audio_results:
            print("🎊 SUCCESS! Your voices are now EMOTIONAL and ENGAGING!")
            print("🎤 No more boring robot voices - now with human personality!")
            print(f"📁 Audio files saved in: output/sessions/{datetime.now().strftime('%Y%m%d_%H%M%S')}/audio/")
        
    except Exception as e:
        print(f"❌ Error in pipeline: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function with enhanced argument parsing"""
    
    parser = argparse.ArgumentParser(
        description="AI News-to-Reels Generator with Emotional Human-Like Voices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_main_emotional.py                                    # Run with emotional voices
  python enhanced_main_emotional.py --countries us,gb --categories tech,sports
  python enhanced_main_emotional.py --max-articles 5 --test          # Quick emotional test
  python enhanced_main_emotional.py --max-workers 6 --audio-workers 6 # Max parallel processing
        """
    )
    
    parser.add_argument('--countries', 
                       help='Comma-separated country codes (e.g., us,in,gb,ca)')
    parser.add_argument('--categories', 
                       help='Comma-separated categories (e.g., technology,business,sports,entertainment)')
    parser.add_argument('--max-articles', type=int, default=3,
                       help='Maximum articles per category (default: 3)')
    parser.add_argument('--test', action='store_true',
                       help='Run quick test with limited articles')
    parser.add_argument('--max-workers', type=int, default=4,
                       help='Maximum parallel workers for content processing (default: 4)')
    parser.add_argument('--audio-workers', type=int, default=4,
                       help='Parallel workers for audio generation (default: 4)')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Adjust for test mode
    if args.test:
        args.max_articles = min(args.max_articles, 2)
        print("🧪 Test mode: Limited to 2 articles per category")
        print()
    
    # Run the emotional pipeline
    run_emotional_pipeline(args)

if __name__ == "__main__":
    main()
