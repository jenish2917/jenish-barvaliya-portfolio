"""
Simple Video Reel Generator with Audio
Creates video reels by combining background, avatar, and audio using FFmpeg/OpenCV
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.enhanced_funny_content_processor import EnhancedFunnyContentProcessor
from src.services.enhanced_emotional_audio_service_fixed import EnhancedEmotionalAudioService
from src.services.emotional_voice_system import VoiceEmotion
import requests
import json
from datetime import datetime
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import subprocess
import tempfile
import shutil

class SimpleVideoReelGenerator:
    def __init__(self):
        self.content_processor = EnhancedFunnyContentProcessor()
        self.audio_service = EnhancedEmotionalAudioService()
        
        # Avatar configurations for different emotions
        self.avatar_configs = {
            'excited': {
                'expression': 'big_smile',
                'color': (255, 140, 0)  # Orange
            },
            'surprised': {
                'expression': 'wide_eyes',
                'color': (0, 191, 255)  # Blue
            },
            'confident': {
                'expression': 'knowing_smile',
                'color': (25, 25, 112)  # Dark blue
            },
            'dramatic': {
                'expression': 'serious',
                'color': (75, 0, 130)  # Purple
            },
            'playful': {
                'expression': 'cheeky_grin',
                'color': (255, 20, 147)  # Pink
            }
        }

    def get_todays_news_simple(self):
        """Get simplified news for testing"""
        return [
            {
                'title': 'AI Breakthrough: New Model Achieves Human-Level Reasoning',
                'content': 'Researchers unveiled an AI system that demonstrates unprecedented reasoning abilities, solving complex problems that previously required human intelligence. The system shows remarkable performance across multiple domains including mathematics, science, and creative tasks.',
                'category': 'technology',
                'source': 'TechNews',
                'time': '1 hour ago',
                'importance': 'high'
            },
            {
                'title': 'Space Discovery: Water Found on Mars Surface',
                'content': 'NASA scientists have confirmed liquid water flowing on the surface of Mars, dramatically increasing the possibility of finding life on the red planet. The discovery was made using advanced spectral analysis from the latest Mars rover mission.',
                'category': 'science',
                'source': 'Space Today',
                'time': '2 hours ago',
                'importance': 'high'
            },
            {
                'title': 'Market Surge: Tech Stocks Hit Record Highs',
                'content': 'Technology stocks reached unprecedented levels today as investors showed strong confidence in AI and renewable energy sectors. The NASDAQ gained 3.5% with several tech giants posting remarkable quarterly earnings.',
                'category': 'business',
                'source': 'Financial Times',
                'time': '30 minutes ago',
                'importance': 'medium'
            }
        ]

    def analyze_emotion(self, title, content):
        """Simple emotion analysis"""
        text = (title + " " + content).lower()
        
        if any(word in text for word in ['breakthrough', 'amazing', 'record', 'unprecedented']):
            return VoiceEmotion.EXCITED
        elif any(word in text for word in ['discovered', 'found', 'reveals']):
            return VoiceEmotion.SURPRISED
        elif any(word in text for word in ['surge', 'gains', 'confidence', 'strong']):
            return VoiceEmotion.CONFIDENT
        elif any(word in text for word in ['crisis', 'concern', 'warning']):
            return VoiceEmotion.CONCERNED
        else:
            return VoiceEmotion.EXCITED

    def create_simple_background(self, category, emotion, title, width=1080, height=1920):
        """Create simple background with gradient and text"""
        
        # Color schemes based on emotion
        colors = {
            'excited': [(255, 140, 0), (255, 69, 0)],
            'surprised': [(0, 191, 255), (30, 144, 255)],
            'confident': [(25, 25, 112), (72, 61, 139)],
            'dramatic': [(75, 0, 130), (138, 43, 226)],
            'playful': [(255, 20, 147), (255, 105, 180)]
        }
        
        color_pair = colors.get(emotion.value, colors['excited'])
        
        # Create gradient background
        img = Image.new('RGB', (width, height), color_pair[0])
        draw = ImageDraw.Draw(img)
        
        # Create gradient
        for y in range(height):
            ratio = y / height
            r = int(color_pair[0][0] + (color_pair[1][0] - color_pair[0][0]) * ratio)
            g = int(color_pair[0][1] + (color_pair[1][1] - color_pair[0][1]) * ratio)
            b = int(color_pair[0][2] + (color_pair[1][2] - color_pair[0][2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add title text
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Wrap title text
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), line_text, font=font)
            if bbox[2] > width - 100:
                if len(current_line) > 1:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw text with shadow
        start_y = 150
        for i, line in enumerate(lines[:3]):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 80
            
            # Shadow
            draw.text((x+3, y+3), line, font=font, fill=(0, 0, 0, 128))
            # Main text
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        return img

    def create_simple_avatar(self, emotion, width=200, height=300):
        """Create simple avatar"""
        config = self.avatar_configs.get(emotion.value, self.avatar_configs['excited'])
        color = config['color']
        
        # Create avatar image
        avatar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(avatar)
        
        center_x, center_y = width // 2, height // 2
        
        # Head
        head_radius = 60
        draw.ellipse([center_x - head_radius, center_y - 80 - head_radius, 
                     center_x + head_radius, center_y - 80 + head_radius], 
                    fill=(255, 220, 177), outline=color, width=3)
        
        # Eyes and mouth based on emotion
        if config['expression'] == 'big_smile':
            # Happy eyes (crescents)
            draw.arc([center_x - 25, center_y - 100, center_x - 5, center_y - 80], 0, 180, fill=(0, 0, 0), width=3)
            draw.arc([center_x + 5, center_y - 100, center_x + 25, center_y - 80], 0, 180, fill=(0, 0, 0), width=3)
            # Big smile
            draw.arc([center_x - 20, center_y - 70, center_x + 20, center_y - 50], 0, 180, fill=(0, 0, 0), width=4)
        elif config['expression'] == 'wide_eyes':
            # Surprised eyes
            draw.ellipse([center_x - 25, center_y - 100, center_x - 5, center_y - 80], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
            draw.ellipse([center_x + 5, center_y - 100, center_x + 25, center_y - 80], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
            draw.ellipse([center_x - 20, center_y - 95, center_x - 10, center_y - 85], fill=(0, 0, 0))
            draw.ellipse([center_x + 10, center_y - 95, center_x + 20, center_y - 85], fill=(0, 0, 0))
            # Open mouth
            draw.ellipse([center_x - 10, center_y - 70, center_x + 10, center_y - 50], fill=(0, 0, 0))
        else:
            # Normal eyes
            draw.ellipse([center_x - 20, center_y - 95, center_x - 10, center_y - 85], fill=(0, 0, 0))
            draw.ellipse([center_x + 10, center_y - 95, center_x + 20, center_y - 85], fill=(0, 0, 0))
            # Normal mouth
            draw.arc([center_x - 15, center_y - 70, center_x + 15, center_y - 60], 0, 180, fill=(0, 0, 0), width=3)
        
        # Body
        draw.rectangle([center_x - 40, center_y - 20, center_x + 40, center_y + 100], 
                      fill=color, outline=(0, 0, 0), width=2)
        
        # Arms
        draw.line([center_x - 40, center_y, center_x - 70, center_y + 50], fill=(255, 220, 177), width=6)
        draw.line([center_x + 40, center_y, center_x + 70, center_y + 50], fill=(255, 220, 177), width=6)
        
        return avatar

    def create_video_with_ffmpeg(self, background_path, audio_path, output_path, duration):
        """Create video using FFmpeg"""
        try:
            print(f"🎬 Creating video with FFmpeg...")
            print(f"   Background: {background_path}")
            print(f"   Audio: {audio_path}")
            print(f"   Output: {output_path}")
            print(f"   Duration: {duration:.1f}s")
            
            # FFmpeg command to create video from image and audio
            cmd = [
                'ffmpeg', '-y',  # Overwrite output file
                '-loop', '1',  # Loop the image
                '-i', background_path,  # Input image
                '-i', audio_path,  # Input audio
                '-c:v', 'libx264',  # Video codec
                '-tune', 'stillimage',  # Optimize for still image
                '-c:a', 'aac',  # Audio codec
                '-b:a', '192k',  # Audio bitrate
                '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
                '-shortest',  # End when shortest input ends
                '-vf', 'scale=1080:1920',  # Scale to 1080x1920
                output_path
            ]
            
            # Run FFmpeg
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=60)  # 60 second timeout
            
            if result.returncode == 0:
                print(f"✅ FFmpeg success: {output_path}")
                return True
            else:
                print(f"❌ FFmpeg failed:")
                print(f"   Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ FFmpeg timeout after 60 seconds")
            return False
        except FileNotFoundError:
            print(f"❌ FFmpeg not found in PATH")
            return False
        except Exception as e:
            print(f"❌ FFmpeg error: {e}")
            return False

    def create_simple_reel(self, article, index, total):
        """Create a simple video reel with audio"""
        try:
            print(f"\n🎬 Creating reel {index}/{total}: {article['title'][:50]}...")
            
            # Analyze emotion
            emotion = self.analyze_emotion(article['title'], article['content'])
            print(f"🎭 Detected emotion: {emotion.value}")
            
            # Process content for audio
            processed = self.content_processor.process_article(
                article['title'],
                article['content'],
                'US',
                article['category']
            )
            
            if not processed:
                print(f"❌ Content processing failed")
                return None
            
            print(f"📝 Content processed: {len(processed.script)} characters")
            
            # Generate audio
            audio_path, metrics = self.audio_service.generate_emotional_voiceover(
                processed.script,
                article['title'],
                article['category'],
                emotion
            )
            
            if not audio_path:
                print(f"❌ Audio generation failed")
                return None
            
            print(f"🎵 Audio generated: {audio_path}")
            print(f"⏱️ Duration: {metrics.duration:.1f}s")
            
            # Create visuals
            background = self.create_simple_background(
                article['category'], emotion, article['title']
            )
            
            avatar = self.create_simple_avatar(emotion)
            
            # Position avatar on background
            bg_width, bg_height = background.size
            avatar_x = bg_width - avatar.width - 50
            avatar_y = bg_height // 2 - avatar.height // 2
            
            # Composite avatar onto background
            final_frame = background.copy()
            final_frame.paste(avatar, (avatar_x, avatar_y), avatar)
            
            print(f"🎨 Visuals created with avatar")
            
            # Save frame temporarily
            session_dir = os.path.dirname(os.path.dirname(audio_path))
            video_dir = os.path.join(session_dir, 'videos')
            os.makedirs(video_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in article['title'] if c.isalnum() or c in (' ', '-', '_'))[:30]
            safe_title = safe_title.replace(' ', '_')
            
            temp_frame_path = os.path.join(video_dir, f"frame_{safe_title}_{timestamp}.png")
            final_frame.save(temp_frame_path)
            
            # Create video
            video_filename = f"reel_{safe_title}_{timestamp}.mp4"
            video_path = os.path.join(video_dir, video_filename)
            
            # Try FFmpeg first
            if self.create_video_with_ffmpeg(temp_frame_path, audio_path, video_path, metrics.duration):
                # Clean up temp frame
                try:
                    os.remove(temp_frame_path)
                except:
                    pass
                
                print(f"✅ Video reel created successfully!")
                
                return {
                    'index': index,
                    'title': article['title'],
                    'category': article['category'],
                    'emotion': emotion.value,
                    'audio_path': audio_path,
                    'video_path': video_path,
                    'duration': metrics.duration,
                    'engagement': processed.engagement_score,
                    'file_size': os.path.getsize(video_path) if os.path.exists(video_path) else 0
                }
            else:
                print(f"❌ Video creation failed")
                # Clean up temp frame
                try:
                    os.remove(temp_frame_path)
                except:
                    pass
                return None
                
        except Exception as e:
            print(f"❌ Error creating reel {index}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_all_reels(self):
        """Create all video reels"""
        print("🎬 SIMPLE VIDEO REEL GENERATOR")
        print("=" * 50)
        
        news_articles = self.get_todays_news_simple()
        print(f"📊 Processing {len(news_articles)} articles")
        
        successful_reels = []
        
        for i, article in enumerate(news_articles):
            result = self.create_simple_reel(article, i+1, len(news_articles))
            if result:
                successful_reels.append(result)
                print(f"✅ Reel {i+1} completed successfully")
            else:
                print(f"❌ Reel {i+1} failed")
        
        # Summary
        print(f"\n🎯 RESULTS:")
        print(f"✅ Successful: {len(successful_reels)}")
        print(f"❌ Failed: {len(news_articles) - len(successful_reels)}")
        print(f"📈 Success rate: {len(successful_reels)/len(news_articles)*100:.1f}%")
        
        if successful_reels:
            total_duration = sum(r['duration'] for r in successful_reels)
            total_size = sum(r['file_size'] for r in successful_reels)
            
            print(f"\n📊 STATISTICS:")
            print(f"⏱️ Total duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
            print(f"💾 Total size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
            
            print(f"\n📁 Videos saved to:")
            sample_path = os.path.dirname(successful_reels[0]['video_path'])
            print(f"   {os.path.abspath(sample_path)}")
        
        return successful_reels

def main():
    generator = SimpleVideoReelGenerator()
    reels = generator.create_all_reels()
    
    if reels:
        print(f"\n🚀 SUCCESS! {len(reels)} video reels with audio created!")
        print("🎥 Ready for social media sharing!")

if __name__ == "__main__":
    main()
