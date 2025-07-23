"""
Enhanced Audio Service
High-quality text-to-speech generation with multiple providers and quality analysis
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
    import librosa
    import soundfile as sf
    AUDIO_PROCESSING_AVAILABLE = True
except ImportError:
    AUDIO_PROCESSING_AVAILABLE = False

load_dotenv('config.env')

@dataclass
class AudioMetrics:
    """Audio quality metrics"""
    duration: float
    sample_rate: int
    bit_rate: int
    file_size: int
    rms_energy: float
    quality_score: float
    
    def to_dict(self) -> Dict:
        return {
            'duration': self.duration,
            'sample_rate': self.sample_rate,
            'bit_rate': self.bit_rate,
            'file_size': self.file_size,
            'rms_energy': self.rms_energy,
            'quality_score': self.quality_score
        }

class EnhancedAudioService:
    def __init__(self):
        self.tts_service = os.getenv('TTS_SERVICE', 'gtts').lower()
        self.logger = self._setup_logger()
        
        # Quality settings
        self.min_duration = float(os.getenv('MIN_AUDIO_DURATION', '25'))
        self.max_duration = float(os.getenv('MAX_AUDIO_DURATION', '65'))
        
        # Initialize TTS providers
        self._init_providers()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for audio service"""
        logger = logging.getLogger('AudioService')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _init_providers(self):
        """Initialize available TTS providers"""
        self.providers = {}
        
        # Google TTS
        if GTTS_AVAILABLE:
            self.providers['gtts'] = self._gtts_generate
            self.logger.info("Google TTS available")
        
        # ElevenLabs
        if ELEVENLABS_AVAILABLE:
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if api_key and api_key != 'not_used':
                # Check if the elevenlabs module has the set_api_key attribute
                if hasattr(elevenlabs, 'set_api_key'):
                    elevenlabs.set_api_key(api_key)
                    self.providers['elevenlabs'] = self._elevenlabs_generate
                    self.logger.info("ElevenLabs TTS available")
                else:
                    self.logger.warning("ElevenLabs module structure is different than expected. Using only Google TTS.")
        
        # Azure Speech
        if AZURE_AVAILABLE:
            speech_key = os.getenv('AZURE_SPEECH_KEY')
            speech_region = os.getenv('AZURE_SPEECH_REGION')
            if speech_key and speech_region and speech_key != 'not_used' and speech_region != 'not_used':
                self.azure_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
                self.providers['azure'] = self._azure_generate
                self.logger.info("Azure Speech available")
        
        if not self.providers:
            raise RuntimeError("No TTS providers available. Please install required dependencies.")
    
    def generate_voiceover(self, 
                          script: str, 
                          output_path: str,
                          voice_settings: Dict = None,
                          category: str = 'general',
                          **kwargs) -> Optional[Tuple[str, AudioMetrics]]:
        """
        Generate high-quality voiceover from script
        
        Args:
            script: Text script to convert to speech
            output_path: Path where audio file should be saved
            voice_settings: Optional voice configuration
            
        Returns:
            Tuple of (audio_path, metrics) or None if failed
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Get voice settings
            settings = voice_settings or self._get_default_voice_settings()
            
            self.logger.info(f"Generating voiceover using {self.tts_service}")
            self.logger.info(f"Script length: {len(script)} characters")
            
            # Generate audio using selected provider
            if self.tts_service in self.providers:
                success = self.providers[self.tts_service](script, output_path, settings)
            else:
                self.logger.error(f"TTS provider '{self.tts_service}' not available")
                return None
            
            if not success:
                return None
            
            # Post-process audio for quality
            processed_path = self._post_process_audio(output_path)
            
            # Analyze audio quality
            metrics = self._analyze_audio_quality(processed_path)
            
            # Validate audio meets quality standards
            if not self._validate_audio_quality(metrics):
                self.logger.warning("Audio failed quality validation")
                return None
            
            self.logger.info(f"✅ Generated high-quality voiceover: {os.path.basename(processed_path)}")
            self.logger.info(f"Duration: {metrics.duration:.1f}s, Quality: {metrics.quality_score:.1f}%")
            
            return processed_path, metrics
            
        except Exception as e:
            self.logger.error(f"Error generating voiceover: {e}")
            return None
    
    def _gtts_generate(self, script: str, output_path: str, settings: Dict) -> bool:
        """Generate audio using Google TTS"""
        try:
            # Clean script for better pronunciation
            cleaned_script = self._clean_script_for_tts(script)
            
            # Create TTS object
            tts = gTTS(
                text=cleaned_script,
                lang=settings.get('language', 'en'),
                tld=settings.get('tld', 'com'),
                slow=settings.get('slow', False)
            )
            
            # Save audio file
            tts.save(output_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Google TTS error: {e}")
            return False
    
    def _elevenlabs_generate(self, script: str, output_path: str, settings: Dict) -> bool:
        """Generate audio using ElevenLabs"""
        try:
            voice_id = settings.get('voice_id', 'EXAVITQu4vr4xnSDxMaL')  # Bella voice
            
            audio = elevenlabs.generate(
                text=script,
                voice=voice_id,
                model=settings.get('model', 'eleven_monolingual_v1'),
                stream=False
            )
            
            # Save audio
            with open(output_path, 'wb') as f:
                f.write(audio)
            
            return True
            
        except Exception as e:
            self.logger.error(f"ElevenLabs TTS error: {e}")
            return False
    
    def _azure_generate(self, script: str, output_path: str, settings: Dict) -> bool:
        """Generate audio using Azure Speech"""
        try:
            # Configure voice
            self.azure_config.speech_synthesis_voice_name = settings.get('voice_name', 'en-US-JennyNeural')
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.azure_config,
                audio_config=speechsdk.audio.AudioOutputConfig(filename=output_path)
            )
            
            # Generate speech
            result = synthesizer.speak_text_async(script).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True
            else:
                self.logger.error(f"Azure TTS failed: {result.reason}")
                return False
                
        except Exception as e:
            self.logger.error(f"Azure TTS error: {e}")
            return False
    
    def _get_default_voice_settings(self) -> Dict:
        """Get default voice settings based on provider"""
        if self.tts_service == 'gtts':
            return {
                'language': 'en',
                'tld': 'com',
                'slow': False
            }
        elif self.tts_service == 'elevenlabs':
            return {
                'voice_id': 'EXAVITQu4vr4xnSDxMaL',  # Bella
                'model': 'eleven_monolingual_v1'
            }
        elif self.tts_service == 'azure':
            return {
                'voice_name': 'en-US-JennyNeural'
            }
        else:
            return {}
    
    def _clean_script_for_tts(self, script: str) -> str:
        """Clean script for better TTS pronunciation"""
        import re
        
        # Replace abbreviations and symbols
        replacements = {
            '&': 'and',
            '%': 'percent',
            '$': 'dollars',
            '€': 'euros',
            '£': 'pounds',
            '@': 'at',
            '#': 'hashtag',
            'w/': 'with',
            'w/o': 'without',
            'vs.': 'versus',
            'vs': 'versus',
            'etc.': 'etcetera',
            'e.g.': 'for example',
            'i.e.': 'that is'
        }
        
        for old, new in replacements.items():
            script = script.replace(old, new)
        
        # Fix common abbreviations
        script = re.sub(r'\\bUS\\b', 'United States', script)
        script = re.sub(r'\\bUK\\b', 'United Kingdom', script)
        script = re.sub(r'\\bAI\\b', 'A I', script)
        script = re.sub(r'\\bCEO\\b', 'C E O', script)
        script = re.sub(r'\\bFBI\\b', 'F B I', script)
        script = re.sub(r'\\bNASA\\b', 'NASA', script)
        script = re.sub(r'\\bCOVID-19\\b', 'COVID nineteen', script)
        script = re.sub(r'\\bCOVID\\b', 'COVID', script)
        
        # Fix numbers and dates
        script = re.sub(r'\\b2024\\b', 'twenty twenty four', script)
        script = re.sub(r'\\b2025\\b', 'twenty twenty five', script)
        
        # Remove extra whitespace
        script = ' '.join(script.split())
        
        return script
    
    def _post_process_audio(self, audio_path: str) -> str:
        """Post-process audio for better quality"""
        if not AUDIO_PROCESSING_AVAILABLE:
            return audio_path
        
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Normalize audio levels
            normalized_audio = audio.normalize()
            
            # Apply slight compression for better consistency
            # compressed_audio = normalized_audio.compress_dynamic_range()
            
            # Ensure consistent sample rate (44.1kHz)
            if normalized_audio.frame_rate != 44100:
                normalized_audio = normalized_audio.set_frame_rate(44100)
            
            # Export with high quality
            output_path = audio_path.replace('.mp3', '_processed.mp3')
            normalized_audio.export(
                output_path,
                format="mp3",
                bitrate="192k",
                parameters=["-q:a", "0"]  # Highest quality
            )
            
            # Replace original file
            os.replace(output_path, audio_path)
            
            return audio_path
            
        except Exception as e:
            self.logger.warning(f"Audio post-processing failed: {e}")
            return audio_path
    
    def _analyze_audio_quality(self, audio_path: str) -> AudioMetrics:
        """Analyze audio file quality metrics"""
        try:
            if AUDIO_PROCESSING_AVAILABLE:
                # Load with librosa for detailed analysis
                y, sr = librosa.load(audio_path)
                duration = librosa.get_duration(y=y, sr=sr)
                rms_energy = float(librosa.feature.rms(y=y).mean())
            else:
                # Basic analysis with pydub
                audio = AudioSegment.from_file(audio_path)
                duration = len(audio) / 1000.0  # Convert to seconds
                rms_energy = audio.rms / 1000.0  # Normalize
                sr = audio.frame_rate
            
            # Get file stats
            file_stats = os.stat(audio_path)
            file_size = file_stats.st_size
            
            # Estimate bitrate
            bit_rate = int((file_size * 8) / duration) if duration > 0 else 0
            
            # Calculate quality score
            quality_score = self._calculate_audio_quality_score(duration, sr, bit_rate, rms_energy)
            
            return AudioMetrics(
                duration=round(duration, 2),
                sample_rate=sr,
                bit_rate=bit_rate,
                file_size=file_size,
                rms_energy=round(rms_energy, 4),
                quality_score=round(quality_score, 1)
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing audio quality: {e}")
            # Return default metrics
            return AudioMetrics(
                duration=30.0,
                sample_rate=44100,
                bit_rate=128000,
                file_size=os.path.getsize(audio_path) if os.path.exists(audio_path) else 0,
                rms_energy=0.1,
                quality_score=50.0
            )
    
    def _calculate_audio_quality_score(self, duration: float, sample_rate: int, bit_rate: int, rms_energy: float) -> float:
        """Calculate overall audio quality score"""
        score = 0.0
        
        # Duration score (30%)
        if self.min_duration <= duration <= self.max_duration:
            score += 30
        elif duration < self.min_duration:
            score += 20 * (duration / self.min_duration)
        else:  # duration > max_duration
            score += 20 * (self.max_duration / duration)
        
        # Sample rate score (25%)
        if sample_rate >= 44100:
            score += 25
        elif sample_rate >= 22050:
            score += 20
        else:
            score += 10
        
        # Bit rate score (25%)
        if bit_rate >= 192000:
            score += 25
        elif bit_rate >= 128000:
            score += 20
        elif bit_rate >= 96000:
            score += 15
        else:
            score += 10
        
        # RMS energy score (20%) - indicates good audio levels
        if 0.05 <= rms_energy <= 0.3:
            score += 20
        elif 0.03 <= rms_energy < 0.05 or 0.3 < rms_energy <= 0.5:
            score += 15
        else:
            score += 10
        
        return min(score, 100.0)
    
    def _validate_audio_quality(self, metrics: AudioMetrics) -> bool:
        """Validate if audio meets minimum quality standards"""
        # Check duration
        if not (self.min_duration <= metrics.duration <= self.max_duration):
            self.logger.warning(f"Audio duration out of range: {metrics.duration}s")
            return False
        
        # Check quality score
        if metrics.quality_score < 60:  # Minimum 60% quality
            self.logger.warning(f"Audio quality too low: {metrics.quality_score}%")
            return False
        
        # Check file size (minimum 100KB for reasonable quality)
        if metrics.file_size < 100000:
            self.logger.warning(f"Audio file too small: {metrics.file_size} bytes")
            return False
        
        return True
    
    def generate_batch_voiceovers(self, articles: List[Dict], output_dir: str, max_workers: int = 4) -> List[Dict]:
        """
        Generate voiceovers for multiple articles in parallel for maximum speed
        
        Args:
            articles: List of article dictionaries with scripts
            output_dir: Directory to save audio files
            max_workers: Number of parallel workers
            
        Returns:
            List of articles with added 'audio_path' and 'audio_metrics' fields
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import threading
        
        os.makedirs(output_dir, exist_ok=True)
        
        successful_articles = []
        results_lock = threading.Lock()
        
        self.logger.info(f"🚀 Generating voiceovers for {len(articles)} articles in parallel with {max_workers} workers...")
        
        def generate_single_voiceover(article_data):
            """Generate voiceover for a single article (thread-safe)"""
            article, index = article_data
            try:
                title = article.get('title', f'Article_{index+1}')
                script = article.get('script', '')
                category = article.get('category', 'general')
                
                if not script:
                    self.logger.warning(f"No script found for article {index+1}")
                    return (index, None, False)
                
                # Create safe filename
                safe_title = self._create_safe_filename(title)
                audio_filename = f"{safe_title}.mp3"
                audio_path = os.path.join(output_dir, audio_filename)
                
                # Generate voiceover with gender-aware voice selection
                result = self.generate_voiceover(script, audio_path, category=category)
                
                if result:
                    final_path, metrics = result
                    
                    # Add audio info to article
                    article_copy = article.copy()
                    article_copy['audio_path'] = final_path
                    article_copy['audio_metrics'] = metrics.to_dict()
                    
                    return (index, article_copy, True)
                else:
                    self.logger.error(f"Failed to generate audio for article {index+1}")
                    return (index, None, False)
                    
            except Exception as e:
                self.logger.error(f"Error processing article {index+1}: {e}")
                return (index, None, False)
        
        # Use ThreadPoolExecutor for parallel audio generation
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all articles for processing
            article_data = [(article, i) for i, article in enumerate(articles)]
            future_to_article = {executor.submit(generate_single_voiceover, data): data for data in article_data}
            
            # Collect results as they complete
            completed_count = 0
            for future in as_completed(future_to_article):
                completed_count += 1
                index, article_with_audio, success = future.result()
                
                if success and article_with_audio:
                    with results_lock:
                        successful_articles.append(article_with_audio)
                
                # Log progress
                self.logger.info(f"🎤 Completed audio {completed_count}/{len(articles)}")
        
        self.logger.info(f"🎉 Successfully generated {len(successful_articles)}/{len(articles)} voiceovers in parallel")
        return successful_articles
    
    def _create_safe_filename(self, title: str) -> str:
        """Create a safe filename from article title"""
        import re
        
        # Remove special characters and limit length
        safe_title = re.sub(r'[^a-zA-Z0-9\s\-_]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title.strip())
        safe_title = safe_title[:50]  # Limit length
        
        if not safe_title:
            safe_title = f"article_{int(time.time())}"
        
        return safe_title
    
    def save_audio_report(self, articles_with_audio: List[Dict], output_dir: str) -> str:
        """Save audio generation report"""
        os.makedirs(output_dir, exist_ok=True)
        
        report = {
            'generation_time': datetime.now().isoformat(),
            'total_articles': len(articles_with_audio),
            'tts_provider': self.tts_service,
            'total_duration': sum(article.get('audio_metrics', {}).get('duration', 0) for article in articles_with_audio),
            'average_quality': sum(article.get('audio_metrics', {}).get('quality_score', 0) for article in articles_with_audio) / len(articles_with_audio) if articles_with_audio else 0,
            'articles': [{
                'title': article.get('title', ''),
                'audio_path': article.get('audio_path', ''),
                'metrics': article.get('audio_metrics', {})
            } for article in articles_with_audio]
        }
        
        report_path = os.path.join(output_dir, f"audio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved audio report to {report_path}")
        return report_path

# Legacy compatibility
class TTSGenerator(EnhancedAudioService):
    """Backward compatibility wrapper"""
    
    def generate_voiceover(self, script: str, output_path: str, **kwargs) -> str:
        """Legacy method signature"""
        result = super().generate_voiceover(script, output_path)
        return result[0] if result else None
