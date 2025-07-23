"""
Snapchat-Style Human Avatar Generator
Creates realistic human-like avatars with natural facial features, expressions, and animations
Similar to Snapchat Bitmoji but more realistic and professional
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
import math

class SnapchatStyleAvatarGenerator:
    def __init__(self):
        self.content_processor = EnhancedFunnyContentProcessor()
        self.audio_service = EnhancedEmotionalAudioService()
        
        # Realistic human features
        self.human_features = {
            'skin_tones': [
                (255, 220, 177),  # Light
                (241, 194, 125),  # Medium light
                (224, 172, 105),  # Medium
                (198, 134, 66),   # Medium dark
                (141, 85, 36)     # Dark
            ],
            'hair_colors': [
                (139, 69, 19),    # Brown
                (0, 0, 0),        # Black
                (255, 222, 173),  # Blonde
                (165, 42, 42),    # Auburn
                (128, 128, 128)   # Gray
            ],
            'eye_colors': [
                (139, 69, 19),    # Brown
                (70, 130, 180),   # Blue
                (34, 139, 34),    # Green
                (128, 128, 128),  # Gray
                (0, 0, 0)         # Black
            ]
        }
        
        # Professional avatar styles
        self.avatar_styles = {
            'news_anchor_male': {
                'hair_style': 'professional_short',
                'clothing': 'business_suit',
                'facial_hair': 'clean_shaven',
                'expression_base': 'confident'
            },
            'news_anchor_female': {
                'hair_style': 'professional_medium',
                'clothing': 'business_blazer',
                'facial_hair': 'none',
                'expression_base': 'friendly_professional'
            },
            'tech_reporter': {
                'hair_style': 'modern_casual',
                'clothing': 'smart_casual',
                'facial_hair': 'light_stubble',
                'expression_base': 'enthusiastic'
            }
        }

    def create_realistic_human_face(self, width, height, style='news_anchor_male', emotion=VoiceEmotion.CONFIDENT, mouth_opening=0.3):
        """Create realistic human-like face similar to Snapchat avatars"""
        
        # Create canvas
        face_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(face_img)
        
        center_x, center_y = width // 2, height // 2
        
        # Choose realistic features
        skin_tone = random.choice(self.human_features['skin_tones'])
        hair_color = random.choice(self.human_features['hair_colors'])
        eye_color = random.choice(self.human_features['eye_colors'])
        
        # Face shape (more realistic oval)
        face_width = width * 0.7
        face_height = height * 0.8
        face_left = center_x - face_width // 2
        face_top = center_y - face_height // 2
        face_right = center_x + face_width // 2
        face_bottom = center_y + face_height // 2
        
        # Draw realistic face shape
        draw.ellipse([face_left, face_top, face_right, face_bottom], 
                    fill=skin_tone, outline=(0, 0, 0, 50), width=2)
        
        # Add face shading for 3D effect
        shadow_color = tuple(max(0, c - 30) for c in skin_tone[:3]) + (80,)
        draw.ellipse([face_left + 10, face_top + 15, face_right, face_bottom], 
                    fill=shadow_color)
        
        # Realistic eyes
        eye_y = center_y - face_height * 0.15
        eye_width = 25
        eye_height = 15
        
        # Left eye
        left_eye_x = center_x - face_width * 0.2
        draw.ellipse([left_eye_x - eye_width//2, eye_y - eye_height//2,
                     left_eye_x + eye_width//2, eye_y + eye_height//2], 
                    fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
        # Left eye iris
        iris_size = 12
        draw.ellipse([left_eye_x - iris_size//2, eye_y - iris_size//2,
                     left_eye_x + iris_size//2, eye_y + iris_size//2], 
                    fill=eye_color)
        
        # Left eye pupil
        pupil_size = 6
        draw.ellipse([left_eye_x - pupil_size//2, eye_y - pupil_size//2,
                     left_eye_x + pupil_size//2, eye_y + pupil_size//2], 
                    fill=(0, 0, 0))
        
        # Eye highlight for realism
        draw.ellipse([left_eye_x - 2, eye_y - 3, left_eye_x + 2, eye_y + 1], 
                    fill=(255, 255, 255))
        
        # Right eye (mirror left)
        right_eye_x = center_x + face_width * 0.2
        draw.ellipse([right_eye_x - eye_width//2, eye_y - eye_height//2,
                     right_eye_x + eye_width//2, eye_y + eye_height//2], 
                    fill=(255, 255, 255), outline=(0, 0, 0), width=1)
        
        draw.ellipse([right_eye_x - iris_size//2, eye_y - iris_size//2,
                     right_eye_x + iris_size//2, eye_y + iris_size//2], 
                    fill=eye_color)
        
        draw.ellipse([right_eye_x - pupil_size//2, eye_y - pupil_size//2,
                     right_eye_x + pupil_size//2, eye_y + pupil_size//2], 
                    fill=(0, 0, 0))
        
        draw.ellipse([right_eye_x - 2, eye_y - 3, right_eye_x + 2, eye_y + 1], 
                    fill=(255, 255, 255))
        
        # Realistic eyebrows
        brow_color = tuple(max(0, c - 50) for c in hair_color[:3])
        brow_y = eye_y - 20
        
        # Left eyebrow
        draw.ellipse([left_eye_x - 15, brow_y - 3, left_eye_x + 15, brow_y + 3], 
                    fill=brow_color)
        
        # Right eyebrow  
        draw.ellipse([right_eye_x - 15, brow_y - 3, right_eye_x + 15, brow_y + 3], 
                    fill=brow_color)
        
        # Realistic nose
        nose_y = center_y
        nose_width = 8
        nose_height = 15
        nose_color = tuple(max(0, c - 10) for c in skin_tone[:3])
        
        # Nose shape
        draw.ellipse([center_x - nose_width//2, nose_y - nose_height//2,
                     center_x + nose_width//2, nose_y + nose_height//2], 
                    fill=nose_color, outline=(0, 0, 0, 30), width=1)
        
        # Nostrils
        draw.ellipse([center_x - 4, nose_y + 5, center_x - 2, nose_y + 7], fill=(0, 0, 0, 100))
        draw.ellipse([center_x + 2, nose_y + 5, center_x + 4, nose_y + 7], fill=(0, 0, 0, 100))
        
        # Dynamic realistic mouth based on speech
        mouth_y = center_y + face_height * 0.25
        mouth_width = 30
        
        if mouth_opening > 0.4:  # Speaking
            # Open mouth for speech
            mouth_height = int(mouth_opening * 20)
            draw.ellipse([center_x - mouth_width//2, mouth_y - mouth_height//2,
                         center_x + mouth_width//2, mouth_y + mouth_height//2], 
                        fill=(50, 20, 20), outline=(0, 0, 0), width=1)
            
            # Teeth
            if mouth_opening > 0.6:
                draw.ellipse([center_x - mouth_width//3, mouth_y - mouth_height//3,
                             center_x + mouth_width//3, mouth_y], 
                            fill=(255, 255, 255))
        else:
            # Closed mouth - natural smile
            if emotion in [VoiceEmotion.EXCITED, VoiceEmotion.CONFIDENT]:
                # Slight smile
                draw.arc([center_x - mouth_width//2, mouth_y - 5,
                         center_x + mouth_width//2, mouth_y + 10], 
                        0, 180, fill=(100, 50, 50), width=3)
            else:
                # Neutral expression
                draw.line([(center_x - mouth_width//2, mouth_y), 
                          (center_x + mouth_width//2, mouth_y)], 
                         fill=(100, 50, 50), width=3)
        
        # Realistic hair
        hair_y = face_top - 20
        hair_width = face_width + 20
        hair_height = 40
        
        # Hair shape based on style
        if style in ['news_anchor_male', 'tech_reporter']:
            # Short professional hair
            draw.ellipse([center_x - hair_width//2, hair_y, 
                         center_x + hair_width//2, hair_y + hair_height], 
                        fill=hair_color)
        else:  # Female styles
            # Longer hair
            hair_height = 60
            draw.ellipse([center_x - hair_width//2, hair_y, 
                         center_x + hair_width//2, hair_y + hair_height], 
                        fill=hair_color)
            
            # Side hair
            draw.ellipse([face_left - 15, face_top, face_left + 10, face_bottom - 30], 
                        fill=hair_color)
            draw.ellipse([face_right - 10, face_top, face_right + 15, face_bottom - 30], 
                        fill=hair_color)
        
        # Professional clothing
        clothing_y = face_bottom - 20
        clothing_width = width
        clothing_height = height - clothing_y
        
        if 'suit' in style or 'business' in style:
            # Business suit
            suit_color = (30, 30, 60)  # Navy blue
            draw.rectangle([0, clothing_y, width, height], fill=suit_color)
            
            # Shirt collar
            collar_color = (255, 255, 255)
            draw.polygon([
                (center_x - 25, clothing_y),
                (center_x - 10, clothing_y + 25),
                (center_x + 10, clothing_y + 25),
                (center_x + 25, clothing_y)
            ], fill=collar_color, outline=(0, 0, 0), width=1)
            
            # Tie
            tie_color = (150, 30, 30)  # Red tie
            draw.polygon([
                (center_x - 8, clothing_y + 20),
                (center_x + 8, clothing_y + 20),
                (center_x + 5, height - 10),
                (center_x - 5, height - 10)
            ], fill=tie_color, outline=(0, 0, 0), width=1)
        else:
            # Casual/blazer
            blazer_color = (60, 60, 90)
            draw.rectangle([0, clothing_y, width, height], fill=blazer_color)
            
            # Shirt underneath
            shirt_color = (200, 200, 220)
            draw.polygon([
                (center_x - 20, clothing_y),
                (center_x - 15, clothing_y + 20),
                (center_x + 15, clothing_y + 20),
                (center_x + 20, clothing_y)
            ], fill=shirt_color)
        
        return face_img

    def create_snapchat_style_background(self, theme, title):
        """Create modern Snapchat-style background"""
        
        width, height = 1080, 1920
        
        # Modern gradient colors (Snapchat style)
        modern_themes = {
            'technology': {
                'colors': [(15, 32, 39), (32, 58, 67), (44, 83, 100)],  # Modern tech blue
                'accent': (0, 173, 181),  # Cyan accent
                'pattern': 'tech_grid'
            },
            'military': {
                'colors': [(25, 42, 25), (42, 69, 42), (59, 96, 59)],  # Modern military green
                'accent': (76, 175, 80),  # Green accent
                'pattern': 'tactical_grid'
            },
            'space': {
                'colors': [(13, 13, 40), (26, 26, 80), (39, 39, 120)],  # Deep space blue
                'accent': (156, 39, 176),  # Purple accent
                'pattern': 'cosmic_grid'
            },
            'medical': {
                'colors': [(25, 35, 45), (50, 70, 90), (75, 105, 135)],  # Medical blue
                'accent': (33, 150, 243),  # Medical blue accent
                'pattern': 'medical_grid'
            },
            'crypto': {
                'colors': [(45, 35, 15), (90, 70, 30), (135, 105, 45)],  # Gold gradient
                'accent': (255, 193, 7),  # Gold accent
                'pattern': 'crypto_grid'
            },
            'science': {
                'colors': [(15, 45, 25), (30, 90, 50), (45, 135, 75)],  # Science green
                'accent': (76, 175, 80),  # Green accent
                'pattern': 'science_grid'
            }
        }
        
        theme_data = modern_themes.get(theme, modern_themes['technology'])
        colors = theme_data['colors']
        accent_color = theme_data['accent']
        
        # Create modern gradient
        img = Image.new('RGB', (width, height), colors[0])
        
        # Smooth gradient with multiple stops
        gradient_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for y in range(height):
            ratio = y / height
            if ratio < 0.3:
                # Top section
                blend = ratio / 0.3
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * blend)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * blend)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * blend)
            elif ratio < 0.7:
                # Middle section
                blend = (ratio - 0.3) / 0.4
                r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * blend)
                g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * blend)
                b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * blend)
            else:
                # Bottom section
                blend = (ratio - 0.7) / 0.3
                r = int(colors[2][0] * (1 - blend * 0.2))
                g = int(colors[2][1] * (1 - blend * 0.2))
                b = int(colors[2][2] * (1 - blend * 0.2))
            
            gradient_array[y, :] = [r, g, b]
        
        img = Image.fromarray(gradient_array)
        
        # Modern overlay pattern
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Snapchat-style modern elements
        for i in range(0, width, 100):
            for j in range(0, height, 100):
                # Subtle modern grid
                overlay_draw.rectangle([i, j, i+1, j+50], fill=accent_color + (20,))
                overlay_draw.rectangle([i, j, i+50, j+1], fill=accent_color + (20,))
                
                # Modern accent dots
                if (i + j) % 300 == 0:
                    overlay_draw.ellipse([i+45, j+45, i+55, j+55], fill=accent_color + (60,))
        
        # Blend overlay
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # Modern title styling
        try:
            font_large = ImageFont.truetype("arialbd.ttf", 65)
            font_medium = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 30)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add modern title layout
        text_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Modern "LIVE" indicator (Snapchat style)
        live_text = "LIVE"
        live_bg = (244, 67, 54)  # Red background
        text_draw.rectangle([30, 30, 120, 70], fill=live_bg, 
                          outline=(255, 255, 255), width=2)
        text_draw.text((45, 40), live_text, font=font_small, fill=(255, 255, 255))
        
        # Clean modern title
        clean_title = title.replace('-', ' ').replace('_', ' ')
        words = clean_title.split()[:6]
        title_text = ' '.join(words).title()
        
        # Multi-line title with modern styling
        max_chars_per_line = 18
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
        
        # Draw title with modern shadow effect
        start_y = 120
        line_height = 75
        
        for i, line in enumerate(lines[:3]):
            bbox = text_draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = 50  # Left aligned for modern look
            y = start_y + (i * line_height)
            
            # Modern shadow
            text_draw.text((x+4, y+4), line, font=font_large, fill=(0, 0, 0, 100))
            text_draw.text((x, y), line, font=font_large, fill=(255, 255, 255))
        
        # Modern timestamp and category
        timestamp = datetime.now().strftime("%I:%M %p • %b %d")
        category_text = theme.upper()
        
        # Bottom info bar
        info_text = f"{timestamp}                {category_text}"
        text_draw.text((50, height - 80), info_text, font=font_small, 
                      fill=(255, 255, 255, 200))
        
        # Modern accent line
        text_draw.rectangle([50, height - 50, width - 50, height - 47], 
                          fill=accent_color + (150,))
        
        # Composite text
        img = Image.alpha_composite(img.convert('RGBA'), text_img).convert('RGB')
        
        return img

    def generate_snapchat_style_reel(self, title, summary):
        """Generate reel with Snapchat-style human avatars"""
        
        print(f"\n🎬 Creating Snapchat-style human avatar reel: {title}")
        
        try:
            # Detect theme
            theme = self.detect_article_theme(title, summary)
            print(f"🎯 Theme: {theme.title()}")
            
            # Create professional script
            script = self.create_professional_script(title, summary, theme)
            print(f"📝 Professional script created")
            
            # Generate audio
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
            
            # Create Snapchat-style background
            background_img = self.create_snapchat_style_background(theme, title)
            print(f"🎨 Snapchat-style {theme} background created")
            
            # Analyze audio for lip-sync
            speech_segments = self.analyze_audio_for_lipsyncing(audio_file)
            
            # Get audio duration
            try:
                import librosa
                y, sr = librosa.load(audio_file)
                duration = librosa.get_duration(y=y, sr=sr)
            except:
                duration = 30
            
            fps = 15  # Higher FPS for smoother animation
            total_frames = int(duration * fps)
            
            # Create frames directory
            frames_dir = "temp_human_frames"
            os.makedirs(frames_dir, exist_ok=True)
            
            print(f"👤 Generating {total_frames} frames with realistic human avatar...")
            
            # Choose avatar style
            avatar_style = 'news_anchor_male' if theme in ['military', 'technology'] else 'news_anchor_female'
            
            # Generate frames with Snapchat-style human avatar
            for frame_num in range(total_frames):
                current_time = frame_num / fps
                
                # Find mouth opening for this time
                mouth_opening = 0.1
                for segment in speech_segments:
                    if abs(segment['time'] - current_time) < 0.07:
                        mouth_opening = segment['mouth_opening']
                        break
                
                # Create frame
                frame_img = background_img.copy()
                
                # Create realistic human avatar
                human_avatar = self.create_realistic_human_face(
                    width=350, 
                    height=450, 
                    style=avatar_style,
                    emotion=VoiceEmotion.CONFIDENT, 
                    mouth_opening=mouth_opening
                )
                
                # Position avatar (modern placement)
                avatar_x = frame_img.width - 400
                avatar_y = frame_img.height - 500
                
                # Composite with smooth blending
                frame_img.paste(human_avatar, (avatar_x, avatar_y), human_avatar)
                
                # Save frame
                frame_path = os.path.join(frames_dir, f"frame_{frame_num:04d}.png")
                frame_img.save(frame_path)
                
                if frame_num % 30 == 0:
                    progress = (frame_num / total_frames) * 100
                    print(f"   👤 Progress: {progress:.1f}% - Frame {frame_num}/{total_frames}")
            
            # Create video
            output_path = os.path.join("human_reels", f"human_{title[:40]}.mp4")
            os.makedirs("human_reels", exist_ok=True)
            
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
            
            print(f"🎬 Creating final video with human avatar...")
            result = subprocess.run(cmd, capture_output=True)
            
            # Cleanup
            try:
                import shutil
                shutil.rmtree(frames_dir)
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            except:
                pass
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"✅ Snapchat-style human avatar reel created!")
                print(f"📁 File: {output_path}")
                print(f"💾 Size: {file_size:.1f} MB")
                print(f"⏱️ Duration: {duration:.1f} seconds")
                print(f"👤 Avatar: Realistic human-like ({avatar_style})")
                print(f"🎨 Background: Modern {theme} theme")
                return output_path
            else:
                print(f"❌ Video creation failed")
                return None
                
        except Exception as e:
            print(f"❌ Error creating Snapchat-style reel: {str(e)}")
            return None

    def detect_article_theme(self, title, summary):
        """Detect theme for contextual backgrounds"""
        content = (title + " " + summary).lower()
        
        if any(word in content for word in ['military', 'pentagon', 'defense', 'army', 'navy']):
            return 'military'
        elif any(word in content for word in ['tech', 'ai', 'iphone', 'technology']):
            return 'technology'
        elif any(word in content for word in ['nasa', 'space', 'europa', 'mars']):
            return 'space'
        elif any(word in content for word in ['medical', 'drug', 'alzheimer', 'health']):
            return 'medical'
        elif any(word in content for word in ['bitcoin', 'crypto', 'cryptocurrency']):
            return 'crypto'
        elif any(word in content for word in ['science', 'research', 'climate', 'discovery']):
            return 'science'
        else:
            return 'technology'

    def create_professional_script(self, title, summary, theme):
        """Create professional news script"""
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
        
        script_parts.append("This represents a significant development.")
        
        script = ". ".join(script_parts)
        return script.replace("95%", "ninety-five percent").replace("$95,000", "ninety-five thousand dollars")

    def analyze_audio_for_lipsyncing(self, audio_file):
        """Analyze audio for lip-sync"""
        try:
            import librosa
            y, sr = librosa.load(audio_file)
            
            hop_length = 512
            frame_length = 2048
            
            rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
            times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
            
            rms_normalized = (rms - rms.min()) / (rms.max() - rms.min() + 1e-8)
            
            speech_segments = []
            threshold = 0.02
            
            for i, amplitude in enumerate(rms_normalized):
                if amplitude > threshold:
                    mouth_opening = min(amplitude * 1.5, 1.0)
                    speech_segments.append({
                        'time': times[i],
                        'mouth_opening': mouth_opening,
                        'talking': True
                    })
                else:
                    speech_segments.append({
                        'time': times[i],
                        'mouth_opening': 0.1,
                        'talking': False
                    })
            
            return speech_segments
            
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            duration = 30
            segments = []
            for i in range(0, int(duration * 15)):  # 15 FPS
                time_pos = i / 15.0
                mouth_opening = 0.3 + 0.4 * abs(np.sin(time_pos * 4))
                segments.append({
                    'time': time_pos,
                    'mouth_opening': mouth_opening,
                    'talking': True
                })
            return segments

def main():
    """Test the Snapchat-style generator"""
    generator = SnapchatStyleAvatarGenerator()
    
    test_title = "Pentagon_Military_Defense_Budget_Increase"
    test_summary = "Pentagon announces significant military defense budget increase for advanced technology and equipment."
    
    result = generator.generate_snapchat_style_reel(test_title, test_summary)
    
    if result:
        print(f"\n🎉 Snapchat-style human avatar reel created: {result}")
    else:
        print("\n❌ Failed to create reel")

if __name__ == "__main__":
    main()
