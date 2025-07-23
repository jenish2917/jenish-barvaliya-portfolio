#!/usr/bin/env python3
"""
Debug Emotional Voice System
"""

import os
import sys

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from services.emotional_voice_system import EmotionalVoiceSystem, VoiceEmotion

def debug_emotional_system():
    print("🔍 Debugging Emotional Voice System...")
    
    voice_system = EmotionalVoiceSystem()
    
    print(f"Available emotions: {list(VoiceEmotion)}")
    print(f"Emotional emphasis keys: {list(voice_system.emotional_emphasis.keys())}")
    
    # Test each emotion
    test_emotion = VoiceEmotion.EXCITED
    print(f"Testing emotion: {test_emotion}")
    print(f"Type: {type(test_emotion)}")
    
    if test_emotion in voice_system.emotional_emphasis:
        print("✅ Emotion found in dictionary")
        config = voice_system.emotional_emphasis[test_emotion]
        print(f"Config: {config}")
    else:
        print("❌ Emotion NOT found in dictionary")
        print("Available keys:")
        for key in voice_system.emotional_emphasis.keys():
            print(f"  {key} (type: {type(key)})")
    
    # Test the method that's failing
    print("\n🎵 Testing add_emotional_markers...")
    try:
        result = voice_system.add_emotional_markers("Test script", test_emotion)
        print(f"✅ Success: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_emotional_system()
