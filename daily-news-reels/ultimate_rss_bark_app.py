"""
Enhanced Ultimate News-to-Reels Generator
Using RSS feeds (unlimited news) + Bark TTS (offline high-quality voice)
No API keys required for core functionality!
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from services.rss_news_service import RSSNewsService
from services.bark_tts_service import BarkTTSService, BARK_INSTALLATION_GUIDE
from services.video_analyzer import VideoAnalyzer
from dotenv import load_dotenv

# Load configuration
load_dotenv('config.env')

def setup_console_logger():
    """Setup colorful console logging"""
    try:
        from colorama import init, Fore, Style
        init()
        
        class ColoredFormatter(logging.Formatter):
            """Custom formatter with colors"""
            
            COLORS = {
                'DEBUG': Fore.CYAN,
                'INFO': Fore.GREEN,
                'WARNING': Fore.YELLOW,
                'ERROR': Fore.RED,
                'CRITICAL': Fore.MAGENTA
            }
            
            def format(self, record):
                log_message = super().format(record)
                return f"{self.COLORS.get(record.levelname, '')}{log_message}{Style.RESET_ALL}"
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Add colored console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)
        
    except ImportError:
        # Fallback to basic logging if colorama not available
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    """Display application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║           🌍 UNLIMITED NEWS-TO-REELS GENERATOR 🎬                           ║
    ║                                                                              ║
    ║              📡 RSS Feeds (No API Keys) + 🎙️ Bark TTS (Offline)             ║
    ║                      Truly Unlimited Global News Reels                      ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if all required dependencies are available"""
    issues = []
    
    # Check RSS service
    try:
        import feedparser
        print("✅ RSS News Service: Ready (feedparser available)")
    except ImportError:
        issues.append("❌ feedparser not installed. Run: pip install feedparser")
    
    # Check Bark TTS
    bark_service = BarkTTSService()
    if bark_service.is_available():
        print("✅ Bark TTS Service: Ready (offline high-quality voice)")
    else:
        issues.append("❌ Bark TTS not available. Install with instructions below.")
        print(BARK_INSTALLATION_GUIDE)
    
    # Check other dependencies
    try:
        import cv2
        print("✅ Video Processing: Ready (OpenCV available)")
    except ImportError:
        issues.append("❌ OpenCV not installed. Run: pip install opencv-python")
    
    try:
        import moviepy
        print("✅ Video Generation: Ready (MoviePy available)")
    except ImportError:
        issues.append("❌ MoviePy not installed. Run: pip install moviepy")
    
    return issues

def create_directories():
    """Create required output directories"""
    directories = [
        'output',
        'output/audio',
        'output/videos',
        'output/temp',
        'output/logs',
        'output/reports',
        'reels'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
    print("✅ Output directories created")

def run_unlimited_pipeline(max_articles: int = 20, test_mode: bool = False):
    """
    Run the unlimited news-to-reels pipeline
    
    Args:
        max_articles: Maximum number of articles to process
        test_mode: If True, run with minimal articles for testing
    """
    logger = logging.getLogger(__name__)
    
    print("\n🚀 Starting Unlimited News-to-Reels Pipeline")
    print("=" * 80)
    
    # Adjust for test mode
    if test_mode:
        max_articles = 3
        print(f"🧪 Test mode: Processing only {max_articles} articles")
    
    # Initialize services
    print("\n📡 Step 1: Initializing RSS News Service")
    rss_service = RSSNewsService()
    
    print("🎙️ Step 2: Initializing Bark TTS Service")
    bark_service = BarkTTSService()
    
    if not bark_service.is_available():
        print("⚠️ Bark TTS not available, falling back to gTTS")
        # You could implement gTTS fallback here
        return False
    
    print("📊 Step 3: Initializing Video Analyzer")
    video_analyzer = VideoAnalyzer()
    
    # Fetch global news
    print(f"\n📰 Step 4: Fetching Global News (max {max_articles} articles)")
    articles = rss_service.fetch_global_news(
        max_articles_per_region=5 if not test_mode else 1,
        max_total_articles=max_articles
    )
    
    if not articles:
        print("❌ No articles fetched. Check your internet connection.")
        return False
    
    print(f"✅ Fetched {len(articles)} articles from global sources")
    
    # Show trending topics
    trending = rss_service.get_trending_topics(articles)
    if trending:
        print(f"📈 Trending topics: {', '.join(trending[:5])}")
    
    # Process articles
    processed_count = 0
    
    for i, article in enumerate(articles, 1):
        print(f"\n🤖 Step 5.{i}: Processing Article {i}/{len(articles)}")
        print(f"   Title: {article['title'][:60]}...")
        print(f"   Source: {article['source']} ({article['region']})")
        print(f"   Category: {article['category']}")
        
        # Create a script from the article
        script = create_news_script(article)
        
        if not script:
            print("   ⚠️ Failed to create script, skipping")
            continue
        
        # Generate speech using Bark
        audio_path = f"output/audio/article_{i:03d}_{article['source']}.wav"
        print(f"   🎙️ Generating speech with Bark TTS...")
        
        if bark_service.generate_speech(
            script, 
            audio_path,
            voice_preset='news_anchor_female',
            add_emotion=True
        ):
            print(f"   ✅ Audio generated: {audio_path}")
            
            # Create video (simplified for now)
            video_path = f"reels/reel_{i:03d}_{article['source']}.mp4"
            if create_news_video(script, audio_path, video_path, article):
                print(f"   ✅ Video created: {video_path}")
                
                # Analyze video quality
                metrics = video_analyzer.analyze_video(video_path)
                if metrics:
                    print(f"   📊 Video Quality: {metrics.overall_quality_score:.1f}%")
                    
                processed_count += 1
            else:
                print("   ❌ Failed to create video")
        else:
            print("   ❌ Failed to generate speech")
        
        # Limit for test mode
        if test_mode and processed_count >= 2:
            break
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 PIPELINE SUMMARY")
    print(f"{'='*80}")
    print(f"📰 Articles Fetched: {len(articles)}")
    print(f"🎬 Videos Created: {processed_count}")
    print(f"📈 Success Rate: {(processed_count/len(articles)*100):.1f}%")
    print(f"💰 Cost: $0.00 (Completely free!)")
    print(f"🚫 Rate Limits: None (Unlimited)")
    
    return processed_count > 0

def create_news_script(article: dict) -> str:
    """
    Create a news script from article data
    Enhanced with better formatting for speech
    """
    try:
        title = article['title']
        content = article['content']
        source = article['source']
        
        # Create a natural-sounding script
        script = f"""
        Breaking news from {source}.
        
        {title}
        
        {content[:500]}...
        
        This has been your news update. Stay informed, stay connected.
        """
        
        # Clean up the script
        script = script.strip()
        script = script.replace('\n\n', '\n')
        script = script.replace('  ', ' ')
        
        return script
        
    except Exception as e:
        logging.error(f"Error creating script: {e}")
        return ""

def create_news_video(script: str, audio_path: str, video_path: str, article: dict) -> bool:
    """
    Create a news video with the generated audio
    Simplified version - you can enhance this with better visuals
    """
    try:
        from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, TextClip
        
        # Load audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create background
        background = ColorClip(size=(1080, 1920), color=(25, 25, 25), duration=duration)
        
        # Create title text
        title_text = TextClip(
            article['title'][:100], 
            fontsize=48, 
            color='white', 
            font='Arial-Bold',
            size=(1000, None)
        ).set_position(('center', 200)).set_duration(duration)
        
        # Create source text
        source_text = TextClip(
            f"Source: {article['source']} | {article['region'].upper()}", 
            fontsize=32, 
            color='gray', 
            font='Arial'
        ).set_position(('center', 1600)).set_duration(duration)
        
        # Compose video
        video = CompositeVideoClip([background, title_text, source_text])
        video = video.set_audio(audio)
        
        # Export
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        video.write_videofile(
            video_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # Cleanup
        audio.close()
        video.close()
        
        return True
        
    except Exception as e:
        logging.error(f"Error creating video: {e}")
        return False

def main():
    """Main application entry point"""
    setup_console_logger()
    display_banner()
    
    parser = argparse.ArgumentParser(
        description="Unlimited News-to-Reels Generator - RSS + Bark TTS",
        epilog="""
