"""
Simple Video Creator - Alternative to MoviePy
Creates attractive videos using PIL and FFmpeg directly
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import subprocess
import tempfile
from datetime import datetime
from typing import Dict, Optional, List

class SimpleVideoCreator:
    """Simple video creator without MoviePy dependencies"""
    
    def __init__(self):
        self.video_width = 1080
        self.video_height = 1920
        self.fps = 30
        self.duration = 30  # Default 30 seconds
        
    def create_attractive_video(self, article: Dict, audio_path: str, output_path: str) -> bool:
        """Create an attractive video from article data and audio"""
        try:
            print(f"🎬 Creating attractive video: {article.get('title', 'News')[:50]}...")
            
            # Create frames directory
            temp_dir = tempfile.mkdtemp()
            frames_dir = os.path.join(temp_dir, "frames")
            os.makedirs(frames_dir, exist_ok=True)
            
            # Get audio duration
            audio_duration = self._get_audio_duration(audio_path)
            if audio_duration:
                self.duration = min(audio_duration, 60)  # Max 60 seconds
            
            # Calculate total frames
            total_frames = int(self.duration * self.fps)
            
            # Generate frames
            for frame_num in range(total_frames):
                frame_path = os.path.join(frames_dir, f"frame_{frame_num:06d}.png")
                self._create_frame(article, frame_num, total_frames, frame_path)
                
                if frame_num % 300 == 0:  # Progress every 10 seconds
                    progress = (frame_num / total_frames) * 100
                    print(f"   📸 Generated frames: {progress:.1f}%")
            
            print("   🎵 Combining with audio...")
            
            # Combine frames with audio using FFmpeg
            success = self._combine_frames_audio(frames_dir, audio_path, output_path)
            
            # Cleanup
            import shutil
            shutil.rmtree(temp_dir)
            
            if success:
                print(f"✅ Attractive video created: {os.path.basename(output_path)}")
                return True
            else:
                print("❌ Failed to create video")
                return False
                
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            return False
    
    def _create_frame(self, article: Dict, frame_num: int, total_frames: int, output_path: str):
        """Create a single attractive frame"""
        # Create base image
        img = Image.new('RGB', (self.video_width, self.video_height), (25, 35, 45))
        draw = ImageDraw.Draw(img)
        
        # Add gradient background
        self._add_gradient_background(img, frame_num, total_frames)
        
        # Add title with attractive styling
        title = article.get('title', 'Breaking News')
        self._add_title_text(img, title, frame_num, total_frames)
        
        # Add source info
        country = article.get('country', 'GLOBAL')
        source = article.get('source', 'News')
        self._add_source_info(img, country, source)
        
        # Add script text (subtitle style)
        script = article.get('script', '')
        if script:
            self._add_script_text(img, script, frame_num, total_frames)
        
        # Add attractive visual elements
        self._add_visual_elements(img, frame_num, total_frames)
        
        # Save frame
        img.save(output_path, quality=95)
    
    def _add_gradient_background(self, img: Image.Image, frame_num: int, total_frames: int):
        """Add animated gradient background"""
        # Create gradient overlay
        gradient = Image.new('RGBA', (self.video_width, self.video_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        # Animation factor
        progress = frame_num / total_frames
        color_shift = int(20 * abs(0.5 - progress))
        
        # Create vertical gradient
        for y in range(self.video_height):
            alpha = int(100 * (1 - y / self.video_height))
            color = (30 + color_shift, 50 + color_shift, 80 + color_shift, alpha)
            draw.line([(0, y), (self.video_width, y)], fill=color)
        
        # Blend with base image
        img.paste(gradient, (0, 0), gradient)
    
    def _add_title_text(self, img: Image.Image, title: str, frame_num: int, total_frames: int):
        """Add animated title text"""
        draw = ImageDraw.Draw(img)
        
        # Animation: Slide in from right in first 2 seconds
        slide_frames = int(2 * self.fps)
        if frame_num < slide_frames:
            offset = int(200 * (1 - frame_num / slide_frames))
        else:
            offset = 0
        
        # Load font (fallback to default if not available)
        try:
            font = ImageFont.truetype("arial.ttf", 56)
            bold_font = ImageFont.truetype("arialbd.ttf", 56)
        except:
            font = ImageFont.load_default()
            bold_font = font
        
        # Wrap title text
        wrapped_title = self._wrap_text(title, 35)
        
        # Calculate position
        bbox = draw.multiline_textbbox((0, 0), wrapped_title, font=bold_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.video_width - text_width) // 2 + offset
        y = 180
        
        # Add shadow
        shadow_offset = 3
        draw.multiline_text((x + shadow_offset, y + shadow_offset), wrapped_title, 
                          fill=(0, 0, 0, 180), font=bold_font, align='center')
        
        # Add main text with outline
        draw.multiline_text((x, y), wrapped_title, fill=(255, 255, 255), 
                          font=bold_font, align='center')
    
    def _add_source_info(self, img: Image.Image, country: str, source: str):
        """Add source information"""
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        source_text = f"{country} • {source}"
        
        # Calculate position (top center)
        bbox = draw.textbbox((0, 0), source_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.video_width - text_width) // 2
        y = 80
        
        # Add background rectangle
        padding = 20
        rect_coords = [x - padding, y - 10, x + text_width + padding, y + 50]
        draw.rounded_rectangle(rect_coords, radius=15, fill=(0, 0, 0, 120))
        
        # Add text
        draw.text((x, y), source_text, fill=(200, 200, 200), font=font)
    
    def _add_script_text(self, img: Image.Image, script: str, frame_num: int, total_frames: int):
        """Add script text as subtitles"""
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Typewriter effect: reveal text gradually
        chars_per_second = 8
        chars_to_show = int((frame_num / self.fps) * chars_per_second)
        visible_script = script[:chars_to_show]
        
        # Wrap text
        wrapped_script = self._wrap_text(visible_script, 50)
        
        # Calculate position (bottom area)
        bbox = draw.multiline_textbbox((0, 0), wrapped_script, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.video_width - text_width) // 2
        y = self.video_height - text_height - 200
        
        # Add semi-transparent background
        padding = 30
        rect_coords = [x - padding, y - 20, x + text_width + padding, y + text_height + 20]
        draw.rounded_rectangle(rect_coords, radius=20, fill=(0, 0, 0, 150))
        
        # Add text with outline
        outline_offset = 2
        for dx in [-outline_offset, 0, outline_offset]:
            for dy in [-outline_offset, 0, outline_offset]:
                if dx != 0 or dy != 0:
                    draw.multiline_text((x + dx, y + dy), wrapped_script, 
                                      fill=(0, 0, 0), font=font, align='center')
        
        draw.multiline_text((x, y), wrapped_script, fill=(255, 255, 255), 
                          font=font, align='center')
    
    def _add_visual_elements(self, img: Image.Image, frame_num: int, total_frames: int):
        """Add attractive visual elements"""
        draw = ImageDraw.Draw(img)
        
        # Animated progress bar
        progress = frame_num / total_frames
        bar_width = int(400 * progress)
        bar_y = self.video_height - 100
        
        # Background bar
        draw.rounded_rectangle([340, bar_y, 740, bar_y + 6], radius=3, fill=(60, 60, 60))
        
        # Progress bar
        if bar_width > 0:
            draw.rounded_rectangle([340, bar_y, 340 + bar_width, bar_y + 6], 
                                 radius=3, fill=(0, 150, 255))
        
        # Add decorative elements
        # Corner accents
        accent_color = (0, 150, 255, 100)
        draw.polygon([(0, 0), (100, 0), (0, 100)], fill=accent_color)
        draw.polygon([(self.video_width, 0), (self.video_width - 100, 0), 
                     (self.video_width, 100)], fill=accent_color)
    
    def _wrap_text(self, text: str, width: int) -> str:
        """Wrap text to specified width"""
        import textwrap
        lines = textwrap.wrap(text, width=width)
        return '\n'.join(lines)
    
    def _get_audio_duration(self, audio_path: str) -> Optional[float]:
        """Get audio duration using FFmpeg"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                '-show_format', audio_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return float(data['format']['duration'])
        except:
            pass
        return None
    
    def _combine_frames_audio(self, frames_dir: str, audio_path: str, output_path: str) -> bool:
        """Combine frames with audio using FFmpeg"""
        try:
            # Create video from frames
            temp_video = os.path.join(os.path.dirname(output_path), "temp_video.mp4")
            
            # FFmpeg command to create video from frames
            frames_pattern = os.path.join(frames_dir, "frame_%06d.png")
            
            cmd = [
                'ffmpeg', '-y',  # Overwrite output
                '-framerate', str(self.fps),
                '-i', frames_pattern,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-pix_fmt', 'yuv420p',
                '-crf', '18',  # High quality
                '-preset', 'medium',
                '-shortest',  # Match shortest stream
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                print(f"FFmpeg error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error combining frames: {e}")
            return False

def create_sample_attractive_video():
    """Create a sample attractive video to demonstrate capabilities"""
    creator = SimpleVideoCreator()
    
    # Sample article data
    sample_article = {
        'title': 'Revolutionary AI System Transforms Healthcare Diagnosis with 95% Accuracy Rate',
        'script': 'Scientists have developed a groundbreaking artificial intelligence system that can diagnose complex medical conditions with unprecedented accuracy. This breakthrough promises to revolutionize healthcare delivery worldwide.',
        'country': 'US',
        'source': 'Tech News Today',
        'category': 'technology'
    }
    
    # Check if we have sample audio
    audio_files = []
    for root, dirs, files in os.walk('reels'):
        for file in files:
            if file.endswith('.mp3'):
                audio_files.append(os.path.join(root, file))
    
    if not audio_files:
        print("❌ No audio files found. Please run audio generation first.")
        return False
    
    audio_path = audio_files[0]
    output_path = f"reels/attractive_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    
    print("🎨 Creating attractive video sample...")
    success = creator.create_attractive_video(sample_article, audio_path, output_path)
    
    if success:
        print(f"✅ Sample attractive video created: {output_path}")
        print("🎯 This demonstrates improved video quality with:")
        print("   • Animated gradient backgrounds")
        print("   • Smooth text animations")
        print("   • Professional typography")
        print("   • Progress indicators")
        print("   • High-quality rendering")
        return True
    else:
        print("❌ Failed to create sample video")
        return False

if __name__ == "__main__":
    create_sample_attractive_video()
