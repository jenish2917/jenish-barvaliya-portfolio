"""
Human-Like Avatar System (Snapchat Style)
Creates realistic human avatars with natural facial features, expressions, and lip-syncing
Similar to Snapchat Bitmoji but more realistic for news presentation
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

class HumanLikeAvatarSystem:
    def __init__(self):
        self.content_processor = EnhancedFunnyContentProcessor()
        self.audio_service = EnhancedEmotionalAudioService()
        
        # Human avatar variations (like Snapchat)
        self.avatar_styles = {
            'news_anchor_male': {
                'skin_tone': (245, 215, 190),
                'hair_color': (60, 40, 30),
                'eye_color': (70, 50, 40),
                'suit_color': (20, 30, 60),
                'tie_color': (150, 30, 30),
                'style': 'professional_male'
            },
            'news_anchor_female': {
                'skin_tone': (250, 220, 195),
                'hair_color': (80, 50, 30),
                'eye_color': (50, 70, 90),
                'suit_color': (30, 20, 60),
                'accessories': 'earrings',
                'style': 'professional_female'
            },
            'tech_reporter_male': {
                'skin_tone': (240, 200, 170),
                'hair_color': (40, 30, 25),
                'eye_color': (60, 80, 40),
                'shirt_color': (200, 200, 200),
                'style': 'casual_professional'
            },
            'science_correspondent': {
                'skin_tone': (235, 205, 180),
                'hair_color': (100, 70, 50),
                'eye_color': (40, 60, 80),
                'lab_coat': True,
                'style': 'scientist'
            }
        }
        
        # Facial expressions for different emotions
        self.expressions = {
            'confident': {'eyebrow_height': 0.2, 'eye_opening': 0.8, 'mouth_curve': 0.3},
            'excited': {'eyebrow_height': 0.4, 'eye_opening': 1.0, 'mouth_curve': 0.6},
            'serious': {'eyebrow_height': -0.1, 'eye_opening': 0.7, 'mouth_curve': 0.0},
            'concerned': {'eyebrow_height': -0.3, 'eye_opening': 0.6, 'mouth_curve': -0.2}
        }

    def create_realistic_human_avatar(self, style='news_anchor_male', emotion='confident', mouth_opening=0.3):
        """Create realistic human-like avatar (Snapchat style)"""
        
        width, height = 400, 500
        avatar_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(avatar_img)
        
        center_x, center_y = width // 2, height // 2
        
        # Get style parameters
        style_data = self.avatar_styles.get(style, self.avatar_styles['news_anchor_male'])
        expression = self.expressions.get(emotion, self.expressions['confident'])
        
        # Realistic skin tone
        skin_color = style_data['skin_tone']
        
        # Draw realistic head shape (more human proportions)
        head_width = 120
        head_height = 140
        
        # Head with natural oval shape
        head_bbox = [center_x - head_width//2, center_y - head_height//2 - 40,
                     center_x + head_width//2, center_y + head_height//2 - 40]
        draw.ellipse(head_bbox, fill=skin_color, outline=(200, 180, 160), width=2)
        
        # Realistic hair
        hair_color = style_data['hair_color']
        if style_data['style'] == 'professional_male':
            # Professional male haircut
            hair_bbox = [center_x - head_width//2 - 10, center_y - head_height//2 - 60,
                        center_x + head_width//2 + 10, center_y - 20]
            draw.ellipse(hair_bbox, fill=hair_color, outline=hair_color)
        elif style_data['style'] == 'professional_female':
            # Professional female hairstyle
            hair_bbox = [center_x - head_width//2 - 15, center_y - head_height//2 - 60,
                        center_x + head_width//2 + 15, center_y + 10]
            draw.ellipse(hair_bbox, fill=hair_color, outline=hair_color)
        
        # Realistic eyes with expression
        eye_color = style_data['eye_color']
        eye_y = center_y - 80
        eye_opening = expression['eye_opening']
        
        # Left eye
        left_eye_bbox = [center_x - 35, eye_y, center_x - 15, eye_y + int(20 * eye_opening)]
        draw.ellipse(left_eye_bbox, fill=(255, 255, 255), outline=(150, 150, 150), width=1)
        # Iris
        iris_size = int(12 * eye_opening)
        draw.ellipse([center_x - 30, eye_y + 2, center_x - 30 + iris_size, eye_y + 2 + iris_size], 
                    fill=eye_color)
        # Pupil
        pupil_size = int(6 * eye_opening)
        draw.ellipse([center_x - 27, eye_y + 5, center_x - 27 + pupil_size, eye_y + 5 + pupil_size], 
                    fill=(0, 0, 0))
        
        # Right eye
        right_eye_bbox = [center_x + 15, eye_y, center_x + 35, eye_y + int(20 * eye_opening)]
        draw.ellipse(right_eye_bbox, fill=(255, 255, 255), outline=(150, 150, 150), width=1)
        # Iris
        draw.ellipse([center_x + 20, eye_y + 2, center_x + 20 + iris_size, eye_y + 2 + iris_size], 
                    fill=eye_color)
        # Pupil
        draw.ellipse([center_x + 23, eye_y + 5, center_x + 23 + pupil_size, eye_y + 5 + pupil_size], 
                    fill=(0, 0, 0))
        
        # Realistic eyebrows with expression
        eyebrow_y = eye_y - 15 + int(expression['eyebrow_height'] * 10)
        eyebrow_color = tuple(max(0, c - 50) for c in hair_color)
        
        # Left eyebrow
        draw.ellipse([center_x - 40, eyebrow_y, center_x - 10, eyebrow_y + 8], 
                    fill=eyebrow_color)
        # Right eyebrow
        draw.ellipse([center_x + 10, eyebrow_y, center_x + 40, eyebrow_y + 8], 
                    fill=eyebrow_color)
        
        # Realistic nose
        nose_color = tuple(max(0, c - 20) for c in skin_color)
        nose_points = [(center_x - 5, center_y - 50), (center_x + 5, center_y - 50),
                      (center_x + 8, center_y - 35), (center_x - 8, center_y - 35)]
        draw.polygon(nose_points, fill=nose_color, outline=nose_color)
        
        # Realistic mouth with lip-sync
        mouth_y = center_y - 20
        mouth_curve = expression['mouth_curve']
        
        if mouth_opening > 0.4:  # Speaking
            # Open mouth for talking
            mouth_width = 25
            mouth_height = int(mouth_opening * 15)
            
            # Mouth opening (oval shape)
            mouth_bbox = [center_x - mouth_width//2, mouth_y,
                         center_x + mouth_width//2, mouth_y + mouth_height]
            draw.ellipse(mouth_bbox, fill=(80, 40, 40), outline=(120, 80, 80), width=1)
            
            # Upper lip
            upper_lip_points = [(center_x - mouth_width//2, mouth_y),
                               (center_x, mouth_y - 3),
                               (center_x + mouth_width//2, mouth_y)]
            draw.polygon(upper_lip_points, fill=(180, 100, 100))
            
            # Lower lip
            lower_lip_points = [(center_x - mouth_width//2, mouth_y + mouth_height),
                               (center_x, mouth_y + mouth_height + 5),
                               (center_x + mouth_width//2, mouth_y + mouth_height)]
            draw.polygon(lower_lip_points, fill=(180, 100, 100))
            
        else:  # Closed mouth
            # Closed mouth with expression
            mouth_width = 30
            curve_offset = int(mouth_curve * 8)
            
            if mouth_curve > 0:  # Smile
                mouth_points = [(center_x - mouth_width//2, mouth_y + 5),
                               (center_x - 10, mouth_y + curve_offset),
                               (center_x + 10, mouth_y + curve_offset),
                               (center_x + mouth_width//2, mouth_y + 5)]
            else:  # Neutral or frown
                mouth_points = [(center_x - mouth_width//2, mouth_y + 5),
                               (center_x - 5, mouth_y + curve_offset + 5),
                               (center_x + 5, mouth_y + curve_offset + 5),
                               (center_x + mouth_width//2, mouth_y + 5)]
            
            draw.polygon(mouth_points, fill=(180, 100, 100), outline=(150, 80, 80), width=1)
        
        # Professional attire
        if style_data['style'] in ['professional_male', 'professional_female']:
            # Professional suit
            suit_color = style_data['suit_color']
            
            # Shoulders and suit jacket
            suit_points = [(center_x - 150, height - 20),
                          (center_x - 100, center_y + 60),
                          (center_x - 60, center_y + 40),
                          (center_x + 60, center_y + 40),
                          (center_x + 100, center_y + 60),
                          (center_x + 150, height - 20)]
            draw.polygon(suit_points, fill=suit_color, outline=(0, 0, 0), width=2)
            
            # White shirt/blouse collar
            collar_points = [(center_x - 40, center_y + 40),
                            (center_x - 20, center_y + 20),
                            (center_x + 20, center_y + 20),
                            (center_x + 40, center_y + 40),
                            (center_x + 25, center_y + 80),
                            (center_x - 25, center_y + 80)]
            draw.polygon(collar_points, fill=(255, 255, 255), outline=(200, 200, 200), width=1)
            
            # Tie (for male) or accessories (for female)
            if style_data['style'] == 'professional_male' and 'tie_color' in style_data:
                tie_color = style_data['tie_color']
                tie_points = [(center_x - 12, center_y + 25),
                             (center_x + 12, center_y + 25),
                             (center_x + 8, center_y + 100),
                             (center_x - 8, center_y + 100)]
                draw.polygon(tie_points, fill=tie_color, outline=(100, 0, 0), width=1)
            
            elif style_data['style'] == 'professional_female' and 'accessories' in style_data:
                # Small earrings
                draw.ellipse([center_x - head_width//2 - 8, eye_y + 15, 
                             center_x - head_width//2 - 3, eye_y + 20], 
                            fill=(200, 200, 0))
                draw.ellipse([center_x + head_width//2 + 3, eye_y + 15, 
                             center_x + head_width//2 + 8, eye_y + 20], 
                            fill=(200, 200, 0))
        
        # Add subtle shading for 3D effect
        shadow_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_overlay)
        
        # Face shading
        shadow_draw.ellipse([center_x - head_width//2 + 5, center_y - head_height//2 - 35,
                            center_x + head_width//2 + 5, center_y + head_height//2 - 35], 
                           fill=(0, 0, 0, 20))
        
        # Blend shadow
        avatar_img = Image.alpha_composite(avatar_img, shadow_overlay)
        
        return avatar_img

    def create_snapchat_style_background(self, theme, title):
        """Create modern, clean background similar to Snapchat style"""
        
        width, height = 1080, 1920
        
        # Modern gradient schemes (like Snapchat)
        gradient_schemes = {
            'technology': [(25, 118, 210), (33, 150, 243), (100, 181, 246)],  # Modern blue
            'military': [(56, 142, 60), (76, 175, 80), (129, 199, 132)],      # Modern green
            'space': [(63, 81, 181), (92, 107, 192), (159, 168, 218)],        # Modern purple
            'medical': [(26, 188, 156), (38, 198, 218), (77, 208, 225)],      # Modern teal
            'business': [(244, 67, 54), (229, 115, 115), (239, 154, 154)],    # Modern red
            'crypto': [(255, 193, 7), (255, 213, 79), (255, 238, 88)],        # Modern gold
            'science': [(76, 175, 80), (129, 199, 132), (165, 214, 167)]      # Modern green
        }
        
        colors = gradient_schemes.get(theme, gradient_schemes['technology'])
        
        # Create smooth modern gradient
        gradient_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        for y in range(height):
            ratio = y / height
            if ratio < 0.5:
                # Top to middle
                blend = ratio * 2
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * blend)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * blend)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * blend)
            else:
                # Middle to bottom
                blend = (ratio - 0.5) * 2
                r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * blend)
                g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * blend)
                b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * blend)
            
            gradient_array[y, :] = [r, g, b]
        
        img = Image.fromarray(gradient_array)
        
        # Add modern geometric elements
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Modern subtle pattern
        for i in range(0, width, 60):
            for j in range(0, height, 60):
                # Subtle dots pattern
                overlay_draw.ellipse([i + 25, j + 25, i + 35, j + 35], 
                                   fill=(255, 255, 255, 15))
        
        # Modern title design
        try:
            font_large = ImageFont.truetype("arialbd.ttf", 65)
            font_medium = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 28)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Modern header
        text_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Live indicator (like Snapchat)
        live_text = "🔴 LIVE"
        live_bbox = text_draw.textbbox((0, 0), live_text, font=font_small)
        live_width = live_bbox[2] - live_bbox[0]
        live_x = 50
        
        # Live background
        text_draw.rounded_rectangle([live_x - 15, 40, live_x + live_width + 15, 75], 
                                   radius=15, fill=(0, 0, 0, 150))
        text_draw.text((live_x, 48), live_text, font=font_small, fill=(255, 255, 255))
        
        # Modern title with better typography
        clean_title = title.replace('-', ' ').replace('_', ' ')
        words = clean_title.split()[:6]
        title_text = ' '.join(words).title()
        
        # Multi-line title
        lines = []
        max_chars = 18
        if len(title_text) > max_chars:
            words = title_text.split()
            current_line = ""
            for word in words:
                if len(current_line + " " + word) <= max_chars:
                    current_line += " " + word if current_line else word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
        else:
            lines = [title_text]
        
        # Modern title positioning (top area)
        start_y = 120
        line_height = 75
        
        for i, line in enumerate(lines[:3]):
            bbox = text_draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = 50  # Left aligned for modern look
            y = start_y + (i * line_height)
            
            # Modern text shadow
            text_draw.text((x + 3, y + 3), line, font=font_large, fill=(0, 0, 0, 100))
            text_draw.text((x, y), line, font=font_large, fill=(255, 255, 255))
        
        # Modern timestamp
        timestamp = datetime.now().strftime("%I:%M %p • %b %d")
        time_x = 50
        time_y = height - 100
        text_draw.text((time_x, time_y), timestamp, font=font_medium, fill=(255, 255, 255, 200))
        
        # Theme indicator
        theme_labels = {
            'technology': "💻 TECH",
            'military': "🛡️ DEFENSE", 
            'space': "🚀 SPACE",
            'medical': "🏥 HEALTH",
            'business': "💼 BUSINESS",
            'crypto': "₿ CRYPTO",
            'science': "🔬 SCIENCE"
        }
        
        theme_text = theme_labels.get(theme, "📰 NEWS")
        theme_bbox = text_draw.textbbox((0, 0), theme_text, font=font_medium)
        theme_width = theme_bbox[2] - theme_bbox[0]
        theme_x = width - theme_width - 50
        theme_y = height - 100
        
        text_draw.rounded_rectangle([theme_x - 15, theme_y - 10, theme_x + theme_width + 15, theme_y + 35], 
                                   radius=20, fill=(255, 255, 255, 30))
        text_draw.text((theme_x, theme_y), theme_text, font=font_medium, fill=(255, 255, 255))
        
        # Blend overlays
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        img = Image.alpha_composite(img.convert('RGBA'), text_img).convert('RGB')
        
        return img

    def analyze_audio_for_realistic_lipsyncing(self, audio_file):
        """Enhanced audio analysis for realistic mouth movement"""
        try:
            import librosa
            y, sr = librosa.load(audio_file)
            
            # More detailed analysis for realistic movement
            hop_length = 256  # Higher resolution
            frame_length = 1024
            
            # RMS energy
            rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
            
            # Spectral centroid for speech detection
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
            
            # Zero crossing rate for consonant detection
            zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame_length, hop_length=hop_length)[0]
            
            times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=hop_length)
            
            # Normalize features
            rms_norm = (rms - rms.min()) / (rms.max() - rms.min() + 1e-8)
            centroid_norm = (spectral_centroids - spectral_centroids.min()) / (spectral_centroids.max() - spectral_centroids.min() + 1e-8)
            zcr_norm = (zcr - zcr.min()) / (zcr.max() - zcr.min() + 1e-8)
            
            # Create realistic mouth movements
            speech_segments = []
            for i in range(len(times)):
                # Combine features for more realistic movement
                volume = rms_norm[i]
                speech_activity = centroid_norm[i]
                consonant_activity = zcr_norm[i]
                
                # Calculate mouth opening based on multiple factors
                base_opening = volume * 0.6
                speech_modifier = speech_activity * 0.3
                consonant_modifier = consonant_activity * 0.2
                
                mouth_opening = min(base_opening + speech_modifier + consonant_modifier, 1.0)
                
                # Add natural variation
                if mouth_opening > 0.15:
                    natural_variation = 0.1 * math.sin(times[i] * 10)  # Natural flutter
                    mouth_opening += natural_variation
                    mouth_opening = max(0.1, min(mouth_opening, 1.0))
                else:
                    mouth_opening = 0.05 + random.uniform(0, 0.1)  # Slight closed position
                
                speech_segments.append({
                    'time': times[i],
                    'mouth_opening': mouth_opening,
                    'talking': mouth_opening > 0.2,
                    'volume': volume,
                    'speech_quality': speech_activity
                })
            
            return speech_segments
            
        except Exception as e:
            print(f"Error in advanced audio analysis: {e}")
            # Enhanced fallback
            duration = 30
            segments = []
            for i in range(int(duration * 20)):  # 20 FPS for smoother animation
                time_pos = i / 20.0
                base_wave = 0.4 + 0.3 * abs(math.sin(time_pos * 3))
                natural_flutter = 0.1 * math.sin(time_pos * 15)
                mouth_opening = base_wave + natural_flutter
                mouth_opening = max(0.1, min(mouth_opening, 0.9))
                
                segments.append({
                    'time': time_pos,
                    'mouth_opening': mouth_opening,
                    'talking': mouth_opening > 0.3,
                    'volume': mouth_opening,
                    'speech_quality': 0.8
                })
            return segments

    def generate_snapchat_style_reel(self, title, summary, avatar_style='news_anchor_male'):
        """Generate Snapchat-style reel with human-like avatar"""
        
        print(f"\n🎬 Creating Snapchat-style reel: {title}")
        
        try:
            # Detect theme
            content = (title + " " + summary).lower()
            if any(word in content for word in ['military', 'defense', 'pentagon']):
                theme = 'military'
            elif any(word in content for word in ['tech', 'ai', 'iphone', 'openai']):
                theme = 'technology'
            elif any(word in content for word in ['space', 'nasa', 'europa']):
                theme = 'space'
            elif any(word in content for word in ['medical', 'health', 'drug']):
                theme = 'medical'
            elif any(word in content for word in ['bitcoin', 'crypto']):
                theme = 'crypto'
            else:
                theme = 'business'
            
            print(f"🎯 Theme detected: {theme.title()}")
            
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
            
            script_parts.append("This represents a major development.")
            script = ". ".join(script_parts)
            
            print(f"📝 Professional script created")
            
            # Generate audio
            audio_file, metadata = self.audio_service.generate_emotional_voiceover(
                script=script,
                title=title,
                category=theme,
                target_emotion=VoiceEmotion.CONFIDENT
            )
            
            if not audio_file:
                print("❌ Audio generation failed")
                return None
            
            print(f"🎵 Audio generated successfully")
            
            # Analyze audio for realistic lip-syncing
            speech_segments = self.analyze_audio_for_realistic_lipsyncing(audio_file)
            
            # Create Snapchat-style background
            background_img = self.create_snapchat_style_background(theme, title)
            print(f"🎨 Modern {theme} background created")
            
            # Get audio duration
            try:
                import librosa
                y, sr = librosa.load(audio_file)
                duration = librosa.get_duration(y=y, sr=sr)
            except:
                duration = 30
            
            # Create high-quality animation
            fps = 20  # Higher FPS for smoother animation
            total_frames = int(duration * fps)
            frames_dir = "snapchat_frames"
            os.makedirs(frames_dir, exist_ok=True)
            
            print(f"🎭 Generating {total_frames} frames with realistic lip-syncing...")
            
            for frame_num in range(total_frames):
                current_time = frame_num / fps
                
                # Find mouth opening for this time
                mouth_opening = 0.1
                emotion_state = 'confident'
                
                for segment in speech_segments:
                    if abs(segment['time'] - current_time) < 0.05:
                        mouth_opening = segment['mouth_opening']
                        if segment['speech_quality'] > 0.7:
                            emotion_state = 'confident'
                        elif segment['volume'] > 0.8:
                            emotion_state = 'excited'
                        break
                
                # Create frame
                frame_img = background_img.copy()
                
                # Create realistic human avatar
                avatar = self.create_realistic_human_avatar(
                    style=avatar_style,
                    emotion=emotion_state,
                    mouth_opening=mouth_opening
                )
                
                # Position avatar (modern placement)
                avatar_x = frame_img.width - 450
                avatar_y = frame_img.height - 550
                avatar_resized = avatar.resize((350, 450), Image.Resampling.LANCZOS)
                
                # Create soft shadow for avatar
                shadow = Image.new('RGBA', frame_img.size, (0, 0, 0, 0))
                shadow_draw = ImageDraw.Draw(shadow)
                shadow_draw.ellipse([avatar_x + 10, avatar_y + 400, avatar_x + 340, avatar_y + 440], 
                                   fill=(0, 0, 0, 50))
                
                # Composite everything
                frame_img = Image.alpha_composite(frame_img.convert('RGBA'), shadow)
                frame_img.paste(avatar_resized, (avatar_x, avatar_y), avatar_resized)
                
                # Save frame
                frame_path = os.path.join(frames_dir, f"frame_{frame_num:05d}.png")
                frame_img.save(frame_path)
                
                if frame_num % 40 == 0:
                    progress = (frame_num / total_frames) * 100
                    print(f"   📹 Progress: {progress:.1f}% - Frame {frame_num}/{total_frames}")
            
            # Create final video
            output_path = os.path.join("snapchat_reels", f"human_{title[:40]}.mp4")
            os.makedirs("snapchat_reels", exist_ok=True)
            
            cmd = [
                'ffmpeg', '-y',
                '-framerate', str(fps),
                '-i', os.path.join(frames_dir, 'frame_%05d.png'),
                '-i', audio_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                '-crf', '18',  # Higher quality
                '-shortest',
                output_path
            ]
            
            print(f"🎬 Creating final Snapchat-style video...")
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
                print(f"✅ Snapchat-style reel created successfully!")
                print(f"📁 File: {output_path}")
                print(f"💾 Size: {file_size:.1f} MB")
                print(f"⏱️ Duration: {duration:.1f} seconds")
                print(f"🎭 Theme: {theme.title()}")
                print(f"👤 Avatar: Human-like {avatar_style}")
                print(f"👄 Lip-syncing: ✅ Realistic movement")
                print(f"🎨 Style: Snapchat-quality modern design")
                return output_path
            else:
                print(f"❌ Video creation failed")
                return None
                
        except Exception as e:
            print(f"❌ Error creating Snapchat-style reel: {str(e)}")
            return None

def main():
    """Test the human-like avatar system"""
    system = HumanLikeAvatarSystem()
    
    # Test with military news
    result = system.generate_snapchat_style_reel(
        title="Pentagon_Military_Defense_Budget_Increase_Announcement",
        summary="Pentagon announces significant increase in military defense budget allocation for advanced warfare technology and soldier equipment.",
        avatar_style="news_anchor_male"
    )
    
    if result:
        print(f"\n🎉 Snapchat-style reel created: {result}")

if __name__ == "__main__":
    main()