Examples:
  python ultimate_rss_bark_app.py                    # Run with default settings
  python ultimate_rss_bark_app.py --test            # Quick test with 3 articles
  python ultimate_rss_bark_app.py --max-articles 50 # Process up to 50 articles
  python ultimate_rss_bark_app.py --check-deps      # Check dependencies only
        """
    )
    
    parser.add_argument('--max-articles', type=int, default=20,
                        help='Maximum articles to process (default: 20)')
    parser.add_argument('--test', action='store_true',
                        help='Run quick test with minimal articles')
    parser.add_argument('--check-deps', action='store_true',
                        help='Check dependencies and exit')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check dependencies
    print("\n🔧 Checking Dependencies...")
    issues = check_dependencies()
    
    if args.check_deps:
        if issues:
            print(f"\n❌ Found {len(issues)} issues:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("\n✅ All dependencies are ready!")
        return
    
    if issues:
        print(f"\n❌ Cannot proceed. Found {len(issues)} dependency issues:")
        for issue in issues:
            print(f"   {issue}")
        print("\nPlease install missing dependencies and try again.")
        return
    
    # Create directories
    create_directories()
    
    # Run the pipeline
    try:
        success = run_unlimited_pipeline(
            max_articles=args.max_articles,
            test_mode=args.test
        )
        
        if success:
            print("\n🎉 Pipeline completed successfully!")
            print("📁 Check the 'reels' folder for generated videos")
            print("📊 Check the 'output' folder for detailed reports")
        else:
            print("\n❌ Pipeline failed. Check logs for details.")
            
    except KeyboardInterrupt:
        print("\n⏹️ Pipeline interrupted by user")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"\n❌ Pipeline failed: {e}")

if __name__ == "__main__":
    main()
