"""
Enhanced Bark TTS Service with Multiple Voices and Emotions
Creates engaging, varied audio with different speaking styles
"""

import os
import sys
import logging
import random
from typing import Dict, List, Optional, Tuple
import numpy as np
from pathlib import Path

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    from bark.generation import SUPPORTED_LANGS
    import scipy.io.wavfile as wavfile
    BARK_AVAILABLE = True
except ImportError:
    BARK_AVAILABLE = False
    print("⚠️ Bark TTS not available. Install with: pip install bark")

class EngagingBarkTTS:
    """Enhanced Bark TTS with multiple voices and emotional expressions"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.sample_rate = 24000  # Bark's sample rate
        
        # Voice presets for different news types
        self.voice_presets = {
            'breaking_news': {
                'voices': ['v2/en_speaker_9', 'v2/en_speaker_8', 'v2/en_speaker_7'],  # Authoritative voices
                'description': 'Authoritative, urgent news anchor style'
            },
            'tech_news': {
                'voices': ['v2/en_speaker_5', 'v2/en_speaker_6', 'v2/en_speaker_4'],  # Younger, tech-savvy
                'description': 'Tech-savvy, enthusiastic style'
            },
            'business_news': {
                'voices': ['v2/en_speaker_9', 'v2/en_speaker_8', 'v2/en_speaker_3'],  # Professional
                'description': 'Professional, confident business style'
            },
            'entertainment': {
                'voices': ['v2/en_speaker_1', 'v2/en_speaker_2', 'v2/en_speaker_0'],  # Lively, engaging
                'description': 'Lively, engaging entertainment style'
            },
            'sports': {
                'voices': ['v2/en_speaker_7', 'v2/en_speaker_8', 'v2/en_speaker_9'],  # Energetic
                'description': 'Energetic, exciting sports commentator style'
            },
            'default': {
                'voices': ['v2/en_speaker_6', 'v2/en_speaker_5', 'v2/en_speaker_4'],  # Balanced
                'description': 'Balanced, professional news style'
            }
        }
        
        # Emotional markers that can be added to text
        self.emotional_markers = {
            'excitement': ['♪', '!', '😮'],
            'urgency': ['⚡', '🚨', '⏰'],
            'surprise': ['😲', '🤯', '😱'],
            'importance': ['📢', '⭐', '🔥']
        }
        
        if BARK_AVAILABLE:
            try:
                self.logger.info("Loading Bark models...")
                preload_models()
                self.logger.info("✅ Bark models loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to load Bark models: {e}")
                self.logger.info("Will attempt to load models on first use")
    
    def _setup_logger(self):
        logger = logging.getLogger('EngagingBarkTTS')
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
                              category: str = 'general',
                              emotion: str = 'neutral',
                              voice_preference: Optional[str] = None) -> bool:
        """Generate engaging audio with appropriate voice and emotion"""
        
        if not BARK_AVAILABLE:
            self.logger.error("Bark TTS not available")
            return False
        
        try:
            # Select appropriate voice
            voice = self._select_voice(category, emotion, voice_preference)
            
            # Enhance text with emotional markers
            enhanced_text = self._add_emotional_markers(text, emotion, category)
            
            # Split long text into chunks for better quality
            chunks = self._split_text_intelligently(enhanced_text)
            
            all_audio = []
            
            for i, chunk in enumerate(chunks):
                self.logger.info(f"Generating audio chunk {i+1}/{len(chunks)}")
                
                # Add variety by slightly changing voice for different chunks
                chunk_voice = self._get_varied_voice(voice, i, len(chunks))
                
                # Generate audio for this chunk
                try:
                    audio_array = generate_audio(chunk, history_prompt=chunk_voice)
                    all_audio.append(audio_array)
                    
                    # Add brief pause between chunks
                    if i < len(chunks) - 1:
                        pause_duration = 0.3  # 0.3 seconds
                        pause_samples = int(pause_duration * self.sample_rate)
                        pause = np.zeros(pause_samples)
                        all_audio.append(pause)
                        
                except Exception as e:
                    self.logger.error(f"Error generating chunk {i+1}: {e}")
                    continue
            
            if not all_audio:
                self.logger.error("No audio chunks generated successfully")
                return False
            
            # Concatenate all audio chunks
            final_audio = np.concatenate(all_audio)
            
            # Enhance audio quality
            final_audio = self._enhance_audio_quality(final_audio)
            
            # Save to file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            wavfile.write(output_path, self.sample_rate, final_audio)
            
            self.logger.info(f"✅ Generated engaging audio: {output_path}")
            self.logger.info(f"   Voice: {voice} ({self.voice_presets.get(category, {}).get('description', 'Default')})")
            self.logger.info(f"   Duration: {len(final_audio) / self.sample_rate:.1f} seconds")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating engaging audio: {e}")
            return False
    
    def _select_voice(self, category: str, emotion: str, preference: Optional[str]) -> str:
        """Select the most appropriate voice for the content"""
        
        if preference:
            return preference
        
        # Map category to voice preset
        preset_key = category.lower() if category.lower() in self.voice_presets else 'default'
        voices = self.voice_presets[preset_key]['voices']
        
        # Select based on emotion
        if emotion == 'urgent' or emotion == 'breaking':
            # Use more authoritative voices for urgent news
            return voices[0]  # First voice is usually most authoritative
        elif emotion == 'exciting' or emotion == 'entertainment':
            # Use more lively voices
            return voices[-1]  # Last voice is usually more expressive
        else:
            # Random selection from appropriate voices
            return random.choice(voices)
    
    def _add_emotional_markers(self, text: str, emotion: str, category: str) -> str:
        """Add emotional markers to text for better expression"""
        
        # Don't over-modify the text, just add strategic emphasis
        if emotion == 'urgent' or category == 'breaking':
            # Add urgency markers
            text = text.replace('!', '! ⚡')
            if not text.endswith('!') and not text.endswith('.'):
                text += '!'
        
        elif emotion == 'exciting' or category == 'entertainment':
            # Add excitement markers
            text = text.replace('amazing', 'amazing ♪')
            text = text.replace('incredible', 'incredible 😮')
            text = text.replace('shocking', 'shocking 🤯')
        
        # Add natural speech patterns
        text = text.replace('. And', '. [pause] And')
        text = text.replace('. But', '. [pause] But')
        text = text.replace('. However', '. [pause] However')
        
        return text
    
    def _split_text_intelligently(self, text: str, max_chunk_length: int = 200) -> List[str]:
        """Split text into chunks at natural breaking points"""
        
        if len(text) <= max_chunk_length:
            return [text]
        
        # Split at sentence boundaries first
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Add the period back except for the last sentence
            sentence_with_period = sentence + '.' if sentence != sentences[-1] else sentence
            
            if len(current_chunk + sentence_with_period) <= max_chunk_length:
                current_chunk += sentence_with_period + " " if current_chunk else sentence_with_period
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence_with_period
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _get_varied_voice(self, base_voice: str, chunk_index: int, total_chunks: int) -> str:
        """Add subtle voice variation for longer content"""
        
        # For single chunk, use base voice
        if total_chunks == 1:
            return base_voice
        
        # For multiple chunks, occasionally vary the voice slightly
        if chunk_index > 0 and random.random() < 0.3:  # 30% chance of variation
            # Get voices from the same category
            for preset in self.voice_presets.values():
                if base_voice in preset['voices']:
                    alternate_voices = [v for v in preset['voices'] if v != base_voice]
                    if alternate_voices:
                        return random.choice(alternate_voices)
        
        return base_voice
    
    def _enhance_audio_quality(self, audio: np.ndarray) -> np.ndarray:
        """Apply audio enhancements for better quality"""
        
        # Normalize audio
        audio = audio.astype(np.float32)
        
        # Remove DC offset
        audio = audio - np.mean(audio)
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.95  # Leave some headroom
        
        # Convert back to int16 for wav file
        audio = (audio * 32767).astype(np.int16)
        
        return audio
    
    def get_available_voices(self) -> Dict[str, List[str]]:
        """Get list of available voices by category"""
        return {category: data['voices'] for category, data in self.voice_presets.items()}
    
    def test_voice(self, voice: str, output_path: str = "test_voice.wav") -> bool:
        """Test a specific voice with sample text"""
        
        test_text = "This is a test of the enhanced Bark text-to-speech system. How does this voice sound for news content?"
        
        return self.generate_engaging_audio(
            text=test_text,
            output_path=output_path,
            voice_preference=voice
        )

def test_engaging_tts():
    """Test the engaging TTS system"""
    
    tts = EngagingBarkTTS()
    
    if not BARK_AVAILABLE:
        print("❌ Bark TTS not available for testing")
        return
    
    # Test different categories and emotions
    test_cases = [
        {
            'text': "🚨 BREAKING: Apple just announced revolutionary AI technology that will change everything! This massive development shows incredible innovation in the tech industry.",
            'category': 'tech_news',
            'emotion': 'exciting',
            'output': 'test_tech_exciting.wav'
        },
        {
            'text': "URGENT UPDATE: Stock markets plunge as tech giant reports a whopping 15% decline in quarterly earnings. This shocking development affects millions of investors.",
            'category': 'business_news', 
            'emotion': 'urgent',
            'output': 'test_business_urgent.wav'
        },
        {
            'text': "You won't believe what just happened in sports today! The championship game had the most incredible ending anyone has ever seen.",
            'category': 'sports',
            'emotion': 'exciting',
            'output': 'test_sports_exciting.wav'
        }
    ]
    
    print("🎤 Testing Enhanced Bark TTS...")
    
    for i, test_case in enumerate(test_cases):
        print(f"\n📝 Test {i+1}: {test_case['category']} - {test_case['emotion']}")
        print(f"Text: {test_case['text'][:50]}...")
        
        success = tts.generate_engaging_audio(
            text=test_case['text'],
            output_path=test_case['output'],
            category=test_case['category'],
            emotion=test_case['emotion']
        )
        
        if success:
            print(f"✅ Generated: {test_case['output']}")
        else:
            print(f"❌ Failed to generate: {test_case['output']}")

if __name__ == "__main__":
    test_engaging_tts()
