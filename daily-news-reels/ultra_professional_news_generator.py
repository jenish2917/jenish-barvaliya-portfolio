"""
Ultra Professional News Reel Generator
Creates broadcast-quality news reels with sophisticated visuals and professional presentation
Designed for serious news content with no cartoon or childish elements
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

class UltraProfessionalNewsGenerator:
    def __init__(self):
        self.content_processor = EnhancedFunnyContentProcessor()
        self.audio_service = EnhancedEmotionalAudioService()
        
        # Ultra professional script templates
        self.professional_templates = {
            'technology': {
                'opener': [
                    "Breaking: Major technology development announced today.",
                    "In a significant technological advancement,",
                    "Technology leaders confirm breakthrough in",
                    "Industry sources report major progress in"
                ],
                'style': 'authoritative and clear',
                'personality': 'news_anchor'
            },
            'science': {
                'opener': [
                    "Scientists announce groundbreaking discovery in",
                    "Research teams confirm significant findings about",
                    "Latest studies reveal important developments in",
                    "Medical researchers report breakthrough in"
                ],
                'style': 'informative and authoritative',
                'personality': 'news_anchor'
            },
            'business': {
                'opener': [
                    "Financial markets respond to news of",
                    "Economic developments show significant impact from",
                    "Business leaders announce major changes in",
                    "Market analysts confirm trends in"
                ],
                'style': 'professional and informative',
                'personality': 'news_anchor'
            },
            'health': {
                'opener': [
                    "Health officials report important developments in",
                    "Medical breakthrough announced in treatment of",
                    "Healthcare researchers confirm progress in",
                    "Clinical trials show promising results for"
                ],
                'style': 'serious and informative',
                'personality': 'news_anchor'
            }
        }
    
    def categorize_news(self, title):
        """Categorize news for appropriate professional treatment"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['tech', 'ai', 'robot', 'digital', 'software', 'app', 'iphone', 'tesla', 'google', 'apple']):
            return 'technology'
        elif any(word in title_lower for word in ['science', 'research', 'discovery', 'space', 'nasa', 'study', 'europa', 'mars']):
            return 'science'
        elif any(word in title_lower for word in ['bitcoin', 'market', 'business', 'economy', 'finance', 'stock', 'bank', 'amazon']):
            return 'business'
        elif any(word in title_lower for word in ['health', 'medical', 'drug', 'alzheimer', 'treatment', 'disease']):
            return 'health'
        else:
            return 'technology'

    def create_professional_script(self, title, summary):
        """Create broadcast-quality news script"""
        
        category = self.categorize_news(title)
        template = self.professional_templates[category]
        
        # Professional script structure
        script_parts = []
        
        # Professional opener
        opener = random.choice(template['opener'])
        script_parts.append(opener)
        
        # Clean title presentation
        clean_title = title.replace('_', ' ').replace('-', ' ')
        clean_title = clean_title.replace('GPT-5', 'GPT Five')
        clean_title = clean_title.replace('iPhone 17', 'iPhone Seventeen')
        script_parts.append(clean_title.lower())
        
        # Extract key information from summary
        if summary:
            lines = summary.split('\n')
            key_info = []
            
            for line in lines:
                if line.strip() and not line.startswith('#') and not line.startswith('*'):
                    clean_line = line.strip()
                    # Remove emojis and symbols
                    clean_line = ''.join(char for char in clean_line if ord(char) < 0x1F600 or ord(char) > 0x1F64F)
                    clean_line = ''.join(char for char in clean_line if ord(char) < 0x1F300 or ord(char) > 0x1F5FF)
                    clean_line = ''.join(char for char in clean_line if ord(char) < 0x1F680 or ord(char) > 0x1F6FF)
                    clean_line = ''.join(char for char in clean_line if ord(char) < 0x2600 or ord(char) > 0x26FF)
                    clean_line = clean_line.replace('**', '').replace('•', '').replace('*', '')
                    
                    if len(clean_line) > 20 and len(key_info) < 2:
                        key_info.append(clean_line)
            
            # Add professional details
            for info in key_info:
                script_parts.append(info)
        
        # Professional closing
        closings = [
            "Industry experts are monitoring developments closely.",
            "Further details are expected to be announced soon.",
            "This represents a significant development in the field.",
            "Analysts predict widespread impact from this announcement."
        ]
        
        script_parts.append(random.choice(closings))
        
        # Join professionally
        full_script = ". ".join(script_parts)
        
        # Professional number handling
        full_script = full_script.replace("95%", "ninety-five percent")
        full_script = full_script.replace("90%", "ninety percent")
        full_script = full_script.replace("$95,000", "ninety-five thousand dollars")
        full_script = full_script.replace("$50 billion", "fifty billion dollars")
        full_script = full_script.replace("1000x", "one thousand times faster")
        
        # Remove any remaining symbols
        full_script = full_script.replace("📰", "").replace("🔍", "").replace("💥", "")
        full_script = full_script.replace("⏰", "").replace("🎯", "").replace("❓", "")
        full_script = full_script.replace("  ", " ").strip()
        
        return full_script

    def create_broadcast_background(self, category, title):
        """Create broadcast-quality professional background"""
        
        width, height = 1080, 1920
        
        # Sophisticated color schemes (darker, more professional)
        color_schemes = {
            'technology': [(15, 25, 45), (25, 40, 70), (35, 55, 95)],      # Deep professional blue
            'science': [(20, 35, 25), (30, 55, 40), (40, 75, 55)],        # Deep forest green
            'business': [(45, 25, 25), (70, 40, 40), (95, 55, 55)],       # Deep burgundy
            'health': [(35, 25, 45), (55, 40, 70), (75, 55, 95)]          # Deep professional purple
        }
        
        colors = color_schemes.get(category, color_schemes['technology'])
        
        # Create sophisticated gradient
        img = Image.new('RGB', (width, height), colors[0])
        
        # Professional gradient with multiple layers
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
                # Bottom section - darker
                blend = (ratio - 0.7) / 0.3
                r = int(colors[2][0] * (1 - blend * 0.3))
                g = int(colors[2][1] * (1 - blend * 0.3))
                b = int(colors[2][2] * (1 - blend * 0.3))
            
            gradient_array[y, :] = [r, g, b]
        
        img = Image.fromarray(gradient_array)
        
        # Add professional geometric overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Subtle professional lines
        for i in range(0, width, 200):
            overlay_draw.line([(i, 0), (i, height)], fill=(255, 255, 255, 8), width=1)
        
        for j in range(0, height, 200):
            overlay_draw.line([(0, j), (width, j)], fill=(255, 255, 255, 8), width=1)
        
        # Professional corner elements
        overlay_draw.rectangle([0, 0, width, 80], fill=(0, 0, 0, 40))  # Top bar
        overlay_draw.rectangle([0, height-80, width, height], fill=(0, 0, 0, 40))  # Bottom bar
        
        # Blend overlay
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # Add professional title
        try:
            # Try to use a professional font
            font_large = ImageFont.truetype("arialbd.ttf", 55)  # Bold Arial
            font_small = ImageFont.truetype("arial.ttf", 35)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Clean professional title
        clean_title = title.replace('-', ' ').replace('_', ' ')
        words = clean_title.split()[:8]  # Allow more words for professional titles
        title_text = ' '.join(words).title()
        
        # Add professional title layout
        text_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Breaking news banner
        banner_text = "BREAKING NEWS"
        banner_bbox = text_draw.textbbox((0, 0), banner_text, font=font_small)
        banner_width = banner_bbox[2] - banner_bbox[0]
        banner_x = (width - banner_width) // 2
        
        # Red banner background
        text_draw.rectangle([banner_x - 20, 30, banner_x + banner_width + 20, 75], 
                          fill=(180, 20, 20, 220))
        text_draw.text((banner_x, 40), banner_text, font=font_small, fill=(255, 255, 255, 255))
        
        # Main title
        # Split title into multiple lines if too long
        max_chars_per_line = 25
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
        start_y = 150
        line_height = 65
        
        for i, line in enumerate(lines[:3]):  # Max 3 lines
            bbox = text_draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + (i * line_height)
            
            # Professional text shadow
            text_draw.text((x+2, y+2), line, font=font_large, fill=(0, 0, 0, 150))
            text_draw.text((x, y), line, font=font_large, fill=(255, 255, 255, 255))
        
        # Add timestamp
        timestamp = datetime.now().strftime("%B %d, %Y")
        time_bbox = text_draw.textbbox((0, 0), timestamp, font=font_small)
        time_width = time_bbox[2] - time_bbox[0]
        time_x = (width - time_width) // 2
        text_draw.text((time_x, height - 50), timestamp, font=font_small, fill=(255, 255, 255, 180))
        
        # Composite text
        img = Image.alpha_composite(img.convert('RGBA'), text_img).convert('RGB')
        
        return img

    def create_news_anchor_avatar(self, emotion):
        """Create professional news anchor representation (not cartoon)"""
        
        width, height = 300, 400
        avatar_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(avatar_img)
        
        # Create a professional silhouette instead of cartoon
        center_x, center_y = width // 2, height // 2
        
        # Professional business attire silhouette
        suit_color = (40, 40, 60, 200)  # Dark professional
        
        # Professional shoulder line
        draw.polygon([
            (center_x - 80, height - 20),
            (center_x - 60, center_y + 40),
            (center_x + 60, center_y + 40),
            (center_x + 80, height - 20)
        ], fill=suit_color)
        
        # Professional collar
        draw.polygon([
            (center_x - 30, center_y + 40),
            (center_x - 15, center_y + 20),
            (center_x + 15, center_y + 20),
            (center_x + 30, center_y + 40)
        ], fill=(255, 255, 255, 180))
        
        # Professional head outline
        head_color = (60, 60, 80, 150)
        draw.ellipse([center_x - 45, center_y - 80, center_x + 45, center_y + 10], 
                    fill=head_color)
        
        # Minimal professional details
        # Just a suggestion of professional appearance without cartoon features
        
        return avatar_img

    def generate_professional_reel(self, title, summary):
        """Generate ultra-professional news reel"""
        
        print(f"\n🎬 Creating professional news reel: {title}")
        
        try:
            # Create professional script
            category = self.categorize_news(title)
            script = self.create_professional_script(title, summary)
            
            print(f"📝 Professional script created ({len(script)} characters)")
            print(f"📋 Script preview: {script[:100]}...")
            
            # Generate professional audio with news anchor voice
            emotion = VoiceEmotion.CONFIDENT  # Always professional tone
            
            audio_file, metadata = self.audio_service.generate_emotional_voiceover(
                script=script,
                title=title,
                category=category,
                target_emotion=emotion
            )
            
            if not audio_file or not os.path.exists(audio_file):
                print("❌ Audio generation failed")
                return None
            
            print(f"🎵 Professional audio generated: {audio_file}")
            
            # Create broadcast-quality background
            background_img = self.create_broadcast_background(category, title)
            
            # Create professional avatar
            avatar_img = self.create_news_anchor_avatar(emotion)
            
            # Composite professional layout
            final_width, final_height = 1080, 1920
            final_img = background_img.copy()
            
            # Position avatar professionally (bottom right, like news broadcasts)
            avatar_x = final_width - 350
            avatar_y = final_height - 450
            
            # Resize avatar appropriately
            avatar_resized = avatar_img.resize((250, 320), Image.Resampling.LANCZOS)
            
            # Blend avatar with professional opacity
            final_img.paste(avatar_resized, (avatar_x, avatar_y), avatar_resized)
            
            # Save professional background
            bg_path = os.path.join("premium_reels", f"professional_bg_{title[:30]}.png")
            os.makedirs("premium_reels", exist_ok=True)
            final_img.save(bg_path)
            
            print(f"🎨 Professional background created: {bg_path}")
            
            # Create professional video
            output_path = os.path.join("premium_reels", f"professional_{title[:40]}.mp4")
            
            # Get audio duration
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                '-show_streams', audio_file
            ], capture_output=True, text=True)
            
            duration = 20  # Default fallback
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'audio':
                        duration = float(stream.get('duration', 20))
                        break
            
            # Create professional video with FFmpeg
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1', '-i', bg_path,
                '-i', audio_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-shortest',
                '-t', str(duration),
                '-pix_fmt', 'yuv420p',
                '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"✅ Professional news reel created successfully!")
                print(f"📁 File: {output_path}")
                print(f"💾 Size: {file_size:.1f} MB")
                print(f"⏱️ Duration: {duration:.1f} seconds")
                print(f"🎭 Category: {category.title()}")
                print(f"🎯 Professional quality achieved")
                
                # Cleanup temporary files
                try:
                    os.remove(bg_path)
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                except:
                    pass
                
                return output_path
            else:
                print(f"❌ Video creation failed: {result.stderr.decode()}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating professional reel: {str(e)}")
            return None

def main():
    """Test the ultra-professional generator"""
    generator = UltraProfessionalNewsGenerator()
    
    # Test with one of the existing news items
    test_title = "Scientists_Discover_Water_on_Mars_Moon"
    test_summary = "NASA researchers confirm discovery of water geysers on Jupiter's moon Europa, marking a significant breakthrough in the search for extraterrestrial life. The findings suggest subsurface oceans with conditions potentially suitable for life."
    
    result = generator.generate_professional_reel(test_title, test_summary)
    
    if result:
        print(f"\n🎉 Professional news reel generated: {result}")
    else:
        print("\n❌ Failed to generate professional reel")

if __name__ == "__main__":
    main()
