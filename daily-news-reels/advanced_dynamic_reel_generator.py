"""
Advanced Dynamic Avatar & Background System
- Lip-syncing avatars that move with audio
- Contextual background images matching article content
- Military, tech, science, business themed backgrounds
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.enhanced_funny_content_processor import EnhancedFunnyContentProcessor
from src.services.enhanced_emotional_audio_service_fixed import EnhancedEmotionalAudioService
from src.services.emotional_voice_system import VoiceEmotion
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import subprocess
import cv2
import numpy as np
from datetime import datetime
import random
import time
import requests
import json
import librosa
import wave

class AdvancedDynamicReelGenerator:
    def __init__(self):
        self.content_processor = EnhancedFunnyContentProcessor()
        self.audio_service = EnhancedEmotionalAudioService()
        
        # Contextual background themes
        self.background_themes = {
            'military': {
                'colors': [(20, 40, 20), (40, 60, 40), (60, 80, 60)],  # Military green
                'patterns': 'camouflage',
                'keywords': ['military', 'army', 'navy', 'air force', 'defense', 'war', 'soldier', 'combat', 'marine']
            },
            'technology': {
                'colors': [(10, 20, 40), (20, 40, 80), (30, 60, 120)],  # Tech blue
                'patterns': 'circuit_board',
                'keywords': ['tech', 'ai', 'robot', 'digital', 'software', 'app', 'computer', 'data', 'cyber']
            },
            'space': {
                'colors': [(5, 5, 20), (10, 10, 40), (15, 15, 60)],  # Space dark blue
                'patterns': 'stars',
                'keywords': ['nasa', 'space', 'mars', 'moon', 'satellite', 'astronaut', 'galaxy', 'universe', 'cosmos']
            },
            'medical': {
                'colors': [(20, 40, 50), (40, 80, 100), (60, 120, 150)],  # Medical blue
                'patterns': 'medical_cross',
                'keywords': ['health', 'medical', 'doctor', 'hospital', 'drug', 'disease', 'treatment', 'cure']
            },
            'business': {
                'colors': [(30, 20, 20), (60, 40, 40), (90, 60, 60)],  # Business burgundy
                'patterns': 'corporate',
                'keywords': ['business', 'finance', 'market', 'economy', 'bank', 'stock', 'investment', 'corporate']
            },
            'crypto': {
                'colors': [(40, 30, 10), (80, 60, 20), (120, 90, 30)],  # Crypto gold
                'patterns': 'blockchain',
                'keywords': ['bitcoin', 'crypto', 'blockchain', 'ethereum', 'currency', 'coin', 'mining']
            },
            'science': {
                'colors': [(10, 30, 10), (20, 60, 20), (30, 90, 30)],  # Science green
                'patterns': 'molecular',
                'keywords': ['science', 'research', 'discovery', 'study', 'experiment', 'laboratory', 'scientist']
            }
        }
    
    def detect_article_theme(self, title, summary):
        """Detect the theme of the article for contextual backgrounds"""
        content = (title + " " + summary).lower()
        
        theme_scores = {}
        for theme, data in self.background_themes.items():
            score = sum(1 for keyword in data['keywords'] if keyword in content)
            theme_scores[theme] = score
        
        # Get the theme with highest score
        detected_theme = max(theme_scores, key=theme_scores.get)
        
        # If no strong match, use content-based detection
        if theme_scores[detected_theme] == 0:
            if any(word in content for word in ['openai', 'gpt', 'ai', 'iphone', 'tesla']):
                return 'technology'
            elif any(word in content for word in ['nasa', 'space', 'europa', 'mars']):
                return 'space'
            elif any(word in content for word in ['alzheimer', 'drug', 'medical']):
                return 'medical'
            elif any(word in content for word in ['bitcoin', 'crypto']):
                return 'crypto'
            else:
                return 'business'
        
        return detected_theme

    def create_contextual_background(self, theme, title):
        """Create background image matching the article theme"""
        
        width, height = 1080, 1920
        theme_data = self.background_themes.get(theme, self.background_themes['technology'])
        colors = theme_data['colors']
        pattern = theme_data['patterns']
        
        # Create base gradient
        img = Image.new('RGB', (width, height), colors[0])
        
        # Create sophisticated gradient
        gradient_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for y in range(height):
            ratio = y / height
            if ratio < 0.4:
                blend = ratio / 0.4
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * blend)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * blend)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * blend)
            else:
                blend = (ratio - 0.4) / 0.6
                r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * blend)
                g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * blend)
                b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * blend)
            
            gradient_array[y, :] = [r, g, b]
        
        img = Image.fromarray(gradient_array)
        
        # Add theme-specific patterns
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        if pattern == 'camouflage':
            # Military camouflage pattern
            for _ in range(50):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(30, 80)
                overlay_draw.ellipse([x, y, x+size, y+size], fill=(40, 70, 40, 30))
        
        elif pattern == 'circuit_board':
            # Technology circuit patterns
            for i in range(0, width, 100):
                for j in range(0, height, 100):
                    overlay_draw.rectangle([i, j, i+80, j+2], fill=(0, 150, 255, 20))
                    overlay_draw.rectangle([i, j, i+2, j+80], fill=(0, 150, 255, 20))
                    overlay_draw.ellipse([i+35, j+35, i+45, j+45], fill=(0, 200, 255, 40))
        
        elif pattern == 'stars':
            # Space star field
            for _ in range(100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(1, 3)
                overlay_draw.ellipse([x, y, x+size, y+size], fill=(255, 255, 255, random.randint(50, 150)))
        
        elif pattern == 'medical_cross':
            # Medical crosses pattern
            for i in range(0, width, 200):
                for j in range(0, height, 200):
                    # Medical cross
                    overlay_draw.rectangle([i+90, j+70, i+110, j+130], fill=(255, 255, 255, 15))
                    overlay_draw.rectangle([i+70, j+90, i+130, j+110], fill=(255, 255, 255, 15))
        
        elif pattern == 'blockchain':
            # Crypto blockchain pattern
            for i in range(0, width, 150):
                for j in range(0, height, 150):
                    # Blockchain blocks
                    overlay_draw.rectangle([i+20, j+20, i+60, j+60], fill=(255, 215, 0, 25))
                    overlay_draw.line([(i+60, j+40), (i+90, j+40)], fill=(255, 215, 0, 30), width=2)
        
        elif pattern == 'molecular':
            # Science molecular structure
            for _ in range(30):
                x = random.randint(50, width-50)
                y = random.randint(50, height-50)
                overlay_draw.ellipse([x-5, y-5, x+5, y+5], fill=(0, 255, 100, 40))
                # Connect to nearby points
                for _ in range(2):
                    x2 = x + random.randint(-50, 50)
                    y2 = y + random.randint(-50, 50)
                    overlay_draw.line([(x, y), (x2, y2)], fill=(0, 255, 100, 20), width=1)
        
        else:  # corporate
            # Business corporate pattern
            for i in range(0, width, 120):
                for j in range(0, height, 120):
                    overlay_draw.rectangle([i, j, i+100, j+3], fill=(255, 255, 255, 15))
                    overlay_draw.rectangle([i, j, i+3, j+100], fill=(255, 255, 255, 15))
        
        # Blend overlay
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # Add professional title with theme styling
        try:
            font_large = ImageFont.truetype("arialbd.ttf", 55)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add contextual header
        text_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Theme-specific headers
        headers = {
            'military': "DEFENSE NEWS",
            'technology': "TECH BREAKING",
            'space': "SPACE UPDATE",
            'medical': "HEALTH NEWS", 
            'business': "MARKET NEWS",
            'crypto': "CRYPTO UPDATE",
            'science': "SCIENCE NEWS"
        }
        
        header_text = headers.get(theme, "BREAKING NEWS")
        
        # Header background
        header_bbox = text_draw.textbbox((0, 0), header_text, font=font_small)
        header_width = header_bbox[2] - header_bbox[0]
        header_x = (width - header_width) // 2
        
        # Theme-specific header colors
        header_colors = {
            'military': (60, 80, 40),
            'technology': (20, 60, 120),
            'space': (20, 20, 80),
            'medical': (40, 100, 140),
            'business': (100, 60, 60),
            'crypto': (120, 90, 30),
            'science': (30, 120, 30)
        }
        
        header_color = header_colors.get(theme, (80, 80, 80))
        
        text_draw.rectangle([header_x - 20, 20, header_x + header_width + 20, 60], 
                          fill=header_color + (200,))
        text_draw.text((header_x, 30), header_text, font=font_small, fill=(255, 255, 255, 255))
        
        # Main title with better formatting
        clean_title = title.replace('-', ' ').replace('_', ' ')
        words = clean_title.split()[:8]
        title_text = ' '.join(words).title()
        
        # Multi-line title
        max_chars_per_line = 20
        if len(title_text) > max_chars_per_line:
            words = title_text.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + " " + word) <= max_chars_per_line:
                    current_line += " " + word if current_line else word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
        else:
            lines = [title_text]
        
        # Draw title lines
        start_y = 120
        line_height = 60
        
        for i, line in enumerate(lines[:3]):
            bbox = text_draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + (i * line_height)
            
            # Professional shadow
            text_draw.text((x+3, y+3), line, font=font_large, fill=(0, 0, 0, 120))
            text_draw.text((x, y), line, font=font_large, fill=(255, 255, 255, 255))
        
        # Add timestamp and theme indicator
        timestamp = datetime.now().strftime("%B %d, %Y")
        theme_label = f"{theme.upper()} • {timestamp}"
        
        time_bbox = text_draw.textbbox((0, 0), theme_label, font=font_small)
        time_width = time_bbox[2] - time_bbox[0]
        time_x = (width - time_width) // 2
        text_draw.text((time_x, height - 60), theme_label, font=font_small, fill=(255, 255, 255, 180))
        
        # Composite text
        img = Image.alpha_composite(img.convert('RGBA'), text_img).convert('RGB')
        
        return img

    def analyze_audio_for_lipsyncing(self, audio_file):
        """Analyze audio to extract timing for lip-sync animation"""
        
        try:
            # Load audio using librosa
            y, sr = librosa.load(audio_file)
            
            # Extract amplitude envelope for mouth movement
            hop_length = 512
            frame_length = 2048
            
            # RMS energy for volume-based mouth movement
            rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
            
            # Convert to time stamps
            times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
            
            # Normalize RMS values for mouth opening (0-1)
            rms_normalized = (rms - rms.min()) / (rms.max() - rms.min() + 1e-8)
            
            # Detect speech segments for more accurate lip-sync
            speech_segments = []
            threshold = 0.02
            
            for i, amplitude in enumerate(rms_normalized):
                if amplitude > threshold:
                    mouth_opening = min(amplitude * 1.5, 1.0)  # Scale for mouth movement
                    speech_segments.append({
                        'time': times[i],
                        'mouth_opening': mouth_opening,
                        'talking': True
                    })
                else:
                    speech_segments.append({
                        'time': times[i],
                        'mouth_opening': 0.1,  # Slight opening when not talking
                        'talking': False
                    })
            
            return speech_segments
            
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            # Fallback: simple periodic mouth movement
            duration = 30  # Default duration
            segments = []
            for i in range(0, int(duration * 10)):  # 10 FPS
                time_pos = i / 10.0
                mouth_opening = 0.3 + 0.4 * abs(np.sin(time_pos * 4))  # Sine wave movement
                segments.append({
                    'time': time_pos,
                    'mouth_opening': mouth_opening,
                    'talking': True
                })
            return segments

    def create_lipsyncing_avatar(self, emotion, mouth_opening=0.3):
        """Create avatar with dynamic mouth movement"""
        
        width, height = 300, 400
        avatar_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(avatar_img)
        
        center_x, center_y = width // 2, height // 2
        
        # Professional avatar colors
        skin_color = (255, 220, 177)
        suit_color = (30, 30, 60)
        
        # Head
        head_radius = 60
        draw.ellipse([center_x - head_radius, center_y - 80 - head_radius, 
                     center_x + head_radius, center_y - 80 + head_radius], 
                    fill=skin_color, outline=(0, 0, 0), width=2)
        
        # Eyes (always professional)
        eye_y = center_y - 100
        draw.ellipse([center_x - 25, eye_y, center_x - 15, eye_y + 10], fill=(0, 0, 0))
        draw.ellipse([center_x + 15, eye_y, center_x + 25, eye_y + 10], fill=(0, 0, 0))
        
        # Dynamic mouth based on audio
        mouth_y = center_y - 70
        mouth_width = 20
        mouth_height = int(mouth_opening * 15)  # Scale mouth opening
        
        if mouth_opening > 0.3:  # Talking
            # Open mouth
            draw.ellipse([center_x - mouth_width//2, mouth_y, 
                         center_x + mouth_width//2, mouth_y + mouth_height], 
                        fill=(50, 20, 20), outline=(0, 0, 0), width=1)
        else:
            # Closed mouth
            draw.line([(center_x - mouth_width//2, mouth_y), 
                      (center_x + mouth_width//2, mouth_y)], 
                     fill=(0, 0, 0), width=2)
        
        # Professional suit/shirt
        draw.polygon([
            (center_x - 80, height - 20),
            (center_x - 50, center_y - 20),
            (center_x + 50, center_y - 20),
            (center_x + 80, height - 20)
        ], fill=suit_color, outline=(0, 0, 0), width=2)
        
        # Shirt collar
        draw.polygon([
            (center_x - 25, center_y - 20),
            (center_x - 10, center_y - 40),
            (center_x + 10, center_y - 40),
            (center_x + 25, center_y - 20)
        ], fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
        # Tie
        draw.polygon([
            (center_x - 8, center_y - 35),
            (center_x + 8, center_y - 35),
            (center_x + 5, center_y + 20),
            (center_x - 5, center_y + 20)
        ], fill=(100, 20, 20), outline=(0, 0, 0), width=1)
        
        return avatar_img

    def create_animated_video_with_lipsyncing(self, background_img, audio_file, title, theme):
        """Create video with lip-syncing avatar animation"""
        
        print(f"🎬 Creating animated video with lip-syncing...")
        
        # Analyze audio for lip-sync
        speech_segments = self.analyze_audio_for_lipsyncing(audio_file)
        
        # Get audio duration
        try:
            y, sr = librosa.load(audio_file)
            duration = librosa.get_duration(y=y, sr=sr)
        except:
            duration = 30  # Fallback
        
        fps = 10  # 10 FPS for smooth lip-sync
        total_frames = int(duration * fps)
        
        # Create temporary directory for frames
        frames_dir = "temp_frames"
        os.makedirs(frames_dir, exist_ok=True)
        
        print(f"🎭 Generating {total_frames} frames with lip-syncing...")
        
        # Generate frames with lip-sync animation
        for frame_num in range(total_frames):
            current_time = frame_num / fps
            
            # Find corresponding mouth opening for this time
            mouth_opening = 0.1  # Default closed
            for segment in speech_segments:
                if abs(segment['time'] - current_time) < 0.1:  # Close enough in time
                    mouth_opening = segment['mouth_opening']
                    break
            
            # Create frame
            frame_img = background_img.copy()
            
            # Create avatar with current mouth position
            avatar = self.create_lipsyncing_avatar(VoiceEmotion.CONFIDENT, mouth_opening)
            
            # Position avatar (news anchor position)
            avatar_x = frame_img.width - 350
            avatar_y = frame_img.height - 450
            avatar_resized = avatar.resize((280, 360), Image.Resampling.LANCZOS)
            
            # Composite avatar
            frame_img.paste(avatar_resized, (avatar_x, avatar_y), avatar_resized)
            
            # Save frame
            frame_path = os.path.join(frames_dir, f"frame_{frame_num:04d}.png")
            frame_img.save(frame_path)
            
            if frame_num % 20 == 0:
                progress = (frame_num / total_frames) * 100
                print(f"   📹 Progress: {progress:.1f}% - Frame {frame_num}/{total_frames}")
        
        # Create video from frames using FFmpeg
        output_path = os.path.join("advanced_reels", f"lipsyncing_{title[:40]}.mp4")
        os.makedirs("advanced_reels", exist_ok=True)
        
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', os.path.join(frames_dir, 'frame_%04d.png'),
            '-i', audio_file,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-pix_fmt', 'yuv420p',
            '-shortest',
            output_path
        ]
        
        print(f"🎬 Creating final video with lip-syncing...")
        result = subprocess.run(cmd, capture_output=True)
        
        # Cleanup frames
        try:
            import shutil
            shutil.rmtree(frames_dir)
        except:
            pass
        
        if result.returncode == 0 and os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✅ Lip-syncing video created successfully!")
            print(f"📁 File: {output_path}")
            print(f"💾 Size: {file_size:.1f} MB")
            print(f"⏱️ Duration: {duration:.1f} seconds")
            print(f"🎭 Theme: {theme.title()}")
            print(f"👄 Lip-syncing: ✅ Dynamic mouth movement")
            print(f"🎨 Contextual background: ✅ {theme.title()} themed")
            return output_path
        else:
            print(f"❌ Video creation failed: {result.stderr.decode()}")
            return None

    def generate_advanced_reel(self, title, summary):
        """Generate advanced reel with lip-syncing and contextual backgrounds"""
        
        print(f"\n🎬 Creating advanced reel with lip-syncing: {title}")
        
        try:
            # Detect article theme
            theme = self.detect_article_theme(title, summary)
            print(f"🎯 Detected theme: {theme.title()}")
            
            # Create professional script
            script_parts = []
            script_parts.append(f"Breaking news in {theme}.")
            
            clean_title = title.replace('_', ' ').replace('-', ' ')
            script_parts.append(clean_title.lower())
            
            if summary:
                lines = summary.split('\n')
                for line in lines[:2]:
                    if line.strip() and len(line) > 20:
                        clean_line = line.strip().replace('**', '').replace('•', '')
                        script_parts.append(clean_line)
            
            script_parts.append("This represents a significant development in the field.")
            
            script = ". ".join(script_parts)
            script = script.replace("95%", "ninety-five percent").replace("$95,000", "ninety-five thousand dollars")
            
            print(f"📝 Theme-appropriate script created")
            
            # Generate professional audio
            audio_file, metadata = self.audio_service.generate_emotional_voiceover(
                script=script,
                title=title,
                category=theme,
                target_emotion=VoiceEmotion.CONFIDENT
            )
            
            if not audio_file or not os.path.exists(audio_file):
                print("❌ Audio generation failed")
                return None
            
            print(f"🎵 Professional audio generated")
            
            # Create contextual background
            background_img = self.create_contextual_background(theme, title)
            print(f"🎨 {theme.title()}-themed background created")
            
            # Create animated video with lip-syncing
            result = self.create_animated_video_with_lipsyncing(
                background_img, audio_file, title, theme
            )
            
            # Cleanup
            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except:
                pass
            
            return result
            
        except Exception as e:
            print(f"❌ Error creating advanced reel: {str(e)}")
            return None

def main():
    """Test the advanced generator"""
    generator = AdvancedDynamicReelGenerator()
    
    # Test with different themes
    test_cases = [
        {
            'title': 'Military_Defense_Budget_Increase_Pentagon_Announcement',
            'summary': 'Pentagon announces significant increase in defense budget allocation for advanced military technology and soldier equipment. Defense officials confirm new investments in cyber warfare capabilities.'
        },
        {
            'title': 'OpenAI_GPT_5_Revolutionary_AI_Breakthrough',
            'summary': 'OpenAI announces GPT-5 with unprecedented reasoning capabilities and human-level performance across multiple domains. The new AI system demonstrates significant improvements in complex problem-solving.'
        }
    ]
    
    for test in test_cases:
        result = generator.generate_advanced_reel(test['title'], test['summary'])
        if result:
            print(f"\n🎉 Advanced reel created: {result}")
        else:
            print(f"\n❌ Failed to create reel for: {test['title']}")

if __name__ == "__main__":
    main()
