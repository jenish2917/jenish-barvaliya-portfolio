"""
Create Complete Emotional News Reel
Uses the fixed emotional audio system to generate exciting reels
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.enhanced_funny_content_processor import EnhancedFunnyContentProcessor
from src.services.enhanced_emotional_audio_service_fixed import EnhancedEmotionalAudioService
from src.services.emotional_voice_system import VoiceEmotion
import random
from datetime import datetime

def create_emotional_reel():
    print("🎬 CREATING EMOTIONAL NEWS REEL")
    print("=" * 50)
    
    # Initialize services
    content_processor = EnhancedFunnyContentProcessor()
    audio_service = EnhancedEmotionalAudioService()
    
    # Sample breaking news articles
    breaking_news = [
        {
            'title': 'AI Robot Becomes World Champion Chess Player in 30 Seconds',
            'content': 'Revolutionary AI system defeats grandmaster Magnus Carlsen in record-breaking 30-second match, sparking debate about artificial intelligence in competitive gaming.',
            'category': 'technology'
        },
        {
            'title': 'Scientists Discover Coffee Bean That Makes Perfect Espresso Every Time',
            'content': 'New genetically modified coffee bean promises to deliver barista-quality espresso with zero skill required, revolutionizing home brewing.',
            'category': 'science'
        },
        {
            'title': 'Local Dog Elected as Town Mayor After Promising More Parks',
            'content': 'Golden Retriever named Buddy wins mayoral election with overwhelming 85% vote share after campaign focused on more dog parks and longer walk times.',
            'category': 'general'
        },
        {
            'title': 'Cryptocurrency Created by Teenagers Reaches $1 Billion Value',
            'content': 'High school students launch DogeCoin competitor called "StudyCoin" that rewards students for homework completion, reaches massive valuation.',
            'category': 'business'
        }
    ]
    
    # Select random article
    article = random.choice(breaking_news)
    
    print(f"📰 Selected Breaking News: {article['title']}")
    print(f"🏷️  Category: {article['category']}")
    print()
    
    # Step 1: Process content emotionally
    print("🔄 Step 1: Processing content with emotional AI...")
    processed = content_processor.process_article(
        article['title'],
        article['content'],
        'US',
        article['category']
    )
    
    if not processed:
        print("❌ Failed to process content")
        return
    
    print(f"✅ Content Generated:")
    print(f"   📝 Summary: {processed.summary}")
    print(f"   🎭 Emotional Script: {processed.script}")
    print(f"   😊 Emotion: {processed.emotion}")
    print(f"   📊 Quality: {processed.quality_score:.1f}%")
    print(f"   🔥 Engagement: {processed.engagement_score:.1f}%")
    print()
    
    # Step 2: Generate emotional voiceover
    print("🔄 Step 2: Generating emotional voiceover...")
    
    # Map emotion string to enum
    emotion_map = {
        'excited': VoiceEmotion.EXCITED,
        'surprised': VoiceEmotion.SURPRISED,
        'playful': VoiceEmotion.PLAYFUL,
        'dramatic': VoiceEmotion.DRAMATIC,
        'confident': VoiceEmotion.CONFIDENT,
        'concerned': VoiceEmotion.CONCERNED,
        'sarcastic': VoiceEmotion.SARCASTIC,
        'warm': VoiceEmotion.WARM
    }
    
    emotion_enum = emotion_map.get(processed.emotion, VoiceEmotion.EXCITED)
    
    try:
        audio_path, metrics = audio_service.generate_emotional_voiceover(
            processed.script,
            article['title'],
            article['category'],
            emotion_enum
        )
        
        if audio_path and metrics:
            print(f"✅ Audio Generated Successfully!")
            print(f"   🎤 Audio File: {audio_path}")
            print(f"   ⏱️  Duration: {metrics.duration:.1f} seconds")
            print(f"   🎭 Emotion: {metrics.emotion}")
            print(f"   🎪 Personality: {metrics.personality_traits}")
            print(f"   📊 Audio Quality: {metrics.quality_score:.1f}%")
            print(f"   🔊 Sample Rate: {metrics.sample_rate} Hz")
            print(f"   📁 File Size: {metrics.file_size} bytes")
        else:
            print("❌ Audio generation failed")
            return
            
    except Exception as e:
        print(f"❌ Audio generation error: {e}")
        return
    
    # Step 3: Reel summary
    print()
    print("🎯 REEL CREATION COMPLETE!")
    print("=" * 40)
    print(f"🎬 Title: {article['title']}")
    print(f"📱 Script: {processed.script}")
    print(f"🎵 Audio: {os.path.basename(audio_path)}")
    print(f"⏱️  Duration: {metrics.duration:.1f}s")
    print(f"😊 Emotion: {metrics.emotion}")
    print(f"🔥 Engagement: {processed.engagement_score:.1f}%")
    print()
    print("🎉 Your exciting emotional news reel is ready!")
    print("✅ No more boring voice - now it's human-like and engaging!")
    print("✅ No more boring scripts - now it's funny with OMG and emojis!")
    print("✅ Voice modulation working with speed/pitch/volume effects!")
    
    return {
        'title': article['title'],
        'script': processed.script,
        'audio_path': audio_path,
        'metrics': metrics.to_dict(),
        'emotion': metrics.emotion,
        'engagement': processed.engagement_score,
        'quality': processed.quality_score
    }

if __name__ == "__main__":
    reel = create_emotional_reel()
    if reel:
        print(f"\n🎬 Reel saved with {reel['emotion']} emotion and {reel['engagement']:.1f}% engagement!")
