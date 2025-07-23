"""
Enhanced Emotional Audio Service
Generates human-like voices with emotions, modulation, and personality
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass
import time
from datetime import datetime
import json
from pathlib import Path
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add src to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.emotional_voice_system import EmotionalVoiceSystem, VoiceEmotion, EmotionalVoiceProfile

# TTS Providers
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import elevenlabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

# Audio processing
try:
    from pydub import AudioSegment
    from pydub.effects import speedup, normalize
    import librosa
    import soundfile as sf
    AUDIO_PROCESSING_AVAILABLE = True
except ImportError:
    AUDIO_PROCESSING_AVAILABLE = False

load_dotenv('config.env')

@dataclass
class EnhancedAudioMetrics:
    """Enhanced audio quality metrics with emotion data"""
    duration: float
    sample_rate: int
    bit_rate: int
    file_size: int
    rms_energy: float
    quality_score: float
    emotion: str
    personality_traits: List[str]
    modulation_applied: bool
    
    def to_dict(self) -> Dict:
        return {
            'duration': self.duration,
            'sample_rate': self.sample_rate,
            'bit_rate': self.bit_rate,
            'file_size': self.file_size,
            'rms_energy': self.rms_energy,
            'quality_score': self.quality_score,
            'emotion': self.emotion,
            'personality_traits': self.personality_traits,
            'modulation_applied': self.modulation_applied
        }

class EnhancedEmotionalAudioService:
    """Audio service with emotional intelligence and voice modulation"""
    
    def __init__(self):
        self.tts_service = os.getenv('TTS_SERVICE', 'gtts').lower()
        self.logger = self._setup_logger()
        
        # Quality settings
        self.min_duration = float(os.getenv('MIN_AUDIO_DURATION', '15'))
        self.max_duration = float(os.getenv('MAX_AUDIO_DURATION', '60'))
        
        # Initialize emotional voice system
        self.emotional_voice = EmotionalVoiceSystem()
        
        # Voice modulation settings
        self.voice_personalities = self._init_voice_personalities()
        self.emotional_effects = self._init_emotional_effects()
        
        # Threading lock
        self.processing_lock = threading.Lock()
        
        # Initialize providers
        self._init_providers()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('EnhancedAudioService')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _init_providers(self):
        """Initialize TTS providers"""
        self.providers = {}
        
        if GTTS_AVAILABLE:
            self.providers['gtts'] = self._enhanced_gtts_generate
            self.logger.info("Enhanced Google TTS available")
        
        if not self.providers:
            self.logger.error("No TTS providers available!")
    
    def _init_voice_personalities(self) -> Dict[str, Dict]:
        """Initialize voice personality configurations"""
        return {
            'enthusiastic_host': {
                'speed_range': (1.05, 1.25),
                'pitch_variation': 0.3,
                'volume_boost': 1.2,
                'pause_multiplier': 0.8,
                'description': 'Energetic, upbeat, engaging'
            },
            'friendly_narrator': {
                'speed_range': (0.95, 1.15),
                'pitch_variation': 0.2,
                'volume_boost': 1.0,
                'pause_multiplier': 1.0,
                'description': 'Warm, conversational, relatable'
            },
            'dramatic_announcer': {
                'speed_range': (0.85, 1.05),
                'pitch_variation': 0.4,
                'volume_boost': 1.3,
                'pause_multiplier': 1.5,
                'description': 'Bold, impactful, attention-grabbing'
            },
            'casual_friend': {
                'speed_range': (1.0, 1.2),
                'pitch_variation': 0.25,
                'volume_boost': 0.9,
                'pause_multiplier': 0.9,
                'description': 'Relaxed, natural, authentic'
            },
            'excited_reporter': {
                'speed_range': (1.1, 1.3),
                'pitch_variation': 0.35,
                'volume_boost': 1.4,
                'pause_multiplier': 0.7,
                'description': 'Fast-paced, energetic, breaking news style'
            }
        }
    
    def _init_emotional_effects(self) -> Dict[VoiceEmotion, Dict]:
        """Initialize emotional audio effects"""
        return {
            VoiceEmotion.EXCITED: {
                'speed_modifier': 1.15,
                'pitch_shift': +3,
                'volume_boost': 1.2,
                'add_reverb': False,
                'compress': True
            },
            VoiceEmotion.SURPRISED: {
                'speed_modifier': 0.95,
                'pitch_shift': +5,
                'volume_boost': 1.1,
                'add_reverb': False,
                'compress': True
            },
            VoiceEmotion.CONCERNED: {
                'speed_modifier': 0.9,
                'pitch_shift': -2,
                'volume_boost': 0.9,
                'add_reverb': True,
                'compress': False
            },
            VoiceEmotion.CONFIDENT: {
                'speed_modifier': 1.0,
                'pitch_shift': 0,
                'volume_boost': 1.1,
                'add_reverb': False,
                'compress': True
            },
            VoiceEmotion.PLAYFUL: {
                'speed_modifier': 1.1,
                'pitch_shift': +2,
                'volume_boost': 1.15,
                'add_reverb': False,
                'compress': True
            },
            VoiceEmotion.DRAMATIC: {
                'speed_modifier': 0.85,
                'pitch_shift': -1,
                'volume_boost': 1.3,
                'add_reverb': True,
                'compress': True
            }
        }
    
    def select_voice_personality(self, emotion: VoiceEmotion, category: str) -> str:
        """Select voice personality based on emotion and content category"""
        
        personality_mapping = {
            VoiceEmotion.EXCITED: 'enthusiastic_host',
            VoiceEmotion.SURPRISED: 'excited_reporter',
            VoiceEmotion.CONCERNED: 'dramatic_announcer',
            VoiceEmotion.CONFIDENT: 'friendly_narrator',
            VoiceEmotion.PLAYFUL: 'casual_friend',
            VoiceEmotion.DRAMATIC: 'dramatic_announcer',
            VoiceEmotion.SARCASTIC: 'casual_friend',
            VoiceEmotion.WARM: 'friendly_narrator'
        }
        
        # Category-specific overrides
        if category == 'sports' and emotion in [VoiceEmotion.EXCITED, VoiceEmotion.PLAYFUL]:
            return 'excited_reporter'
        elif category == 'technology' and emotion == VoiceEmotion.EXCITED:
            return 'enthusiastic_host'
        elif category == 'business' and emotion == VoiceEmotion.CONFIDENT:
            return 'friendly_narrator'
        
        return personality_mapping.get(emotion, 'friendly_narrator')
    
    def generate_emotional_voiceover(self, script: str, title: str, category: str = 'general', 
                                   target_emotion: Optional[VoiceEmotion] = None) -> Tuple[Optional[str], Optional[EnhancedAudioMetrics]]:
        """Generate emotionally-aware voiceover with personality"""
        
        if not script:
            self.logger.error("No script provided")
            return None, None
        
        try:
            # Determine emotion and personality
            if target_emotion:
                emotion = target_emotion
            else:
                emotion = self.emotional_voice.select_emotion_for_content(category, title, script)
            
            # Handle string emotions from content processor
            if isinstance(emotion, str):
                try:
                    emotion = VoiceEmotion(emotion)
                except ValueError:
                    emotion = VoiceEmotion.EXCITED  # Default fallback
            
            personality = self.select_voice_personality(emotion, category)
            
            self.logger.info(f"Generating {emotion.value} voice with {personality} personality")
            
            # Debug emotion system
            self.logger.info(f"Emotion type: {type(emotion)}")
            self.logger.info(f"Available emotions in system: {list(self.emotional_voice.emotional_emphasis.keys())}")
            self.logger.info(f"Emotion in dictionary: {emotion in self.emotional_voice.emotional_emphasis}")
            
            # Enhance script with emotional markers
            enhanced_script = self.emotional_voice.add_emotional_markers(script, emotion)
            
            # Generate base audio
            audio_path = self._generate_base_audio(enhanced_script, title)
            if not audio_path:
                return None, None
            
            # Apply emotional modulation
            modulated_path = self._apply_emotional_modulation(
                audio_path, emotion, personality, category
            )
            
            # Calculate enhanced metrics
            metrics = self._calculate_enhanced_metrics(
                modulated_path, emotion, [personality, emotion.value], True
            )
            
            self.logger.info(f"✅ Generated emotional voiceover: {os.path.basename(modulated_path)}")
            self.logger.info(f"Emotion: {emotion.value}, Personality: {personality}, Duration: {metrics.duration:.1f}s")
            
            return modulated_path, metrics
            
        except Exception as e:
            self.logger.error(f"Error generating emotional voiceover: {str(e)}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return None, None
    
    def _generate_base_audio(self, script: str, title: str) -> Optional[str]:
        """Generate base audio using available TTS provider"""
        
        provider = self.tts_service if self.tts_service in self.providers else list(self.providers.keys())[0]
        
        if provider not in self.providers:
            self.logger.error(f"Provider {provider} not available")
            return None
        
        return self.providers[provider](script, title)
    
    def _enhanced_gtts_generate(self, script: str, title: str) -> Optional[str]:
        """Enhanced Google TTS with better voice selection"""
        
        try:
            # Clean script for TTS
            clean_script = self._clean_script_for_tts(script)
            
            # Use different languages/accents for variety
            voice_options = [
                {'lang': 'en', 'tld': 'us'},     # American English
                {'lang': 'en', 'tld': 'co.uk'},  # British English
                {'lang': 'en', 'tld': 'com.au'}, # Australian English
                {'lang': 'en', 'tld': 'ca'},     # Canadian English
            ]
            
            voice_config = random.choice(voice_options)
            
            self.logger.info(f"Using gTTS with {voice_config}")
            
            tts = gTTS(
                text=clean_script,
                lang=voice_config['lang'],
                tld=voice_config['tld'],
                slow=False
            )
            
            # Create filename
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()[:50]
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"emotional_{safe_title}_{timestamp}.mp3"
            
            # Save to temp location first
            temp_path = os.path.join("output", "temp", filename)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            
            tts.save(temp_path)
            
            self.logger.info(f"Generated base audio: {filename}")
            return temp_path
            
        except Exception as e:
            self.logger.error(f"Error with enhanced gTTS: {e}")
            return None
    
    def _clean_script_for_tts(self, script: str) -> str:
        """Clean script for optimal TTS processing"""
        
        # Remove SSML tags that gTTS doesn't support
        clean_script = re.sub(r'<[^>]+>', '', script)
        
        # Convert emphasis markers to natural pauses
        clean_script = re.sub(r'\.\.\.\.+', '... ', clean_script)
        clean_script = re.sub(r'([.!?])\s*([.!?])', r'\1 \2', clean_script)
        
        # Normalize spacing
        clean_script = re.sub(r'\s+', ' ', clean_script)
        clean_script = clean_script.strip()
        
        return clean_script
    
    def _apply_emotional_modulation(self, audio_path: str, emotion: VoiceEmotion, 
                                  personality: str, category: str) -> str:
        """Apply emotional effects and personality to audio"""
        
        if not AUDIO_PROCESSING_AVAILABLE:
            self.logger.warning("Audio processing not available, returning original")
            return audio_path
        
        try:
            # Load audio
            audio = AudioSegment.from_mp3(audio_path)
            
            # Get emotional effects
            effects = self.emotional_effects.get(emotion, {})
            personality_config = self.voice_personalities.get(personality, {})
            
            # Apply speed modification
            speed_modifier = effects.get('speed_modifier', 1.0)
            if speed_modifier != 1.0:
                # Adjust speed while preserving pitch
                if hasattr(audio, 'speedup'):
                    audio = speedup(audio, playback_speed=speed_modifier)
                else:
                    # Fallback: change frame rate
                    audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * speed_modifier)})
                    audio = audio.set_frame_rate(audio.frame_rate)
            
            # Apply volume boost
            volume_boost = effects.get('volume_boost', 1.0)
            if volume_boost != 1.0:
                volume_change = 20 * (volume_boost - 1.0)  # Convert to dB
                audio = audio + volume_change
            
            # Normalize audio
            audio = normalize(audio)
            
            # Ensure good quality
            audio = audio.set_frame_rate(22050).set_channels(1)
            
            # Create output filename
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_filename = f"{base_name}_emotional.mp3"
            output_path = os.path.join("output", "sessions", datetime.now().strftime("%Y%m%d_%H%M%S"), "audio", output_filename)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Export with high quality
            audio.export(
                output_path,
                format="mp3",
                bitrate="128k",
                parameters=["-ar", "22050", "-ac", "1"]
            )
            
            self.logger.info(f"Applied {emotion.value} modulation with {personality} personality")
            
            # Clean up temp file
            try:
                os.remove(audio_path)
            except:
                pass
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error applying emotional modulation: {e}")
            return audio_path
    
    def _calculate_enhanced_metrics(self, audio_path: str, emotion: VoiceEmotion, 
                                  personality_traits: List[str], modulation_applied: bool) -> EnhancedAudioMetrics:
        """Calculate enhanced audio metrics"""
        
        try:
            if AUDIO_PROCESSING_AVAILABLE:
                audio = AudioSegment.from_mp3(audio_path)
                duration = len(audio) / 1000.0
                sample_rate = audio.frame_rate
                
                # Calculate RMS energy
                samples = audio.get_array_of_samples()
                rms_energy = (sum(sample**2 for sample in samples) / len(samples)) ** 0.5 / (2**15)
            else:
                # Fallback calculations
                file_size = os.path.getsize(audio_path)
                duration = max(file_size / 15000, 10.0)  # Rough estimate
                sample_rate = 22050
                rms_energy = 0.1
            
            # File metrics
            file_size = os.path.getsize(audio_path)
            bit_rate = int((file_size * 8) / duration) if duration > 0 else 128000
            
            # Quality score based on emotion appropriateness
            base_quality = 85.0
            
            # Bonus for emotional appropriateness
            if modulation_applied:
                base_quality += 5.0
            
            # Duration appropriateness
            if self.min_duration <= duration <= self.max_duration:
                base_quality += 10.0
            elif duration < self.min_duration:
                base_quality -= 5.0
            
            quality_score = min(base_quality, 100.0)
            
            return EnhancedAudioMetrics(
                duration=round(duration, 1),
                sample_rate=sample_rate,
                bit_rate=bit_rate,
                file_size=file_size,
                rms_energy=round(rms_energy, 4),
                quality_score=quality_score,
                emotion=emotion.value,
                personality_traits=personality_traits,
                modulation_applied=modulation_applied
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            return EnhancedAudioMetrics(
                duration=30.0, sample_rate=22050, bit_rate=128000,
                file_size=0, rms_energy=0.1, quality_score=70.0,
                emotion=emotion.value, personality_traits=personality_traits,
                modulation_applied=modulation_applied
            )
    
    def generate_batch_emotional_voiceovers(self, articles: List[Dict], max_workers: int = 4) -> List[Dict]:
        """Generate emotional voiceovers for multiple articles in parallel"""
        
        self.logger.info(f"🎤 Generating emotional voiceovers for {len(articles)} articles with {max_workers} workers...")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all articles for processing
            future_to_article = {
                executor.submit(
                    self.generate_emotional_voiceover,
                    article['script'],
                    article['title'],
                    article.get('category', 'general')
                ): article for article in articles
            }
            
            # Collect results
            for future in as_completed(future_to_article):
                article = future_to_article[future]
                try:
                    audio_path, metrics = future.result()
                    if audio_path and metrics:
                        result = {
                            'title': article['title'],
                            'audio_path': audio_path,
                            'metrics': metrics.to_dict(),
                            'emotion': metrics.emotion,
                            'personality': metrics.personality_traits
                        }
                        results.append(result)
                        self.logger.info(f"🎤 Completed emotional audio {len(results)}/{len(articles)}")
                    else:
                        self.logger.error(f"Failed to generate audio for: {article['title'][:50]}...")
                except Exception as e:
                    self.logger.error(f"Error processing article audio: {e}")
        
        self.logger.info(f"🎉 Successfully generated {len(results)}/{len(articles)} emotional voiceovers")
        return results
    
    # Legacy compatibility method
    def generate_voiceover(self, script: str, title: str, category: str = 'general', **kwargs) -> Tuple[Optional[str], Optional[Dict]]:
        """Legacy method for compatibility"""
        
        audio_path, metrics = self.generate_emotional_voiceover(script, title, category)
        
        if metrics:
            # Convert to legacy format
            legacy_metrics = {
                'duration': metrics.duration,
                'sample_rate': metrics.sample_rate,
                'bit_rate': metrics.bit_rate,
                'file_size': metrics.file_size,
                'rms_energy': metrics.rms_energy,
                'quality_score': metrics.quality_score
            }
            return audio_path, legacy_metrics
        
        return audio_path, None
