"""
Premium Voice Reel Generator
Creates high-quality, professional news reels with natural voice and engaging content
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.enhanced_funny_content_processor import EnhancedFunnyContentProcessor
from src.services.enhanced_emotional_audio_service_fixed import EnhancedEmotionalAudioService
from src.services.emotional_voice_system import VoiceEmotion
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import subprocess
import cv2
import numpy as np
from datetime import datetime
import random
import time

class PremiumVoiceReelGenerator:
    def __init__(self):
        self.content_processor = EnhancedFunnyContentProcessor()
        self.audio_service = EnhancedEmotionalAudioService()
        
        # Professional script templates for different categories
        self.premium_templates = {
            'technology': {
                'opener': [
                    "Breaking tech news that's changing everything!",
                    "The tech world just got shaken up!",
                    "This technology breakthrough will blow your mind!",
                    "Major tech announcement that affects everyone!"
                ],
                'style': 'confident and excited',
                'personality': 'tech_enthusiast'
            },
            'science': {
                'opener': [
                    "Scientists just made an incredible discovery!",
                    "This scientific breakthrough changes everything!",
                    "Amazing discovery that will shock you!",
                    "Researchers found something incredible!"
                ],
                'style': 'amazed and informative',
                'personality': 'science_expert'
            },
            'business': {
                'opener': [
                    "Market breaking news you need to know!",
                    "This financial move is making headlines!",
                    "Massive business announcement just dropped!",
                    "The markets are reacting to this huge news!"
                ],
                'style': 'professional and confident',
                'personality': 'business_analyst'
            },
            'health': {
                'opener': [
                    "Medical breakthrough bringing hope to millions!",
                    "Incredible health discovery that could save lives!",
                    "This medical advancement is revolutionary!",
                    "Life-changing health news you need to hear!"
                ],
                'style': 'hopeful and informative',
                'personality': 'health_expert'
            }
        }

    def create_premium_script(self, title, content, category):
        """Create professional, engaging script without confusing elements"""
        
        template = self.premium_templates.get(category, self.premium_templates['technology'])
        opener = random.choice(template['opener'])
        
        # Extract key facts without confusing symbols
        key_facts = []
        
        # Simple fact extraction
        sentences = content.split('.')[:3]
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and not any(symbol in sentence for symbol in ['$', '%', 'x', '>']):
                # Clean up the sentence
                clean_sentence = sentence.replace('billion', 'billion dollars')
                clean_sentence = clean_sentence.replace('million', 'million people')
                key_facts.append(clean_sentence)
        
        # Build clean, professional script
        script_parts = [
            opener,
            "",
            title.replace('-', ' '),
            ""
        ]
        
        # Add key facts in simple language
        if key_facts:
            script_parts.append("Here's what happened:")
            for fact in key_facts[:2]:  # Only top 2 facts
                script_parts.append(fact)
        
        # Add professional closing
        closings = [
            "This is huge news that will impact everyone!",
            "What do you think about this development?",
            "This changes everything in the industry!",
            "Amazing times we're living in!"
        ]
        
        script_parts.append("")
        script_parts.append(random.choice(closings))
        
        # Join and clean up
        full_script = ". ".join(script_parts)
        
        # Remove problematic elements
        full_script = full_script.replace("**", "")
        full_script = full_script.replace("📰", "")
        full_script = full_script.replace("🔍", "")
        full_script = full_script.replace("💥", "")
        full_script = full_script.replace("⏰", "")
        full_script = full_script.replace("🎯", "")
        full_script = full_script.replace("❓", "")
        full_script = full_script.replace("•", "")
        full_script = full_script.replace("  ", " ")
        
        # Remove mathematical symbols and confusing numbers
        full_script = full_script.replace("95%", "ninety five percent")
        full_script = full_script.replace("80%", "eighty percent")
        full_script = full_script.replace("1000x", "one thousand times")
        full_script = full_script.replace("$95,000", "ninety five thousand dollars")
        full_script = full_script.replace("$50 billion", "fifty billion dollars")
        
        return full_script

    def create_premium_background(self, category, title):
        """Create clean, professional background"""
        
        width, height = 1080, 1920
        
        # Professional color schemes
        color_schemes = {
            'technology': [(20, 50, 100), (40, 80, 160), (60, 120, 200)],  # Professional blue
            'science': [(30, 70, 50), (50, 120, 80), (70, 160, 110)],      # Scientific green
            'business': [(70, 30, 30), (120, 50, 50), (160, 70, 70)],      # Business red
            'health': [(50, 30, 70), (80, 50, 120), (110, 70, 160)]        # Medical purple
        }
        
        colors = color_schemes.get(category, color_schemes['technology'])
        
        # Create gradient background
        img = Image.new('RGB', (width, height), colors[0])
        draw = ImageDraw.Draw(img)
        
        # Smooth gradient
        for y in range(height):
            ratio = y / height
            if ratio < 0.5:
                ratio *= 2
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
            else:
                ratio = (ratio - 0.5) * 2
                r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ratio)
                g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ratio)
                b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ratio)
            
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add subtle professional pattern
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Simple geometric pattern
        for i in range(0, width, 150):
            for j in range(0, height, 150):
                overlay_draw.rectangle([i, j, i+100, j+3], fill=(255, 255, 255, 20))
                overlay_draw.rectangle([i, j, i+3, j+100], fill=(255, 255, 255, 20))
        
        # Blend overlay
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # Add clean title
        try:
            font_size = 60
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Clean title text
        clean_title = title.replace('-', ' ').replace('_', ' ')
        words = clean_title.split()[:6]  # Max 6 words
        title_text = ' '.join(words)
        
        # Add title with professional styling
        text_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Center the text
        bbox = text_draw.textbbox((0, 0), title_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = 300
        
        # Draw text with subtle shadow
        text_draw.text((x+2, y+2), title_text, font=font, fill=(0, 0, 0, 100))
        text_draw.text((x, y), title_text, font=font, fill=(255, 255, 255, 255))
        
        # Composite text
        img = Image.alpha_composite(img.convert('RGBA'), text_img).convert('RGB')
        
        return img

    def create_professional_avatar(self, emotion):
        """Create clean, professional avatar"""
        
        width, height = 200, 250
        avatar_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(avatar_img)
        
        center_x, center_y = width // 2, height // 2
        
        # Professional avatar colors
        skin_color = (255, 220, 177)
        suit_color = (50, 50, 100)
        
        # Head
        head_radius = 50
        draw.ellipse([center_x - head_radius, center_y - 60 - head_radius, 
                     center_x + head_radius, center_y - 60 + head_radius], 
                    fill=skin_color, outline=(0, 0, 0), width=2)
        
        # Professional expression
        if emotion.value == 'excited':
            # Confident smile
            draw.arc([center_x - 20, center_y - 75, center_x + 20, center_y - 55], 0, 180, fill=(0, 0, 0), width=3)
            # Bright eyes
            draw.ellipse([center_x - 20, center_y - 85, center_x - 10, center_y - 75], fill=(0, 0, 0))
            draw.ellipse([center_x + 10, center_y - 85, center_x + 20, center_y - 75], fill=(0, 0, 0))
        else:
            # Professional expression
            draw.line([(center_x - 15, center_y - 65), (center_x + 15, center_y - 65)], fill=(0, 0, 0), width=2)
            draw.ellipse([center_x - 20, center_y - 85, center_x - 10, center_y - 75], fill=(0, 0, 0))
            draw.ellipse([center_x + 10, center_y - 85, center_x + 20, center_y - 75], fill=(0, 0, 0))
        
        # Professional suit
        draw.rectangle([center_x - 40, center_y - 10, center_x + 40, center_y + 100], 
                      fill=suit_color, outline=(0, 0, 0), width=2)
        
        # Tie
        draw.polygon([(center_x, center_y - 10), (center_x - 8, center_y + 20), 
                     (center_x + 8, center_y + 20)], fill=(150, 0, 0))
        
        return avatar_img

    def generate_premium_audio(self, script, title, emotion):
        """Generate high-quality audio with professional voice"""
        
        print(f"🎵 Generating premium voice for: {title[:40]}...")
        
        # Use better voice settings for naturalness
        audio_path, metrics = self.audio_service.generate_emotional_voiceover(
            script,
            title,
            'technology',  # Use consistent category for better voice
            emotion
        )
        
        return audio_path, metrics

    def create_premium_video(self, background, avatar, audio_path, title, duration):
        """Create high-quality video"""
        
        try:
            # Create output directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_dir = "premium_reels"
            os.makedirs(video_dir, exist_ok=True)
            
            # Clean filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-')).strip()[:30]
            safe_title = safe_title.replace(' ', '_')
            video_filename = f"premium_reel_{safe_title}_{timestamp}.mp4"
            video_path = os.path.join(video_dir, video_filename)
            
            print(f"🎬 Creating premium video: {video_filename}")
            
            # Position avatar professionally
            bg_width, bg_height = background.size
            avatar_x = bg_width - avatar.width - 80  # Professional positioning
            avatar_y = bg_height // 2 + 200  # Lower position
            
            # Composite avatar
            final_frame = background.copy()
            final_frame.paste(avatar, (avatar_x, avatar_y), avatar)
            
            # Save frame
            temp_frame_path = os.path.join(video_dir, f"temp_frame_{timestamp}.png")
            final_frame.save(temp_frame_path)
            
            # Create video with FFmpeg
            cmd = [
                'ffmpeg', '-y',
                '-loop', '1',
                '-i', temp_frame_path,
                '-i', audio_path,
                '-c:v', 'libx264',
                '-tune', 'stillimage',
                '-c:a', 'aac',
                '-b:a', '256k',  # Higher audio quality
                '-pix_fmt', 'yuv420p',
                '-shortest',
                '-movflags', '+faststart',
                video_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Clean up
            os.remove(temp_frame_path)
            
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                print(f"✅ Premium video created: {video_path} ({file_size:,} bytes)")
                return video_path
            
        except Exception as e:
            print(f"❌ Error creating premium video: {e}")
            return None

    def create_premium_reel(self, title, content, category):
        """Create one premium quality reel"""
        
        try:
            print(f"🎬 Creating premium reel: {title[:50]}...")
            
            # Create premium script
            premium_script = self.create_premium_script(title, content, category)
            print(f"📝 Premium script created (clean and professional)")
            
            # Determine emotion
            emotion = VoiceEmotion.CONFIDENT if category == 'business' else VoiceEmotion.EXCITED
            
            # Generate premium audio
            audio_path, metrics = self.generate_premium_audio(premium_script, title, emotion)
            
            if not audio_path:
                print(f"❌ Audio generation failed")
                return None
            
            print(f"🎵 Premium audio generated: {metrics.duration:.1f}s")
            
            # Create premium visuals
            background = self.create_premium_background(category, title)
            avatar = self.create_professional_avatar(emotion)
            
            # Create premium video
            video_path = self.create_premium_video(
                background, avatar, audio_path, title, metrics.duration
            )
            
            if video_path:
                return {
                    'title': title,
                    'video_path': video_path,
                    'audio_path': audio_path,
                    'duration': metrics.duration,
                    'script': premium_script,
                    'quality': 'PREMIUM'
                }
                
        except Exception as e:
            print(f"❌ Error creating premium reel: {e}")
            return None

def main():
    print("🎥 CREATING PREMIUM QUALITY NEWS REELS")
    print("=" * 50)
    print("✅ Professional voice quality")
    print("✅ Clean, engaging scripts")
    print("✅ No confusing symbols or numbers")
    print("✅ Premium user experience")
    print()
    
    generator = PremiumVoiceReelGenerator()
    
    # Test with premium news
    premium_news = [
        {
            'title': 'AI Revolution: ChatGPT Breakthrough Changes Everything',
            'content': 'OpenAI announced a major breakthrough with their latest AI model that can think and reason like humans. The technology demonstrates incredible problem solving abilities and creative thinking. Companies are already seeing massive productivity improvements. This represents a turning point in artificial intelligence development.',
            'category': 'technology'
        },
        {
            'title': 'Scientists Discover Water on Mars Moon',
            'content': 'NASA scientists confirmed the discovery of liquid water beneath the surface of Mars moon. The finding dramatically increases chances of finding life beyond Earth. Researchers detected underground lakes using advanced radar technology. This discovery could change space exploration forever.',
            'category': 'science'
        },
        {
            'title': 'Tesla Stock Surges After Robotaxi Announcement',
            'content': 'Tesla shares jumped twenty five percent after announcing their fully autonomous taxi service. The company deployed thousands of self driving vehicles in major cities. Rides cost significantly less than traditional taxis. Wall Street analysts are calling it a game changer.',
            'category': 'business'
        }
    ]
    
    successful_reels = []
    
    for i, news in enumerate(premium_news, 1):
        print(f"🎬 Creating premium reel {i}/{len(premium_news)}")
        
        result = generator.create_premium_reel(
            news['title'],
            news['content'], 
            news['category']
        )
        
        if result:
            successful_reels.append(result)
            print(f"✅ Premium reel {i} completed!")
            print(f"   🎥 Video: {result['video_path']}")
            print(f"   ⏱️ Duration: {result['duration']:.1f}s")
            print()
        else:
            print(f"❌ Premium reel {i} failed")
    
    print("🎯 PREMIUM REEL GENERATION COMPLETE!")
    print(f"✅ {len(successful_reels)}/{len(premium_news)} premium reels created")
    print("🎉 Professional quality with natural voice!")
    print("📁 Premium reels saved to: premium_reels/")

if __name__ == "__main__":
    main()
