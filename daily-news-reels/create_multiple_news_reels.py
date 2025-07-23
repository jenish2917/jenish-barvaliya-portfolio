"""
Multiple Today's News Reels with Emotion Matching
Creates several reels from different news types to show emotion variety
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from todays_news_reel_generator import TodaysNewsReelGenerator
import random

def create_multiple_news_reels():
    print("🎬 CREATING MULTIPLE TODAY'S NEWS REELS")
    print("=" * 60)
    print("🎯 Demonstrating emotion-based voice selection for different news types")
    print()
    
    generator = TodaysNewsReelGenerator()
    
    # Get all today's news
    news_articles = generator.get_todays_news()
    
    # Create reels for different news types
    created_reels = []
    
    for i, article in enumerate(news_articles[:3], 1):  # Create 3 reels
        print(f"🎬 REEL #{i}")
        print("-" * 30)
        
        print(f"📰 News: {article['title']}")
        print(f"📅 Source: {article['source']} ({article['time']})")
        
        # Analyze emotion
        detected_emotion = generator.analyze_news_emotion(article['title'], article['content'])
        print(f"🧠 AI-detected emotion: {detected_emotion.value}")
        
        # Process content
        processed = generator.content_processor.process_article(
            article['title'],
            article['content'],
            'US',
            article['category']
        )
        
        if processed:
            # Generate audio
            try:
                audio_path, metrics = generator.audio_service.generate_emotional_voiceover(
                    processed.script,
                    article['title'],
                    article['category'],
                    detected_emotion
                )
                
                if audio_path and metrics:
                    reel_info = {
                        'number': i,
                        'title': article['title'],
                        'category': article['category'],
                        'emotion': detected_emotion.value,
                        'personality': metrics.personality_traits[0] if metrics.personality_traits else 'unknown',
                        'script': processed.script,
                        'duration': metrics.duration,
                        'engagement': processed.engagement_score,
                        'audio_file': os.path.basename(audio_path)
                    }
                    created_reels.append(reel_info)
                    
                    print(f"✅ Success!")
                    print(f"   🎭 Emotion: {reel_info['emotion']}")
                    print(f"   🎪 Voice: {reel_info['personality']}")
                    print(f"   ⏱️  Duration: {reel_info['duration']:.1f}s")
                    print(f"   🔥 Engagement: {reel_info['engagement']:.1f}%")
                    print(f"   📱 Script preview: {processed.script[:80]}...")
                else:
                    print("❌ Audio generation failed")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ Content processing failed")
        
        print()
    
    # Summary of all reels
    print("🎯 EMOTION-MATCHED REELS SUMMARY")
    print("=" * 50)
    
    for reel in created_reels:
        print(f"🎬 Reel #{reel['number']}: {reel['title'][:50]}...")
        print(f"   📂 Category: {reel['category']}")
        print(f"   😊 Emotion: {reel['emotion']} → 🎪 Voice: {reel['personality']}")
        print(f"   ⏱️  Duration: {reel['duration']:.1f}s | 🔥 Engagement: {reel['engagement']:.1f}%")
        print()
    
    print(f"🎉 Created {len(created_reels)} emotion-matched news reels!")
    print("✅ Each reel has emotion automatically selected based on news content!")
    print("✅ Voice personalities match the emotional tone of each story!")
    print("✅ Real breaking news with human-like emotional delivery!")

if __name__ == "__main__":
    create_multiple_news_reels()
