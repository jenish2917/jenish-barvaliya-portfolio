"""
Video Analysis Tool
Comprehensive analysis of video reels including background image, avatar quality, and speech quality
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import time
from datetime import datetime
from dataclasses import dataclass

# Video processing
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("⚠️ OpenCV not available. Video analysis will be limited.")

# Audio processing
try:
    import librosa
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️ Librosa not available. Audio analysis will be limited.")

# Image processing
try:
    from PIL import Image, ImageStat
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL not available. Image analysis will be limited.")

@dataclass
class VideoQualityMetrics:
    """Comprehensive video quality metrics"""
    resolution: Tuple[int, int]
    duration: float
    fps: float
    bitrate: float
    
    # Video quality metrics
    clarity_score: float
    brightness_score: float
    contrast_score: float
    stability_score: float
    
    # Background metrics
    bg_quality_score: float
    bg_relevance_score: float
    bg_brightness_score: float
    
    # Avatar metrics
    avatar_detection_score: float
    avatar_quality_score: float
    avatar_positioning_score: float
    
    # Audio metrics
    audio_clarity_score: float
    speech_quality_score: float
    volume_consistency_score: float
    noise_level_score: float
    
    # Overall scores
    overall_video_score: float
    overall_audio_score: float
    overall_quality_score: float
    
    # Recommendations
    recommendations: List[str]
    
    def to_dict(self) -> Dict:
        return {
            'technical': {
                'resolution': f"{self.resolution[0]}x{self.resolution[1]}",
                'duration': f"{self.duration:.2f} seconds",
                'fps': f"{self.fps:.2f}",
                'bitrate': f"{self.bitrate:.2f} Mbps"
            },
            'video_quality': {
                'clarity': self.clarity_score,
                'brightness': self.brightness_score,
                'contrast': self.contrast_score,
                'stability': self.stability_score,
                'overall': self.overall_video_score
            },
            'background': {
                'quality': self.bg_quality_score,
                'relevance': self.bg_relevance_score,
                'brightness': self.bg_brightness_score
            },
            'avatar': {
                'detection': self.avatar_detection_score,
                'quality': self.avatar_quality_score,
                'positioning': self.avatar_positioning_score
            },
            'audio': {
                'clarity': self.audio_clarity_score,
                'speech_quality': self.speech_quality_score,
                'volume_consistency': self.volume_consistency_score,
                'noise_level': self.noise_level_score,
                'overall': self.overall_audio_score
            },
            'overall_quality': self.overall_quality_score,
            'recommendations': self.recommendations
        }

class VideoAnalyzer:
    """Comprehensive video analyzer for news reels"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.min_resolution = (720, 1280)  # Vertical video minimum resolution
        self.required_modules = self._check_required_modules()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for video analyzer"""
        logger = logging.getLogger('VideoAnalyzer')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _check_required_modules(self) -> Dict[str, bool]:
        """Check if required modules are available"""
        return {
            'opencv': OPENCV_AVAILABLE,
            'librosa': LIBROSA_AVAILABLE,
            'pil': PIL_AVAILABLE
        }
        
    def analyze_video(self, video_path: str) -> Optional[VideoQualityMetrics]:
        """
        Perform comprehensive analysis of a video including:
        - Technical quality (resolution, fps, bitrate)
        - Background image quality
        - Avatar detection and quality
        - Voice/speech quality
        
        Args:
            video_path: Path to the video file
            
        Returns:
            VideoQualityMetrics object with analysis results
        """
        if not os.path.exists(video_path):
            self.logger.error(f"Video file not found: {video_path}")
            return None
            
        if not self.required_modules['opencv']:
            self.logger.error("OpenCV is required for video analysis")
            return None
            
        try:
            self.logger.info(f"Analyzing video: {video_path}")
            video = cv2.VideoCapture(video_path)
            
            if not video.isOpened():
                self.logger.error("Error opening video file")
                return None
                
            # Get basic video properties
            fps = video.get(cv2.CAP_PROP_FPS)
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Calculate video bitrate
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
            bitrate = (file_size * 8) / duration if duration > 0 else 0  # Mbps
            
            # Initialize metrics
            frames_for_analysis = min(100, frame_count)  # Analyze up to 100 frames
            frame_interval = max(1, frame_count // frames_for_analysis)
            
            # Metrics accumulators
            brightness_values = []
            contrast_values = []
            clarity_values = []
            faces_detected = 0
            face_sizes = []
            
            # Extract frames for analysis
            self.logger.info(f"Extracting {frames_for_analysis} frames for analysis")
            analyzed_frames = 0
            
            # Sample frames for analysis
            for i in range(0, frame_count, frame_interval):
                if analyzed_frames >= frames_for_analysis:
                    break
                    
                video.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = video.read()
                
                if not ret:
                    continue
                    
                # Calculate brightness (0-255)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                brightness = hsv[:, :, 2].mean()
                brightness_values.append(brightness)
                
                # Calculate contrast (standard deviation of brightness)
                contrast = hsv[:, :, 2].std()
                contrast_values.append(contrast)
                
                # Calculate clarity using Laplacian variance
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                clarity_values.append(laplacian_var)
                
                # Detect faces for avatar analysis
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    faces_detected += 1
                    # Get face sizes
                    for (x, y, w, h) in faces:
                        face_size = w * h
                        face_sizes.append(face_size / (width * height))  # Normalized face size
                
                analyzed_frames += 1
            
            video.release()
            
            # Calculate metrics
            avg_brightness = sum(brightness_values) / len(brightness_values) if brightness_values else 0
            avg_contrast = sum(contrast_values) / len(contrast_values) if contrast_values else 0
            avg_clarity = sum(clarity_values) / len(clarity_values) if clarity_values else 0
            
            # Normalize scores to 0-100
            brightness_score = min(100, max(0, avg_brightness / 255 * 100))
            contrast_score = min(100, max(0, avg_contrast / 50 * 100))  # Assuming 50 is good contrast
            clarity_score = min(100, max(0, avg_clarity / 500 * 100))  # Scale Laplacian variance
            
            # Avatar detection score
            avatar_detection_ratio = faces_detected / frames_for_analysis if frames_for_analysis > 0 else 0
            avatar_detection_score = avatar_detection_ratio * 100
            
            # Avatar quality and positioning
            avatar_quality_score = 0
            avatar_positioning_score = 0
            
            if face_sizes:
                avg_face_size = sum(face_sizes) / len(face_sizes)
                # Ideal face size is between 5-15% of frame
                if 0.05 <= avg_face_size <= 0.15:
                    avatar_quality_score = 90
                elif 0.02 <= avg_face_size < 0.05 or 0.15 < avg_face_size <= 0.25:
                    avatar_quality_score = 70
                else:
                    avatar_quality_score = 50
                
                # For now, use a placeholder score for positioning
                avatar_positioning_score = 80
            
            # Analyze audio for speech quality
            audio_metrics = self._analyze_audio(video_path)
            
            # Background quality (placeholder scores)
            bg_quality_score = (brightness_score + contrast_score + clarity_score) / 3
            bg_relevance_score = 80  # Placeholder - would need content-based analysis
            bg_brightness_score = brightness_score
            
            # Calculate stability score based on frame differences
            stability_score = 80  # Placeholder - would analyze motion between frames
            
            # Calculate overall scores
            video_score = (clarity_score + brightness_score + contrast_score + stability_score) / 4
            
            if audio_metrics:
                audio_clarity = audio_metrics.get('clarity', 0)
                speech_quality = audio_metrics.get('speech_quality', 0)
                volume_consistency = audio_metrics.get('volume_consistency', 0)
                noise_level = audio_metrics.get('noise_level', 0)
                
                audio_score = (audio_clarity + speech_quality + volume_consistency + noise_level) / 4
            else:
                audio_clarity = 0
                speech_quality = 0
                volume_consistency = 0
                noise_level = 0
                audio_score = 0
            
            # Generate recommendations
            recommendations = []
            
            if width < self.min_resolution[1] or height < self.min_resolution[0]:
                recommendations.append(f"Increase video resolution (current: {width}x{height}, recommended: at least {self.min_resolution[1]}x{self.min_resolution[0]}).")
                
            if brightness_score < 60:
                recommendations.append("Increase video brightness for better visibility.")
                
            if contrast_score < 60:
                recommendations.append("Improve contrast for better text readability.")
                
            if clarity_score < 60:
                recommendations.append("Improve video clarity/sharpness.")
                
            if avatar_detection_score < 50:
                recommendations.append("Ensure avatar/person is clearly visible in the video.")
                
            if audio_score < 60 and audio_metrics:
                recommendations.append("Improve audio quality for better speech clarity.")
                
            # Overall quality score
            overall_score = (video_score * 0.6) + (audio_score * 0.4)
            
            # Create and return metrics object
            return VideoQualityMetrics(
                resolution=(width, height),
                duration=duration,
                fps=fps,
                bitrate=bitrate,
                clarity_score=clarity_score,
                brightness_score=brightness_score,
                contrast_score=contrast_score,
                stability_score=stability_score,
                bg_quality_score=bg_quality_score,
                bg_relevance_score=bg_relevance_score,
                bg_brightness_score=bg_brightness_score,
                avatar_detection_score=avatar_detection_score,
                avatar_quality_score=avatar_quality_score,
                avatar_positioning_score=avatar_positioning_score,
                audio_clarity_score=audio_clarity,
                speech_quality_score=speech_quality,
                volume_consistency_score=volume_consistency,
                noise_level_score=noise_level,
                overall_video_score=video_score,
                overall_audio_score=audio_score,
                overall_quality_score=overall_score,
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _analyze_audio(self, video_path: str) -> Optional[Dict]:
        """
        Analyze audio quality from video file
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary with audio quality metrics
        """
        if not self.required_modules['librosa']:
            self.logger.warning("Librosa not available, skipping detailed audio analysis")
            return None
            
        try:
            # Extract audio from video temporarily
            temp_audio = os.path.join(os.path.dirname(video_path), "temp_audio.wav")
            
            # Use FFmpeg to extract audio
            import subprocess
            cmd = [
                "ffmpeg", "-i", video_path, 
                "-vn", "-acodec", "pcm_s16le", 
                "-ar", "44100", "-ac", "2", 
                temp_audio, "-y"
            ]
            
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Load audio file
            y, sr = librosa.load(temp_audio, sr=None)
            
            # Calculate audio metrics
            # Volume levels
            rms = librosa.feature.rms(y=y)[0]
            avg_volume = np.mean(rms)
            volume_std = np.std(rms)
            volume_consistency = 100 - (volume_std / avg_volume * 100) if avg_volume > 0 else 0
            
            # Speech detection and clarity
            # Using zero-crossing rate as a simple speech measure
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            avg_zcr = np.mean(zcr)
            speech_quality = 100 - (avg_zcr * 1000)  # Lower ZCR often correlates with speech
            speech_quality = max(0, min(100, speech_quality))
            
            # Noise analysis
            noise_level = 100 - (np.percentile(rms, 10) / avg_volume * 100) if avg_volume > 0 else 0
            
            # Overall clarity score - combination of factors
            clarity_score = (volume_consistency + speech_quality + (100 - noise_level)) / 3
            
            # Clean up temp file
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
            
            return {
                'clarity': float(clarity_score),
                'speech_quality': float(speech_quality),
                'volume_consistency': float(volume_consistency),
                'noise_level': float(100 - noise_level),  # Invert for consistency
                'avg_volume': float(avg_volume),
                'zcr': float(avg_zcr)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing audio: {e}")
            import traceback
            traceback.print_exc()
            
            # Clean up temp file
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
                
            return None
    
    def generate_quality_report(self, video_path: str, output_dir: str = None) -> Optional[str]:
        """
        Generate a comprehensive quality report for a video
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save the report (default: same as video)
            
        Returns:
            Path to the generated report file
        """
        metrics = self.analyze_video(video_path)
        
        if not metrics:
            self.logger.error("Failed to analyze video")
            return None
            
        if not output_dir:
            output_dir = os.path.dirname(video_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        video_name = os.path.basename(video_path).split('.')[0]
        report_path = os.path.join(output_dir, f"{video_name}_quality_report.json")
        
            # Save report as JSON
        with open(report_path, 'w', encoding='utf-8') as f:
            # Convert NumPy values to Python native types
            metrics_dict = metrics.to_dict()
            # Convert any numpy values to native Python types
            json.dump(metrics_dict, f, indent=2, default=lambda o: float(o) if isinstance(o, (np.floating)) else int(o) if isinstance(o, (np.integer)) else o)
            
        self.logger.info(f"Quality report generated: {report_path}")
        
        return report_path
    
    def batch_analyze_videos(self, video_dir: str, output_dir: str = None) -> Dict[str, VideoQualityMetrics]:
        """
        Batch analyze multiple videos in a directory
        
        Args:
            video_dir: Directory containing videos
            output_dir: Directory to save reports
            
        Returns:
            Dictionary mapping video paths to their quality metrics
        """
        if not os.path.isdir(video_dir):
            self.logger.error(f"Video directory not found: {video_dir}")
            return {}
        
        if not output_dir:
            output_dir = os.path.join(video_dir, "quality_reports")
            
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all video files
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(list(Path(video_dir).glob(f"*{ext}")))
        
        if not video_files:
            self.logger.warning(f"No video files found in: {video_dir}")
            return {}
        
        self.logger.info(f"Analyzing {len(video_files)} videos...")
        
        # Process each video
        results = {}
        for video_path in video_files:
            video_path_str = str(video_path)
            self.logger.info(f"Analyzing: {os.path.basename(video_path_str)}")
            
            metrics = self.analyze_video(video_path_str)
            if metrics:
                results[video_path_str] = metrics
                
                # Generate report
                self.generate_quality_report(video_path_str, output_dir)
                
        # Generate summary report
        self._generate_summary_report(results, output_dir)
        
        return results
    
    def _generate_summary_report(self, results: Dict[str, VideoQualityMetrics], output_dir: str):
        """Generate a summary report of all analyzed videos"""
        if not results:
            return
            
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(results),
            'average_scores': {
                'overall_quality': float(sum(m.overall_quality_score for m in results.values()) / len(results)) if results else 0,
                'video_quality': float(sum(m.overall_video_score for m in results.values()) / len(results)) if results else 0,
                'audio_quality': float(sum(m.overall_audio_score for m in results.values()) / len(results)) if results else 0
            },
            'videos': {os.path.basename(k): v.to_dict() for k, v in results.items()}
        }
        
        # Save summary report
        summary_path = os.path.join(output_dir, f"quality_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            # Convert NumPy values to Python native types
            json.dump(summary, f, indent=2, default=lambda o: float(o) if isinstance(o, (np.floating)) else int(o) if isinstance(o, (np.integer)) else o)
            
        self.logger.info(f"Summary report generated: {summary_path}")
        return summary_path
