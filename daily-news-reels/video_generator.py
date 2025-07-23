"""
Enhanced Video Generator for News Reels
Creates engaging videos with emotional audio, dynamic visuals, and news content
"""

import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from moviepy.video.fx import resize, fadeout, fadein
from PIL import Image, ImageDraw, ImageFont
import logging
import random
from datetime import datetime

class VideoGenerator:
    def __init__(self):
        self.setup_logging()
        self.setup_video_config()
        
    def setup_logging(self):
        """Setup logging for video generation"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - VideoGenerator - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_video_config(self):
        """Setup video configuration"""
        self.config = {
            'resolution': (1080, 1920),  # Vertical format for TikTok/Instagram
            'fps': 30,
            'background_colors': {
                'technology': '#1e3a8a',     # Deep blue
                'science': '#059669',        # Green
                'business': '#dc2626',       # Red
                'world': '#7c3aed',         # Purple
                'entertainment': '#f59e0b',  # Orange
                'sports': '#16a34a',        # Sport green
                'health': '#ec4899'         # Pink
            },
            'text_animations': ['slide_in', 'fade_in', 'zoom_in', 'bounce'],
            'emotion_effects': {
                'excited': {'color': '#ff6b6b', 'speed': 1.2},
                'surprised': {'color': '#4ecdc4', 'speed': 1.0},
                'concerned': {'color': '#f7ca18', 'speed': 0.8},
                'confident': {'color': '#3498db', 'speed': 1.0},
                'playful': {'color': '#e74c3c', 'speed': 1.3},
                'dramatic': {'color': '#9b59b6', 'speed': 0.9},
                'sarcastic': {'color': '#34495e', 'speed': 1.1},
                'warm': {'color': '#f39c12', 'speed': 1.0}
            }
        }
        
    def create_news_video(self, title, script, audio_path, category='general', emotion='excited'):
        """Create a complete news video with emotional audio"""
        try:
            self.logger.info(f"Creating video for: {title[:30]}...")
            
            # Create output directory
            session_dir = os.path.dirname(os.path.dirname(audio_path))
            video_dir = os.path.join(session_dir, 'videos')
            os.makedirs(video_dir, exist_ok=True)
            
            # Generate video filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
            safe_title = safe_title.replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"emotional_video_{safe_title}_{timestamp}.mp4"
            video_path = os.path.join(video_dir, video_filename)
            
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # Create dynamic background
            background = self.create_dynamic_background(category, emotion, duration)
            
            # Create animated title
            title_clip = self.create_animated_title(title, category, emotion, duration)
            
            # Create news category badge
            category_badge = self.create_category_badge(category, duration)
            
            # Create emotion indicator
            emotion_indicator = self.create_emotion_indicator(emotion, duration)
            
            # Create scrolling script overlay
            script_overlay = self.create_script_overlay(script, duration)
            
            # Composite all elements
            final_video = CompositeVideoClip([
                background,
                title_clip,
                category_badge,
                emotion_indicator,
                script_overlay
            ], size=self.config['resolution'])
            
            # Add audio
            final_video = final_video.set_audio(audio_clip)
            
            # Apply emotion-based effects
            final_video = self.apply_emotion_effects(final_video, emotion)
            
            # Export video
            self.logger.info(f"Exporting video: {video_filename}")
            final_video.write_videofile(
                video_path,
                fps=self.config['fps'],
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Cleanup
            audio_clip.close()
            final_video.close()
            
            self.logger.info(f"✅ Video created successfully: {video_path}")
            return video_path
            
        except Exception as e:
            self.logger.error(f"Error creating video: {e}")
            return None
    
    def create_dynamic_background(self, category, emotion, duration):
        """Create an animated background based on category and emotion"""
        # Get category color
        bg_color = self.config['background_colors'].get(category, '#2c3e50')
        
        # Create gradient background
        def make_gradient_frame(t):
            # Create a gradient that shifts over time
            height, width = self.config['resolution'][1], self.config['resolution'][0]
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Convert hex color to RGB
            color_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
            
            # Create animated gradient
            shift = int(50 * np.sin(t * 0.5))
            for y in range(height):
                intensity = 0.3 + 0.4 * (y + shift) / height
                frame[y, :] = [int(c * intensity) for c in color_rgb]
            
            return frame
        
        background = VideoFileClip("dummy", duration=duration).fl(lambda gf, t: make_gradient_frame(t))
        return background.set_duration(duration)
    
    def create_animated_title(self, title, category, emotion, duration):
        """Create animated title text"""
        # Split title into multiple lines if too long
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 40:  # Adjust based on font size
                if len(current_line) > 1:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Create title clips for each line
        title_clips = []
        y_positions = [200, 300, 400]  # Positions for up to 3 lines
        
        for i, line in enumerate(lines[:3]):  # Max 3 lines
            title_clip = TextClip(
                line,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2
            ).set_position(('center', y_positions[i])).set_duration(duration)
            
            # Add entrance animation
            title_clip = title_clip.crossfadein(0.5)
            title_clips.append(title_clip)
        
        return CompositeVideoClip(title_clips)
    
    def create_category_badge(self, category, duration):
        """Create category badge"""
        badge = TextClip(
            category.upper(),
            fontsize=30,
            color='white',
            font='Arial-Bold',
            bg_color=self.config['background_colors'].get(category, '#2c3e50'),
            stroke_color='white',
            stroke_width=1
        ).set_position((50, 100)).set_duration(duration)
        
        return badge.crossfadein(0.3)
    
    def create_emotion_indicator(self, emotion, duration):
        """Create emotion indicator"""
        emotion_config = self.config['emotion_effects'].get(emotion, {'color': '#ffffff'})
        
        # Create emotion text with icon
        emotion_icons = {
            'excited': '🔥',
            'surprised': '😮',
            'concerned': '⚠️',
            'confident': '💪',
            'playful': '😄',
            'dramatic': '🎭',
            'sarcastic': '😏',
            'warm': '❤️'
        }
        
        icon = emotion_icons.get(emotion, '😊')
        emotion_text = f"{icon} {emotion.upper()}"
        
        indicator = TextClip(
            emotion_text,
            fontsize=25,
            color=emotion_config['color'],
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=1
        ).set_position((50, 1750)).set_duration(duration)
        
        return indicator.crossfadein(0.5)
    
    def create_script_overlay(self, script, duration):
        """Create scrolling script overlay"""
        # Clean and format script
        clean_script = script.replace('#', '').replace('*', '').strip()
        
        # Split into chunks for better readability
        words = clean_script.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(' '.join(current_chunk)) > 80:  # 80 chars per line
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Create scrolling text
        full_text = '\n'.join(chunks)
        
        script_clip = TextClip(
            full_text,
            fontsize=35,
            color='white',
            font='Arial',
            stroke_color='black',
            stroke_width=1,
            align='center',
            method='caption',
            size=(950, None)
        ).set_position(('center', 'bottom')).set_duration(duration)
        
        # Add fade effects
        script_clip = script_clip.crossfadein(1.0).crossfadeout(1.0)
        
        return script_clip
    
    def apply_emotion_effects(self, video, emotion):
        """Apply emotion-specific effects to video"""
        emotion_config = self.config['emotion_effects'].get(emotion, {'speed': 1.0})
        
        # Apply speed modification based on emotion
        speed = emotion_config['speed']
        if speed != 1.0:
            video = video.fx(lambda clip: clip.speedx(speed))
        
        # Add emotion-specific visual effects
        if emotion == 'excited':
            # Add slight zoom effect
            video = video.fx(resize, lambda t: 1 + 0.02 * np.sin(t * 2))
        elif emotion == 'dramatic':
            # Add fade effects
            video = video.crossfadein(0.5).crossfadeout(0.5)
        elif emotion == 'playful':
            # Add bounce effect
            video = video.set_position(lambda t: ('center', 'center' if int(t) % 2 == 0 else 'center'))
        
        return video
    
    def create_thumbnail(self, video_path, title, category, emotion):
        """Create an engaging thumbnail for the video"""
        try:
            # Extract frame from middle of video
            video = VideoFileClip(video_path)
            frame_time = video.duration / 2
            frame = video.get_frame(frame_time)
            
            # Convert to PIL Image
            image = Image.fromarray(frame)
            draw = ImageDraw.Draw(image)
            
            # Add title overlay
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Add semi-transparent overlay
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 128))
            image = Image.alpha_composite(image.convert('RGBA'), overlay)
            
            # Add title text
            draw = ImageDraw.Draw(image)
            draw.text((50, 50), title[:50], fill='white', font=font, stroke_width=2, stroke_fill='black')
            
            # Save thumbnail
            thumbnail_path = video_path.replace('.mp4', '_thumbnail.jpg')
            image.convert('RGB').save(thumbnail_path, 'JPEG')
            
            video.close()
            return thumbnail_path
            
        except Exception as e:
            self.logger.error(f"Error creating thumbnail: {e}")
            return None

# Test the video generator
if __name__ == "__main__":
    generator = VideoGenerator()
    print("🎬 Video Generator initialized successfully!")
    print("✅ Ready to create emotional news videos!")
