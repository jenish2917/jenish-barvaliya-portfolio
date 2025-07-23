"""
Enhanced gTTS Generator with Engaging Features
Fallback TTS system with improved voice modulation and effects
"""

import os
import sys
from gtts import gTTS
import pygame
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import tempfile
import logging
from typing import Dict, List, Optional
import re
import random

class EngagingGTTS:
    """Enhanced gTTS with engaging voice features"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Voice settings for different categories
        self.voice_settings = {
            'breaking_news': {
                'lang': 'en',
                'tld': 'com',
                'speed': 1.1,
                'pitch_shift': 2,
                'emphasis_boost': 3
            },
            'tech_news': {
                'lang': 'en',
                'tld': 'com.au',
                'speed': 1.0,
                'pitch_shift': 1,
                'emphasis_boost': 2
            },
            'business_news': {
                'lang': 'en',
                'tld': 'co.uk',
                'speed': 0.95,
                'pitch_shift': 0,
                'emphasis_boost': 2
            },
            'entertainment': {
                'lang': 'en',
                'tld': 'com',
                'speed': 1.05,
                'pitch_shift': 3,
                'emphasis_boost': 4
            },
            'sports': {
                'lang': 'en',
                'tld': 'com',
                'speed': 1.15,
                'pitch_shift': 2,
                'emphasis_boost': 5
            },
            'default': {
                'lang': 'en',
                'tld': 'com',
                'speed': 1.0,
                'pitch_shift': 1,
                'emphasis_boost': 2
            }
        }
        
        # Initialize pygame for audio processing
        try:
            pygame.mixer.init()
        except:
            self.logger.warning("Could not initialize pygame mixer")
    
    def _setup_logger(self):
        logger = logging.getLogger('EngagingGTTS')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def generate_engaging_audio(self, 
                              text: str,
                              output_path: str,
                              category: str = 'default',
                              emotion: str = 'engaging') -> bool:
        """Generate engaging audio with enhanced effects"""
        
        try:
            self.logger.info(f"🎤 Generating engaging {category} audio with {emotion} emotion")
            
            # Get voice settings
            settings = self.voice_settings.get(category, self.voice_settings['default'])
            
            # Process text for better speech
            processed_text = self._process_text_for_speech(text, emotion)
            
            # Generate base audio with gTTS
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            
            try:
                # Create gTTS object with category-specific settings
                tts = gTTS(
                    text=processed_text,
                    lang=settings['lang'],
                    tld=settings['tld'],
                    slow=False
                )
                
                tts.save(temp_path)
                self.logger.info("✅ Base audio generated with gTTS")
                
                # Apply enhancements
                enhanced_audio = self._enhance_audio(
                    temp_path, 
                    settings, 
                    emotion
                )
                
                # Save final audio
                enhanced_audio.export(output_path, format="wav")
                self.logger.info(f"🎵 Enhanced audio saved: {output_path}")
                
                return True
                
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            
        except Exception as e:
            self.logger.error(f"Error generating engaging audio: {e}")
            return False
    
    def _process_text_for_speech(self, text: str, emotion: str) -> str:
        """Process text to make it more speech-friendly"""
        
        # Remove TTS markup tags that gTTS doesn't understand
        text = re.sub(r'<[^>]+>', '', text)
        
        # Add pauses with punctuation for dramatic effect
        if emotion in ['urgent', 'exciting']:
            # Add dramatic pauses
            text = text.replace('...', '... ')
            text = text.replace('!', '! ')
            text = re.sub(r'BREAKING:', 'BREAKING: ', text)
            text = re.sub(r'URGENT:', 'URGENT: ', text)
        
        # Expand abbreviations for better pronunciation
        abbreviations = {
            'AI': 'A I',
            'CEO': 'C E O',
            'FBI': 'F B I',
            'USA': 'U S A',
            'UK': 'U K',
            'NYC': 'New York City',
            'LA': 'Los Angeles'
        }
        
        for abbr, expansion in abbreviations.items():
            text = re.sub(rf'\\b{abbr}\\b', expansion, text)
        
        # Add emphasis markers that will be processed later
        text = re.sub(r'\\*\\*([^*]+)\\*\\*', r'\\1', text)  # Remove markdown bold
        text = re.sub(r'\\*([^*]+)\\*', r'\\1', text)        # Remove markdown italic
        
        return text
    
    def _enhance_audio(self, audio_path: str, settings: Dict, emotion: str) -> AudioSegment:
        """Apply audio enhancements for more engaging sound"""
        
        # Load audio
        audio = AudioSegment.from_mp3(audio_path)
        
        # Apply speed adjustment
        if settings['speed'] != 1.0:
            # Change speed without changing pitch
            audio = audio.speedup(playback_speed=settings['speed'])
        
        # Apply pitch shifting (simple version using frame rate)
        if settings['pitch_shift'] != 0:
            # Rough pitch shifting by changing frame rate
            new_sample_rate = int(audio.frame_rate * (1 + settings['pitch_shift'] * 0.05))
            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
            audio = audio.set_frame_rate(22050)  # Normalize back
        
        # Apply dynamic range compression for more consistent volume
        audio = compress_dynamic_range(audio, threshold=-20.0, ratio=4.0)
        
        # Normalize volume
        audio = normalize(audio)
        
        # Apply emotion-specific effects
        if emotion == 'urgent':
            # Increase volume and add slight distortion
            audio = audio + 3  # Increase volume by 3dB
            
        elif emotion == 'exciting':
            # Add slight volume boost and compression
            audio = audio + 2
            audio = compress_dynamic_range(audio, threshold=-15.0, ratio=3.0)
            
        elif emotion == 'surprising':
            # Add dynamic range for dramatic effect
            audio = audio + 1
        
        # Ensure good quality
        audio = normalize(audio)
        
        # Add subtle fade in/out for professional sound
        fade_duration = min(200, len(audio) // 10)  # 200ms or 10% of audio
        audio = audio.fade_in(fade_duration).fade_out(fade_duration)
        
        return audio
    
    def test_voice_styles(self):
        """Test different voice styles and emotions"""
        
        test_cases = [
            {
                'text': "🚨 BREAKING: Apple just announced revolutionary AI breakthrough that changes everything!",
                'category': 'tech_news',
                'emotion': 'exciting',
                'filename': 'test_tech_exciting.wav'
            },
            {
                'text': "URGENT UPDATE: Stock markets surge as major tech companies report record profits!",
                'category': 'business_news',
                'emotion': 'urgent',
                'filename': 'test_business_urgent.wav'
            },
            {
                'text': "You won't believe what just happened in sports today! This incredible comeback story will blow your mind!",
                'category': 'sports',
                'emotion': 'exciting',
                'filename': 'test_sports_exciting.wav'
            }
        ]
        
        print("🎤 Testing Enhanced gTTS Voice Styles...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\\n📝 Test {i}: {test_case['category']} - {test_case['emotion']}")
            print(f"Text: {test_case['text'][:50]}...")
            
            success = self.generate_engaging_audio(
                text=test_case['text'],
                output_path=test_case['filename'],
                category=test_case['category'],
                emotion=test_case['emotion']
            )
            
            if success:
                print(f"✅ Generated: {test_case['filename']}")
            else:
                print(f"❌ Failed to generate: {test_case['filename']}")

def main():
    """Test the enhanced gTTS system"""
    
    # Install required packages if missing
    try:
        import pydub
    except ImportError:
        print("Installing pydub...")
        os.system("pip install pydub")
        import pydub
    
    tts = EngagingGTTS()
    tts.test_voice_styles()

if __name__ == "__main__":
    main()
