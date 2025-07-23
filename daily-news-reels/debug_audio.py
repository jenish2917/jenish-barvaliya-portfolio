#!/usr/bin/env python3
"""
Quick Single Test for Audio Error Debugging
"""

import os
import sys

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from services.enhanced_emotional_audio_service_fixed import EnhancedEmotionalAudioService
from services.emotional_voice_system import VoiceEmotion

def test_single_audio():
    print("🎵 Testing single audio generation...")
    
    audio_service = EnhancedEmotionalAudioService()
    
    script = "OMG guys! AI robot makes perfect coffee in seconds!"
    title = "AI Coffee Robot"
    category = "technology"
    emotion = VoiceEmotion.EXCITED
    
    print(f"Script: {script}")
    print(f"Emotion: {emotion}")
    print(f"Emotion type: {type(emotion)}")
    print(f"Emotion value: {emotion.value}")
    
    result = audio_service.generate_emotional_voiceover(script, title, category, emotion)
    
    if result[0]:
        print("✅ Success!")
    else:
        print("❌ Failed")

if __name__ == "__main__":
    test_single_audio()
