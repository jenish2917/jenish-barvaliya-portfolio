"""
Enhanced Video Service
High-quality video generation with advanced features and quality control
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass
import json
from datetime import datetime
from pathlib import Path
import re
import time

# Video processing
try:
    from moviepy.editor import *
    from moviepy.config import check_for_optional_dependencies
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    # Create dummy classes for type hints
    class VideoClip: pass
    class TextClip: pass
    class AudioFileClip: pass
    class ImageClip: pass
    class ColorClip: pass
    class CompositeVideoClip: pass

# Image processing
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    import numpy as np
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    import requests
    from io import BytesIO
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

load_dotenv('config.env')

@dataclass
class VideoMetrics:
    """Video quality and technical metrics"""
    duration: float
    resolution: Tuple[int, int]
    fps: int
    file_size: int
    bitrate: int
    aspect_ratio: str
    quality_score: float
    
    def to_dict(self) -> Dict:
        return {
            'duration': self.duration,
            'resolution': list(self.resolution),
            'fps': self.fps,
            'file_size': self.file_size,
            'bitrate': self.bitrate,
            'aspect_ratio': self.aspect_ratio,
            'quality_score': self.quality_score
        }

class EnhancedVideoService:
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Video settings from config
        self.video_width = int(os.getenv('VIDEO_WIDTH', '1080'))
        self.video_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
        self.fps = int(os.getenv('VIDEO_FPS', '30'))
        
        # Quality settings
        self.min_duration = float(os.getenv('VIDEO_DURATION_MIN', '30'))
        self.max_duration = float(os.getenv('VIDEO_DURATION_MAX', '60'))
        
        # Style settings
        self.background_color = (15, 25, 35)  # Dark blue
        self.text_color = 'white'
        self.accent_color = '#00D4FF'  # Bright blue
        
        self._validate_dependencies()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for video service"""
        logger = logging.getLogger('VideoService')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _validate_dependencies(self):
        """Validate required dependencies"""
        if not MOVIEPY_AVAILABLE:
            self.logger.error("MoviePy not available. Video generation will fail.")
        
        if not PIL_AVAILABLE:
            self.logger.warning("PIL not available. Image processing will be limited.")
        
        if not OPENCV_AVAILABLE:
            self.logger.warning("OpenCV not available. Advanced video analysis not possible.")
    
    def create_reel(self, 
                   article: Dict, 
                   output_dir: str,
                   style_options: Dict = None) -> Optional[Tuple[str, VideoMetrics]]:
        """
        Create a high-quality video reel from article data
        
        Args:
            article: Article data with content, script, audio path, etc.
            output_dir: Directory to save the video
            style_options: Optional styling configuration
            
        Returns:
            Tuple of (video_path, metrics) or None if failed
        """
        if not MOVIEPY_AVAILABLE:
            self.logger.error("MoviePy not available. Cannot create video.")
            return None
        
        try:
            # Extract article data
            title = article.get('title', 'News Update')
            script = article.get('script', '')
            audio_path = article.get('audio_path')
            country = article.get('country', 'GLOBAL')
            source = article.get('source', 'News')
            category = article.get('category', 'general')
            image_url = article.get('urlToImage', '')
            
            self.logger.info(f"🎬 Creating high-quality reel: {title[:50]}...")
            
            # Create output path
            safe_title = self._create_safe_filename(title)
            video_filename = f"{safe_title}.mp4"
            video_path = os.path.join(output_dir, video_filename)
            os.makedirs(output_dir, exist_ok=True)
            
            # Get audio duration
            duration = self._get_audio_duration(audio_path)
            if not duration:
                duration = 35  # Default duration
            
            # Create video components
            background_clip = self._create_advanced_background(duration, image_url, category)
            title_overlay = self._create_enhanced_title_overlay(title, duration, category)
            subtitle_overlay = self._create_dynamic_subtitle_overlay(script, duration)
            info_overlay = self._create_info_overlay(country, source, category, duration)
            branding_overlay = self._create_branding_overlay(duration)
            
            # Compose final video
            video_clips = [background_clip]
            
            if title_overlay:
                video_clips.append(title_overlay)
            if subtitle_overlay:
                video_clips.append(subtitle_overlay)
            if info_overlay:
                video_clips.append(info_overlay)
            if branding_overlay:
                video_clips.append(branding_overlay)
            
            # Create composite video
            final_video = CompositeVideoClip(video_clips, size=(self.video_width, self.video_height))
            
            # Add audio if available
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                final_video = final_video.set_audio(audio_clip)
            
            # Export video with high quality settings
            self.logger.info("🎥 Rendering high-quality video...")
            final_video.write_videofile(
                video_path,
                fps=self.fps,
                bitrate="8000k",  # High bitrate for quality
                audio_bitrate="192k",
                codec='libx264',
                preset='medium',  # Balance between speed and compression
                ffmpeg_params=[
                    '-crf', '18',  # High quality (lower = better quality)
                    '-pix_fmt', 'yuv420p'  # Compatibility
                ],
                verbose=False,
                logger=None
            )
            
            # Clean up clips
            final_video.close()
            if audio_path and os.path.exists(audio_path):
                audio_clip.close()
            
            # Analyze video metrics
            metrics = self._analyze_video_metrics(video_path, duration)
            
            # Validate quality
            if not self._validate_video_quality(metrics):
                self.logger.warning("Video failed quality validation")
                return None
            
            self.logger.info(f"✅ High-quality reel created: {os.path.basename(video_path)}")
            self.logger.info(f"Duration: {metrics.duration:.1f}s, Quality: {metrics.quality_score:.1f}%")
            
            return video_path, metrics
            
        except Exception as e:
            self.logger.error(f"Error creating video reel: {e}")
            return None
    
    def _get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Get audio duration safely"""
        try:
            if audio_path and os.path.exists(audio_path):
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration
                audio_clip.close()
                return duration
        except Exception as e:
            self.logger.warning(f"Could not get audio duration: {e}")
        return None
    
    def _create_advanced_background(self, duration: float, image_url: str, category: str) -> VideoClip:
        """Create an advanced background with animations and effects"""
        try:
            # Try to use article image as background
            if image_url and REQUESTS_AVAILABLE:
                bg_clip = self._create_image_background(image_url, duration)
                if bg_clip:
                    return bg_clip
            
            # Create gradient background based on category
            gradient_colors = self._get_category_colors(category)
            return self._create_gradient_background(duration, gradient_colors)
            
        except Exception as e:
            self.logger.warning(f"Error creating advanced background: {e}")
            return self._create_solid_background(duration)
    
    def _create_image_background(self, image_url: str, duration: float) -> Optional[VideoClip]:
        """Create background from article image"""
        try:
            if not REQUESTS_AVAILABLE or not PIL_AVAILABLE:
                return None
            
            # Download image
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Process image
            img = Image.open(BytesIO(response.content))
            
            # Resize and crop to fit video dimensions
            img = self._prepare_background_image(img)
            
            # Save temporary image
            temp_path = f"temp_bg_{int(time.time())}.jpg"
            img.save(temp_path, quality=85)
            
            # Create video clip
            img_clip = ImageClip(temp_path, duration=duration)
            img_clip = img_clip.resize((self.video_width, self.video_height))
            
            # Add subtle zoom effect
            img_clip = img_clip.resize(lambda t: 1 + 0.02 * t / duration)
            
            # Add overlay for text readability
            overlay = ColorClip(size=(self.video_width, self.video_height), 
                              color=(0, 0, 0), duration=duration).set_opacity(0.3)
            
            background = CompositeVideoClip([img_clip, overlay])
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return background
            
        except Exception as e:
            self.logger.warning(f"Could not create image background: {e}")
            return None
    
    def _prepare_background_image(self, img: Image.Image) -> Image.Image:
        """Prepare image for use as video background"""
        if not PIL_AVAILABLE:
            return img
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate crop dimensions for 9:16 aspect ratio
        img_width, img_height = img.size
        target_ratio = self.video_width / self.video_height
        img_ratio = img_width / img_height
        
        if img_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img_height))
        else:
            # Image is taller, crop height
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            img = img.crop((0, top, img_width, top + new_height))
        
        # Resize to video dimensions
        img = img.resize((self.video_width, self.video_height), Image.Resampling.LANCZOS)
        
        # Apply subtle blur for text readability
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    def _get_category_colors(self, category: str) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """Get gradient colors based on news category"""
        color_schemes = {
            'technology': ((20, 30, 60), (60, 100, 140)),     # Blue gradient
            'business': ((30, 60, 30), (60, 120, 60)),        # Green gradient
            'sports': ((60, 30, 30), (120, 60, 60)),          # Red gradient
            'entertainment': ((60, 30, 60), (120, 60, 120)), # Purple gradient
            'health': ((30, 60, 60), (60, 120, 120)),         # Teal gradient
            'science': ((40, 40, 60), (80, 80, 120)),         # Blue-gray gradient
            'general': ((25, 35, 45), (45, 65, 85))           # Default blue-gray
        }
        
        return color_schemes.get(category.lower(), color_schemes['general'])
    
    def _create_gradient_background(self, duration: float, colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]]) -> VideoClip:
        """Create animated gradient background"""
        try:
            if PIL_AVAILABLE:
                # Create gradient image
                img = Image.new('RGB', (self.video_width, self.video_height))
                draw = ImageDraw.Draw(img)
                
                # Create vertical gradient
                color1, color2 = colors
                for y in range(self.video_height):
                    ratio = y / self.video_height
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                    draw.line([(0, y), (self.video_width, y)], fill=(r, g, b))
                
                # Save temporary image
                temp_path = f"temp_gradient_{int(time.time())}.jpg"
                img.save(temp_path, quality=90)
                
                # Create video clip with subtle animation
                gradient_clip = ImageClip(temp_path, duration=duration)
                
                # Add subtle brightness animation
                def brightness_effect(get_frame, t):
                    frame = get_frame(t)
                    factor = 1 + 0.05 * np.sin(2 * np.pi * t / 10)  # 10-second cycle
                    return np.clip(frame * factor, 0, 255).astype(np.uint8)
                
                gradient_clip = gradient_clip.fl(brightness_effect)
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return gradient_clip
            else:
                return self._create_solid_background(duration)
                
        except Exception as e:
            self.logger.warning(f"Error creating gradient background: {e}")
            return self._create_solid_background(duration)
    
    def _create_solid_background(self, duration: float) -> VideoClip:
        """Create simple solid color background"""
        return ColorClip(size=(self.video_width, self.video_height), 
                        color=self.background_color, duration=duration)
    
    def _create_enhanced_title_overlay(self, title: str, duration: float, category: str) -> Optional[TextClip]:
        """Create enhanced title overlay with animations"""
        try:
            # Split long titles
            if len(title) > 60:
                title = self._wrap_title(title)
            
            # Category-specific styling
            font_size = self._get_title_font_size(len(title))
            font_color = self._get_category_accent_color(category)
            
            title_clip = TextClip(
                title,
                fontsize=font_size,
                color=font_color,
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2,
                method='caption',
                size=(self.video_width - 100, None),
                align='center'
            ).set_duration(duration)
            
            # Position at top
            title_clip = title_clip.set_position(('center', 150))
            
            # Add entrance animation
            title_clip = title_clip.crossfadein(0.5)
            
            # Add subtle scaling animation
            title_clip = title_clip.resize(lambda t: 1 + 0.02 * np.sin(np.pi * t))
            
            return title_clip
            
        except Exception as e:
            self.logger.warning(f"Error creating title overlay: {e}")
            return None
    
    def _get_title_font_size(self, title_length: int) -> int:
        """Get appropriate font size based on title length"""
        if title_length < 30:
            return 75
        elif title_length < 50:
            return 65
        elif title_length < 80:
            return 55
        else:
            return 45
    
    def _get_category_accent_color(self, category: str) -> str:
        """Get accent color for category"""
        colors = {
            'technology': '#00D4FF',
            'business': '#00FF88',
            'sports': '#FF4444',
            'entertainment': '#FF44FF',
            'health': '#44FFFF',
            'science': '#8888FF',
            'general': '#FFFFFF'
        }
        return colors.get(category.lower(), '#FFFFFF')
    
    def _wrap_title(self, title: str) -> str:
        """Intelligently wrap long titles"""
        words = title.split()
        if len(words) <= 2:
            return title
        
        mid_point = len(words) // 2
        first_half = ' '.join(words[:mid_point])
        second_half = ' '.join(words[mid_point:])
        
        return f"{first_half}\\n{second_half}"
    
    def _create_dynamic_subtitle_overlay(self, script: str, duration: float) -> Optional[CompositeVideoClip]:
        """Create dynamic subtitle overlay with word-by-word animation"""
        try:
            if not script:
                return None
            
            # Split script into sentences
            sentences = [s.strip() + '.' for s in script.split('.') if s.strip()]
            if not sentences:
                return None
            
            subtitle_clips = []
            words_per_second = len(script.split()) / duration
            
            current_time = 0
            for sentence in sentences:
                sentence_duration = len(sentence.split()) / words_per_second
                
                # Create subtitle clip
                subtitle_clip = TextClip(
                    sentence,
                    fontsize=45,
                    color='white',
                    font='Arial',
                    stroke_color='black',
                    stroke_width=1,
                    method='caption',
                    size=(self.video_width - 120, None),
                    align='center'
                ).set_duration(sentence_duration).set_start(current_time)
                
                # Position in lower third
                subtitle_clip = subtitle_clip.set_position(('center', self.video_height - 400))
                
                # Add fade effects
                subtitle_clip = subtitle_clip.crossfadein(0.3).crossfadeout(0.3)
                
                subtitle_clips.append(subtitle_clip)
                current_time += sentence_duration
            
            return CompositeVideoClip(subtitle_clips) if subtitle_clips else None
            
        except Exception as e:
            self.logger.warning(f"Error creating subtitle overlay: {e}")
            return None
    
    def _create_info_overlay(self, country: str, source: str, category: str, duration: float) -> Optional[CompositeVideoClip]:
        """Create information overlay with country, source, and category"""
        try:
            info_clips = []
            
            # Country badge
            country_clip = TextClip(
                f"📍 {country}",
                fontsize=35,
                color=self._get_category_accent_color(category),
                font='Arial-Bold'
            ).set_duration(duration).set_position((50, 50))
            
            info_clips.append(country_clip)
            
            # Category badge
            category_clip = TextClip(
                f"#{category.upper()}",
                fontsize=30,
                color='white',
                font='Arial'
            ).set_duration(duration).set_position((50, 100))
            
            info_clips.append(category_clip)
            
            # Source at bottom
            if source and source != 'Unknown':
                source_clip = TextClip(
                    f"Source: {source}",
                    fontsize=25,
                    color='lightgray',
                    font='Arial'
                ).set_duration(duration).set_position((50, self.video_height - 100))
                
                info_clips.append(source_clip)
            
            return CompositeVideoClip(info_clips) if info_clips else None
            
        except Exception as e:
            self.logger.warning(f"Error creating info overlay: {e}")
            return None
    
    def _create_branding_overlay(self, duration: float) -> Optional[TextClip]:
        """Create subtle branding overlay"""
        try:
            brand_clip = TextClip(
                "AI News Reels",
                fontsize=20,
                color='lightgray',
                font='Arial'
            ).set_duration(duration).set_position((self.video_width - 200, self.video_height - 50))
            
            brand_clip = brand_clip.set_opacity(0.7)
            
            return brand_clip
            
        except Exception as e:
            self.logger.warning(f"Error creating branding overlay: {e}")
            return None
    
    def _analyze_video_metrics(self, video_path: str, expected_duration: float) -> VideoMetrics:
        """Analyze video file metrics"""
        try:
            # Get file stats
            file_stats = os.stat(video_path)
            file_size = file_stats.st_size
            
            # Get video info using MoviePy
            if MOVIEPY_AVAILABLE:
                video_clip = VideoFileClip(video_path)
                actual_duration = video_clip.duration
                fps = video_clip.fps
                width, height = video_clip.size
                video_clip.close()
            else:
                actual_duration = expected_duration
                fps = self.fps
                width, height = self.video_width, self.video_height
            
            # Calculate bitrate
            bitrate = int((file_size * 8) / actual_duration) if actual_duration > 0 else 0
            
            # Determine aspect ratio
            aspect_ratio = f"{width}:{height}"
            if abs(width/height - 9/16) < 0.01:
                aspect_ratio = "9:16"
            elif abs(width/height - 16/9) < 0.01:
                aspect_ratio = "16:9"
            
            # Calculate quality score
            quality_score = self._calculate_video_quality_score(
                actual_duration, (width, height), fps, file_size, bitrate
            )
            
            return VideoMetrics(
                duration=round(actual_duration, 2),
                resolution=(width, height),
                fps=fps,
                file_size=file_size,
                bitrate=bitrate,
                aspect_ratio=aspect_ratio,
                quality_score=round(quality_score, 1)
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing video metrics: {e}")
            return self._default_video_metrics(expected_duration)
    
    def _calculate_video_quality_score(self, duration: float, resolution: Tuple[int, int], 
                                     fps: int, file_size: int, bitrate: int) -> float:
        """Calculate video quality score"""
        score = 0.0
        
        # Duration score (25%)
        if self.min_duration <= duration <= self.max_duration:
            score += 25
        elif duration < self.min_duration:
            score += 20 * (duration / self.min_duration)
        else:
            score += 20 * (self.max_duration / duration)
        
        # Resolution score (25%)
        width, height = resolution
        if width >= 1080 and height >= 1920:
            score += 25
        elif width >= 720 and height >= 1280:
            score += 20
        else:
            score += 15
        
        # FPS score (20%)
        if fps >= 30:
            score += 20
        elif fps >= 24:
            score += 15
        else:
            score += 10
        
        # File size score (15%) - indicates quality
        expected_size = duration * 1000000  # ~1MB per second for good quality
        size_ratio = file_size / expected_size if expected_size > 0 else 0
        if 0.8 <= size_ratio <= 2.0:
            score += 15
        elif 0.5 <= size_ratio < 0.8 or 2.0 < size_ratio <= 3.0:
            score += 10
        else:
            score += 5
        
        # Bitrate score (15%)
        if bitrate >= 5000000:  # 5 Mbps
            score += 15
        elif bitrate >= 2000000:  # 2 Mbps
            score += 12
        elif bitrate >= 1000000:  # 1 Mbps
            score += 8
        else:
            score += 5
        
        return min(score, 100.0)
    
    def _default_video_metrics(self, duration: float) -> VideoMetrics:
        """Return default metrics if analysis fails"""
        return VideoMetrics(
            duration=duration,
            resolution=(self.video_width, self.video_height),
            fps=self.fps,
            file_size=0,
            bitrate=0,
            aspect_ratio="9:16",
            quality_score=50.0
        )
    
    def _validate_video_quality(self, metrics: VideoMetrics) -> bool:
        """Validate if video meets minimum quality standards"""
        # Check duration
        if not (self.min_duration <= metrics.duration <= self.max_duration * 1.2):
            self.logger.warning(f"Video duration out of range: {metrics.duration}s")
            return False
        
        # Check quality score
        if metrics.quality_score < 60:
            self.logger.warning(f"Video quality too low: {metrics.quality_score}%")
            return False
        
        # Check file size (minimum 1MB)
        if metrics.file_size < 1024 * 1024:
            self.logger.warning(f"Video file too small: {metrics.file_size} bytes")
            return False
        
        return True
    
    def _create_safe_filename(self, title: str) -> str:
        """Create a safe filename from article title"""
        safe_title = re.sub(r'[^a-zA-Z0-9\s\-_]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title.strip())
        safe_title = safe_title[:50]  # Limit length
        
        if not safe_title:
            safe_title = f"video_{int(time.time())}"
        
        return safe_title
    
    def generate_batch_videos(self, articles_with_audio: List[Dict], output_dir: str, max_workers: int = 2) -> List[Dict]:
        """
        Generate videos for multiple articles in parallel (limited workers due to video processing)
        
        Args:
            articles_with_audio: List of articles with audio paths
            output_dir: Directory to save videos
            max_workers: Number of parallel workers (lower for video processing)
            
        Returns:
            List of articles with added 'video_path' and 'video_metrics' fields
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import threading
        
        os.makedirs(output_dir, exist_ok=True)
        successful_articles = []
        results_lock = threading.Lock()
        
        self.logger.info(f"🎬 Generating videos for {len(articles_with_audio)} articles in parallel with {max_workers} workers...")
        
        def generate_single_video(article_data):
            """Generate video for a single article (thread-safe)"""
            article, index = article_data
            try:
                title = article.get('title', f'Video_{index+1}')
                
                # Create video
                result = self.create_reel(article, output_dir)
                
                if result:
                    video_path, metrics = result
                    
                    # Add video info to article
                    article_copy = article.copy()
                    article_copy['video_path'] = video_path
                    article_copy['video_metrics'] = metrics.to_dict()
                    
                    return (index, article_copy, True)
                else:
                    self.logger.error(f"Failed to generate video for article {index+1}")
                    return (index, None, False)
                    
            except Exception as e:
                self.logger.error(f"Error generating video {index+1}: {e}")
                return (index, None, False)
        
        # Use ThreadPoolExecutor for parallel video generation (limited workers)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all articles for processing
            article_data = [(article, i) for i, article in enumerate(articles_with_audio)]
            future_to_article = {executor.submit(generate_single_video, data): data for data in article_data}
            
            # Collect results as they complete
            completed_count = 0
            for future in as_completed(future_to_article):
                completed_count += 1
                index, article_with_video, success = future.result()
                
                if success and article_with_video:
                    with results_lock:
                        successful_articles.append(article_with_video)
                
                # Log progress
                self.logger.info(f"🎥 Completed video {completed_count}/{len(articles_with_audio)}")
        
        self.logger.info(f"🎉 Successfully generated {len(successful_articles)}/{len(articles_with_audio)} videos in parallel")
        return successful_articles
    
    def save_video_report(self, articles_with_videos: List[Dict], output_dir: str) -> str:
        """Save video generation report"""
        os.makedirs(output_dir, exist_ok=True)
        
        report = {
            'generation_time': datetime.now().isoformat(),
            'total_videos': len(articles_with_videos),
            'total_duration': sum(article.get('video_metrics', {}).get('duration', 0) for article in articles_with_videos),
            'average_quality': sum(article.get('video_metrics', {}).get('quality_score', 0) for article in articles_with_videos) / len(articles_with_videos) if articles_with_videos else 0,
            'total_file_size': sum(article.get('video_metrics', {}).get('file_size', 0) for article in articles_with_videos),
            'videos': [{
                'title': article.get('title', ''),
                'video_path': article.get('video_path', ''),
                'metrics': article.get('video_metrics', {})
            } for article in articles_with_videos]
        }
        
        report_path = os.path.join(output_dir, f"video_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved video report to {report_path}")
        return report_path

# Legacy compatibility
class VideoGenerator(EnhancedVideoService):
    """Backward compatibility wrapper"""
    
    def create_reel(self, article: Dict, output_dir: str) -> str:
        """Legacy method signature"""
        result = super().create_reel(article, output_dir)
        return result[0] if result else None
