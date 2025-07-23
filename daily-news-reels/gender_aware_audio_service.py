"""
Enhanced Audio Service with Gender-Aware Voice Selection
Supports realistic male/female voices with avatar matching
"""

import os
import logging
import tempfile
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import librosa
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

# Import voice gender system
from voice_gender_system import VoiceGenderSystem, VoiceGender, VoiceStyle

@dataclass
class AudioMetrics:
    duration: float
    quality_score: float
    clarity_score: float
    volume_level: float
    voice_profile: str

class GenderAwareAudioService:
    """Enhanced audio service with realistic male/female voice selection"""
    
    def __init__(self):
        self.logger = logging.getLogger('GenderAwareAudioService')
        self.voice_system = VoiceGenderSystem()
        
        # Audio processing settings
        self.sample_rate = 22050
        self.target_duration_range = (25, 90)  # seconds
        self.quality_threshold = 70
        
        # Initialize audio processing
        self._setup_audio_processing()
    
    def _setup_audio_processing(self):
        """Setup audio processing capabilities"""
        try:
            # Test audio libraries
            test_audio = np.array([0.1, 0.2, 0.1])
            librosa.resample(test_audio, orig_sr=22050, target_sr=22050)
            self.logger.info("✅ Audio processing initialized")
        except Exception as e:
            self.logger.warning(f"Audio processing setup issue: {e}")
    
    def generate_gendered_voiceover(self,
                                  script: str,
                                  output_path: str,
                                  category: str = 'general',
                                  preferred_gender: Optional[VoiceGender] = None,
                                  preferred_style: Optional[VoiceStyle] = None,
                                  session_consistency: bool = True) -> Optional[Tuple[str, AudioMetrics, Dict]]:
        """
        Generate voiceover with specific gender and style preferences
        
        Args:
            script: Text to convert to speech
            output_path: Output audio file path
            category: News category for optimal voice selection
            preferred_gender: Force specific gender (male/female)
            preferred_style: Force specific style
            session_consistency: Maintain consistency within session
        
        Returns:
            Tuple of (audio_path, metrics, avatar_config) or None if failed
        """
        
        try:
            self.logger.info(f"🎤 Generating gendered voiceover for {category}")
            
            # Select optimal voice profile
            voice_profile = self.voice_system.select_voice_profile(
                category=category,
                preferred_gender=preferred_gender,
                preferred_style=preferred_style,
                session_consistency=session_consistency
            )
            
            # Get voice settings for gTTS
            voice_settings = self.voice_system.get_voice_settings_for_gtts(voice_profile)
            
            # Get matching avatar configuration
            avatar_config = self.voice_system.get_avatar_settings(voice_profile)
            
            # Process script for better speech
            processed_script = self._process_script_for_speech(script, voice_profile)
            
            # Generate base audio with gTTS
            base_audio_path = self._generate_base_audio(processed_script, voice_settings)
            if not base_audio_path:
                return None
            
            # Apply voice-specific enhancements
            enhanced_audio_path = self._apply_voice_enhancements(
                base_audio_path, 
                output_path, 
                voice_profile
            )
            
            # Analyze audio quality
            metrics = self._analyze_audio_quality(enhanced_audio_path, voice_profile)
            
            # Validate quality
            if metrics.quality_score < self.quality_threshold:
                self.logger.warning(f"Audio quality below threshold: {metrics.quality_score:.1f}%")
                return None
            
            self.logger.info(f"✅ Generated {voice_profile.gender.value} voiceover: {metrics.duration:.1f}s, Quality: {metrics.quality_score:.1f}%")
            
            return enhanced_audio_path, metrics, avatar_config
            
        except Exception as e:
            self.logger.error(f"Error generating gendered voiceover: {e}")
            return None
        finally:
            # Cleanup temp files
            self._cleanup_temp_files()
    
    def _generate_base_audio(self, script: str, voice_settings: Dict) -> Optional[str]:
        """Generate base audio using gTTS with specific voice settings"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            
            # Generate with gTTS
            tts = gTTS(
                text=script,
                lang=voice_settings['language'],
                tld=voice_settings['tld'],
                slow=voice_settings['slow']
            )
            
            tts.save(temp_path)
            
            self.logger.info(f"✅ Base audio generated with {voice_settings['tld']} accent")
            return temp_path
            
        except Exception as e:
            self.logger.error(f"Error generating base audio: {e}")
            return None
    
    def _apply_voice_enhancements(self, 
                                input_path: str, 
                                output_path: str, 
                                voice_profile) -> str:
        """Apply voice-specific audio enhancements"""
        try:
            # Load audio
            audio = AudioSegment.from_mp3(input_path)
            
            # Apply speed adjustment
            if voice_profile.speed != 1.0:
                audio = audio.speedup(playback_speed=voice_profile.speed)
            
            # Apply pitch shifting for gender characteristics
            if voice_profile.pitch_shift != 0:
                # Simple pitch shift using frame rate manipulation
                new_sample_rate = int(audio.frame_rate * (1 + voice_profile.pitch_shift * 0.05))
                audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
                audio = audio.set_frame_rate(22050)
            
            # Apply gender-specific processing
            if voice_profile.gender == VoiceGender.MALE:
                # Male voice enhancements - deeper, more authoritative
                audio = audio + 1  # Slight volume boost
                audio = compress_dynamic_range(audio, threshold=-25.0, ratio=2.0)
            else:
                # Female voice enhancements - clearer, more dynamic
                audio = audio + 0.5  # Slight volume boost
                audio = compress_dynamic_range(audio, threshold=-20.0, ratio=3.0)
            
            # Apply style-specific effects
            if voice_profile.style == VoiceStyle.ENERGETIC:
                audio = audio + 2  # More volume for energetic style
                audio = compress_dynamic_range(audio, threshold=-15.0, ratio=3.0)
            elif voice_profile.style == VoiceStyle.AUTHORITATIVE:
                audio = compress_dynamic_range(audio, threshold=-30.0, ratio=2.0)  # More controlled
            
            # Normalize and add professional touches
            audio = normalize(audio)
            
            # Add fade in/out for professional sound
            fade_duration = min(200, len(audio) // 10)
            audio = audio.fade_in(fade_duration).fade_out(fade_duration)
            
            # Save enhanced audio
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            audio.export(output_path, format="wav")
            
            self.logger.info(f"✅ Applied {voice_profile.gender.value} voice enhancements")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error applying voice enhancements: {e}")
            return input_path  # Return original if enhancement fails
    
    def _process_script_for_speech(self, script: str, voice_profile) -> str:
        """Process script for better speech based on voice profile"""
        
        # Basic text cleaning
        processed = script.strip()
        
        # Remove markdown and HTML tags
        import re
        processed = re.sub(r'[*_#`]', '', processed)
        processed = re.sub(r'<[^>]+>', '', processed)
        
        # Gender-specific text processing
        if voice_profile.gender == VoiceGender.MALE:
            # Male voice - emphasize authority words
            authority_words = ['breaking', 'urgent', 'major', 'significant', 'important']
            for word in authority_words:
                processed = processed.replace(word, f"{word} ")
        else:
            # Female voice - emphasize clarity and engagement
            engagement_words = ['incredible', 'amazing', 'exciting', 'remarkable']
            for word in engagement_words:
                processed = processed.replace(word, f"{word} ")
        
        # Style-specific processing
        if voice_profile.style == VoiceStyle.ENERGETIC:
            # Add energy markers
            processed = processed.replace('!', '! ')
            processed = processed.replace('...', '... ')
        elif voice_profile.style == VoiceStyle.AUTHORITATIVE:
            # Add authority pauses
            processed = processed.replace('.', '. ')
            processed = processed.replace(',', ', ')
        
        # Expand abbreviations for better pronunciation
        abbreviations = {
            'AI': 'A I',
            'CEO': 'C E O',
            'FBI': 'F B I',
            'USA': 'U S A',
            'UK': 'U K',
            'EU': 'E U',
            'NASA': 'N A S A'
        }
        
        for abbr, expansion in abbreviations.items():
            processed = processed.replace(abbr, expansion)
        
        return processed
    
    def _analyze_audio_quality(self, audio_path: str, voice_profile) -> AudioMetrics:
        """Analyze audio quality with voice profile context"""
        try:
            # Load audio for analysis
            audio_segment = AudioSegment.from_wav(audio_path)
            
            # Basic metrics
            duration = len(audio_segment) / 1000.0  # Convert to seconds
            
            # Load with librosa for detailed analysis
            y, sr = librosa.load(audio_path, sr=None)
            
            # Quality scoring based on various factors
            quality_score = 100.0
            
            # Duration check
            if duration < self.target_duration_range[0]:
                quality_score -= 20
            elif duration > self.target_duration_range[1]:
                quality_score -= 15
            
            # Clarity analysis
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            clarity_score = min(100, np.mean(spectral_centroids) / 50)
            
            # Volume analysis
            rms = librosa.feature.rms(y=y)[0]
            volume_level = np.mean(rms) * 100
            
            # Gender-specific quality adjustments
            if voice_profile.gender == VoiceGender.MALE:
                # Check for appropriate depth (lower frequencies)
                if np.mean(spectral_centroids) > 3000:
                    quality_score -= 10  # Too high-pitched for male
            else:
                # Check for appropriate clarity (higher frequencies)
                if np.mean(spectral_centroids) < 1500:
                    quality_score -= 10  # Too low-pitched for female
            
            # Style-specific adjustments
            if voice_profile.style == VoiceStyle.ENERGETIC:
                if volume_level < 30:
                    quality_score -= 15  # Not energetic enough
            elif voice_profile.style == VoiceStyle.AUTHORITATIVE:
                if volume_level > 80:
                    quality_score -= 10  # Too loud for authority
            
            quality_score = max(0, min(100, quality_score))
            
            return AudioMetrics(
                duration=duration,
                quality_score=quality_score,
                clarity_score=clarity_score,
                volume_level=volume_level,
                voice_profile=f"{voice_profile.gender.value}_{voice_profile.style.value}"
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing audio quality: {e}")
            return AudioMetrics(
                duration=0,
                quality_score=0,
                clarity_score=0,
                volume_level=0,
                voice_profile="unknown"
            )
    
    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            # This would clean up any temporary files created during processing
            pass
        except Exception as e:
            self.logger.warning(f"Cleanup warning: {e}")
    
    def get_session_voice_info(self) -> Dict:
        """Get information about current session voice settings"""
        return self.voice_system.generate_session_report()
    
    def reset_voice_session(self):
        """Reset voice session for new variety"""
        self.voice_system.reset_session()
        self.logger.info("🔄 Voice session reset - will select new voice characteristics")
    
    def test_voice_options(self, script: str = "This is a test of the voice generation system."):
        """Test different voice options"""
        print("🎤 Testing Voice Gender Options...")
        
        test_categories = ['business', 'technology', 'sports', 'entertainment']
        genders = [VoiceGender.MALE, VoiceGender.FEMALE]
        
        for category in test_categories:
            print(f"\n📂 Category: {category}")
            
            for gender in genders:
                print(f"   🎵 Testing {gender.value} voice...")
                
                result = self.generate_gendered_voiceover(
                    script=script,
                    output_path=f"test_{category}_{gender.value}.wav",
                    category=category,
                    preferred_gender=gender,
                    session_consistency=False
                )
                
                if result:
                    audio_path, metrics, avatar_config = result
                    print(f"      ✅ Generated: {metrics.voice_profile}")
                    print(f"      📊 Quality: {metrics.quality_score:.1f}%")
                    print(f"      ⏱️  Duration: {metrics.duration:.1f}s")
                    print(f"      👤 Avatar: {avatar_config['gender']} {avatar_config['style']}")
                else:
                    print(f"      ❌ Failed to generate")

def main():
    """Test the gender-aware audio service"""
    audio_service = GenderAwareAudioService()
    
    # Test script
    test_script = """
    Breaking news from the technology sector: Apple has just announced a revolutionary 
    AI breakthrough that could change the entire industry. This incredible development 
    promises to transform how we interact with our devices.
    """
    
    print("🚀 Testing Gender-Aware Audio Service...")
    
    # Test male business voice
    print("\n🚹 Testing Male Business Voice...")
    result = audio_service.generate_gendered_voiceover(
        script=test_script,
        output_path="test_male_business.wav",
        category="business",
        preferred_gender=VoiceGender.MALE,
        session_consistency=False
    )
    
    if result:
        audio_path, metrics, avatar_config = result
        print(f"✅ Generated male voice: {metrics.voice_profile}")
        print(f"📊 Quality: {metrics.quality_score:.1f}%")
        print(f"👤 Avatar: {avatar_config}")
    
    # Test female technology voice
    print("\n🚺 Testing Female Technology Voice...")
    result = audio_service.generate_gendered_voiceover(
        script=test_script,
        output_path="test_female_tech.wav",
        category="technology",
        preferred_gender=VoiceGender.FEMALE,
        session_consistency=False
    )
    
    if result:
        audio_path, metrics, avatar_config = result
        print(f"✅ Generated female voice: {metrics.voice_profile}")
        print(f"📊 Quality: {metrics.quality_score:.1f}%")
        print(f"👤 Avatar: {avatar_config}")
    
    # Test voice options
    audio_service.test_voice_options()

if __name__ == "__main__":
    main()
