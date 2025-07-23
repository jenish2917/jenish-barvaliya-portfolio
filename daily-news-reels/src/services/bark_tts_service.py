
"""
Bark TTS Service - High-quality offline text-to-speech using Bark by Suno
No API keys required, unlimited usage, natural-sounding voices with emotions
"""

import os
import logging
import torch
import numpy as np
from typing import Optional, List, Dict
import tempfile
import json
from pathlib import Path

try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    from bark.generation import SUPPORTED_LANGS
    from scipy.io.wavfile import write as write_wav
    BARK_AVAILABLE = True
except ImportError:
    BARK_AVAILABLE = False

class BarkTTSService:
    """High-quality offline TTS using Bark by Suno"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sample_rate = 24000  # Bark's native sample rate
        self.models_loaded = False
        
        # Voice presets for different styles
        self.voice_presets = {
            'news_anchor_male': 'v2/en_speaker_6',
            'news_anchor_female': 'v2/en_speaker_9', 
            'professional_male': 'v2/en_speaker_7',
            'professional_female': 'v2/en_speaker_8',
            'casual_male': 'v2/en_speaker_0',
            'casual_female': 'v2/en_speaker_1',
            'energetic_male': 'v2/en_speaker_2',
            'energetic_female': 'v2/en_speaker_3',
            'calm_male': 'v2/en_speaker_4',
            'calm_female': 'v2/en_speaker_5'
        }
        
        # Check if Bark is available
        if not BARK_AVAILABLE:
            self.logger.warning("Bark TTS not available. Install with: pip install git+https://github.com/suno-ai/bark.git")
            self.logger.warning("Also install: pip install scipy")
        else:
            self.logger.info("Bark TTS available - High-quality offline voice synthesis ready")
            
    def is_available(self) -> bool:
        """Check if Bark TTS is available"""
        return BARK_AVAILABLE
    
    def initialize(self) -> bool:
        """Initialize and preload Bark models"""
        if not BARK_AVAILABLE:
            return False
            
        try:
            self.logger.info("Loading Bark models (this may take a few minutes on first run)...")
            
            # Fix torch loading issue with weights_only
            import torch.serialization
            
            # Temporarily allow unsafe loading for Bark models
            original_load = torch.load
            def safe_load(*args, **kwargs):
                kwargs['weights_only'] = False
                return original_load(*args, **kwargs)
            torch.load = safe_load
            
            try:
                # Preload models for faster generation
                preload_models()
                self.models_loaded = True
                
                self.logger.info("✅ Bark models loaded successfully")
                return True
                
            finally:
                # Restore original torch.load
                torch.load = original_load
            
        except Exception as e:
            self.logger.error(f"Failed to load Bark models: {e}")
            return False
    
    def generate_speech(self, 
                       text: str, 
                       output_path: str,
                       voice_preset: str = 'news_anchor_female',
                       add_emotion: bool = True,
                       speed_control: float = 1.0) -> bool:
        """
        Generate high-quality speech from text using Bark
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            voice_preset: Voice style to use
            add_emotion: Whether to add natural pauses and emotions
            speed_control: Speed multiplier (not directly supported by Bark)
            
        Returns:
            Success status
        """
        if not BARK_AVAILABLE:
            self.logger.error("Bark TTS not available")
            return False
            
        if not self.models_loaded:
            if not self.initialize():
                return False
        
        try:
            # Get voice preset
            speaker = self.voice_presets.get(voice_preset, self.voice_presets['news_anchor_female'])
            
            # Enhance text for better speech if emotion is enabled
            if add_emotion:
                text = self._enhance_text_for_speech(text)
            
            # Split long text into chunks (Bark works better with shorter texts)
            text_chunks = self._split_text_for_generation(text)
            
            audio_segments = []
            
            for i, chunk in enumerate(text_chunks):
                self.logger.info(f"Generating speech for chunk {i+1}/{len(text_chunks)}")
                
                # Generate audio for this chunk
                audio_array = generate_audio(chunk, history_prompt=speaker)
                audio_segments.append(audio_array)
                
                # Add small pause between chunks
                if i < len(text_chunks) - 1:
                    pause = np.zeros(int(0.3 * self.sample_rate))  # 0.3 second pause
                    audio_segments.append(pause)
            
            # Concatenate all audio segments
            final_audio = np.concatenate(audio_segments)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save audio file
            write_wav(output_path, self.sample_rate, final_audio.astype(np.float32))
            
            self.logger.info(f"✅ Speech generated successfully: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to generate speech: {e}")
            return False
    
    def _enhance_text_for_speech(self, text: str) -> str:
        """
        Enhance text with natural pauses and speech patterns
        Bark supports special tokens for better speech
        """
        # Add pauses after sentences
        text = text.replace('. ', '. [pause] ')
        text = text.replace('! ', '! [pause] ')
        text = text.replace('? ', '? [pause] ')
        
        # Add emphasis for important words (you could make this smarter)
        import re
        
        # Emphasize numbers and proper nouns (basic approach)
        text = re.sub(r'\b(\d+)\b', r'[emphasis] \1 [/emphasis]', text)
        
        # Add breathing pauses for longer sentences
        sentences = text.split('. ')
        enhanced_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 100:  # Long sentence
                # Find a good place to add a breath pause (after commas)
                sentence = sentence.replace(', ', ', [breath] ')
            enhanced_sentences.append(sentence)
        
        return '. '.join(enhanced_sentences)
    
    def _split_text_for_generation(self, text: str, max_length: int = 200) -> List[str]:
        """
        Split text into chunks suitable for Bark generation
        Bark works better with shorter text segments
        """
        # Split by sentences first
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max_length, start a new chunk
            if len(current_chunk) + len(sentence) > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voice presets"""
        return list(self.voice_presets.keys())
    
    def get_voice_info(self) -> Dict:
        """Get information about voice capabilities"""
        return {
            'service': 'Bark TTS by Suno',
            'type': 'offline',
            'quality': 'high',
            'emotions': True,
            'languages': ['en'],  # Bark primarily supports English well
            'voices': self.get_available_voices(),
            'features': [
                'Natural speech with emotions',
                'No API key required',
                'Unlimited usage',
                'High quality audio',
                'Natural pauses and breathing'
            ]
        }
    
    def cleanup_temp_files(self):
        """Clean up any temporary files"""
        # Bark doesn't create temp files by default, but good to have this method
        pass

# Installation instructions for Bark
BARK_INSTALLATION_GUIDE = """
To install Bark TTS for unlimited, high-quality voice generation:

1. Install Bark:
   pip install git+https://github.com/suno-ai/bark.git

2. Install additional dependencies:
   pip install scipy

3. For GPU acceleration (recommended):
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

4. First run will download models (~2GB), so ensure good internet connection.

Features:
- Completely offline after initial model download
- Natural-sounding speech with emotions
- No API keys or rate limits
- Supports different voice styles
- Can add pauses, emphasis, and breathing sounds

Note: Requires decent hardware for good performance:
- Minimum: 8GB RAM, CPU generation
- Recommended: 16GB RAM, NVIDIA GPU with 4GB+ VRAM
"""
