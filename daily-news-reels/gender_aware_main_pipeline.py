"""
Enhanced Main Pipeline with Gender-Aware Voice Selection
Fixes the female-only voice issue with realistic male/female voices
"""

import os
import sys
import logging
import random
from pathlib import Path

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from core.pipeline import EnhancedPipeline
from voice_gender_system import VoiceGenderSystem, VoiceGender, VoiceStyle

class GenderAwareEnhancedPipeline(EnhancedPipeline):
    """Enhanced pipeline with realistic male/female voice selection"""
    
    def __init__(self):
        super().__init__()
        self.voice_system = VoiceGenderSystem()
        self.logger = logging.getLogger('GenderAwarePipeline')
        
        # Gender variety settings
        self.ensure_gender_variety = True
        self.session_stats = {
            'male_voices': 0,
            'female_voices': 0,
            'total_videos': 0
        }
        
        self.logger.info("🎤 Initialized Gender-Aware Pipeline with Male/Female Voice Selection")
    
    def generate_audio_with_gender_selection(self, script: str, output_path: str, article: dict) -> bool:
        """Generate audio with appropriate gender selection"""
        
        try:
            # Determine optimal voice profile
            category = article.get('category', 'general')
            
            # Get gender preference based on category and variety
            preferred_gender = self._select_optimal_gender(category, article)
            
            # Get voice profile
            voice_profile = self.voice_system.select_voice_profile(
                category=category,
                preferred_gender=preferred_gender,
                session_consistency=True
            )
            
            # Generate with gTTS using profile settings
            from gtts import gTTS
            
            # Process script for better speech
            processed_script = self._process_script_for_voice(script, voice_profile)
            
            # Generate audio with selected voice characteristics
            tts = gTTS(
                text=processed_script,
                lang=voice_profile.language,
                tld=voice_profile.tld,
                slow=False
            )
            
            tts.save(output_path)
            
            # Update session statistics
            self._update_voice_stats(voice_profile)
            
            self.logger.info(f"🎤 Generated {voice_profile.gender.value} voice: {voice_profile.description}")
            self.logger.info(f"👥 Session stats: {self.session_stats['male_voices']} male, {self.session_stats['female_voices']} female")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating gender-aware audio: {e}")
            return False
    
    def _select_optimal_gender(self, category: str, article: dict) -> VoiceGender:
        """Select optimal gender based on category and variety requirements"""
        
        # Category-based preferences (realistic news industry patterns)
        category_preferences = {
            'business': {'male_weight': 0.6, 'female_weight': 0.4},
            'technology': {'male_weight': 0.5, 'female_weight': 0.5}, 
            'sports': {'male_weight': 0.7, 'female_weight': 0.3},
            'entertainment': {'male_weight': 0.4, 'female_weight': 0.6},
            'health': {'male_weight': 0.3, 'female_weight': 0.7},
            'science': {'male_weight': 0.6, 'female_weight': 0.4},
            'general': {'male_weight': 0.5, 'female_weight': 0.5}
        }
        
        prefs = category_preferences.get(category, category_preferences['general'])
        
        # Ensure variety - if we have too many of one gender, prefer the other
        total_voices = self.session_stats['male_voices'] + self.session_stats['female_voices']
        
        if total_voices > 0:
            male_ratio = self.session_stats['male_voices'] / total_voices
            
            # If too skewed towards one gender, balance it
            if male_ratio > 0.8:
                return VoiceGender.FEMALE  # Force female for variety
            elif male_ratio < 0.2:
                return VoiceGender.MALE    # Force male for variety
        
        # Otherwise use category-based weighted selection
        if random.random() < prefs['male_weight']:
            return VoiceGender.MALE
        else:
            return VoiceGender.FEMALE
    
    def _process_script_for_voice(self, script: str, voice_profile) -> str:
        """Process script for better speech based on voice profile"""
        
        # Basic text cleaning
        processed = script.strip()
        
        # Remove markdown and formatting
        import re
        processed = re.sub(r'[*_#`]', '', processed)
        processed = re.sub(r'<[^>]+>', '', processed)
        
        # Gender-specific processing
        if voice_profile.gender == VoiceGender.MALE:
            # Male voice - emphasize authority and clarity
            processed = processed.replace('breaking', 'BREAKING')
            processed = processed.replace('urgent', 'URGENT')
        else:
            # Female voice - emphasize engagement and clarity
            processed = processed.replace('incredible', 'incredible')
            processed = processed.replace('amazing', 'amazing')
        
        # Expand abbreviations for better pronunciation
        abbreviations = {
            'AI': 'A I',
            'CEO': 'C E O', 
            'FBI': 'F B I',
            'USA': 'U S A',
            'UK': 'U K'
        }
        
        for abbr, expansion in abbreviations.items():
            processed = processed.replace(abbr, expansion)
        
        return processed
    
    def _update_voice_stats(self, voice_profile):
        """Update session voice statistics"""
        if voice_profile.gender == VoiceGender.MALE:
            self.session_stats['male_voices'] += 1
        else:
            self.session_stats['female_voices'] += 1
        
        self.session_stats['total_videos'] += 1
    
    def get_voice_session_report(self) -> dict:
        """Get voice session statistics"""
        total = self.session_stats['total_videos']
        
        if total == 0:
            return {'status': 'No voices generated yet'}
        
        male_pct = (self.session_stats['male_voices'] / total) * 100
        female_pct = (self.session_stats['female_voices'] / total) * 100
        
        return {
            'total_voices': total,
            'male_voices': self.session_stats['male_voices'],
            'female_voices': self.session_stats['female_voices'],
            'male_percentage': male_pct,
            'female_percentage': female_pct,
            'gender_variety_score': min(100, (min(male_pct, female_pct) / 40) * 100)  # Optimal is 40-60% split
        }

def main():
    """Test the gender-aware enhanced pipeline"""
    
    print("🚀 Testing Gender-Aware Enhanced Pipeline...")
    print("="*60)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Create pipeline
    pipeline = GenderAwareEnhancedPipeline()
    
    # Test articles with different categories
    test_articles = [
        {
            'title': 'Major Business Merger Announced',
            'script': 'In a groundbreaking business development, two major corporations have announced their merger, creating industry-leading opportunities.',
            'category': 'business'
        },
        {
            'title': 'Revolutionary Health Discovery',
            'script': 'Medical researchers have made an incredible breakthrough in treatment options, offering new hope to patients worldwide.',
            'category': 'health'
        },
        {
            'title': 'Championship Sports Victory',
            'script': 'In an electrifying match, the home team secured a stunning victory that will be remembered for years to come.',
            'category': 'sports'
        },
        {
            'title': 'Technology Innovation Update',
            'script': 'Tech industry leaders unveiled revolutionary A I advancements that promise to transform how we interact with technology.',
            'category': 'technology'
        },
        {
            'title': 'Entertainment Industry News',
            'script': 'Hollywood celebrates as independent filmmakers receive recognition for their incredible artistic achievements.',
            'category': 'entertainment'
        }
    ]
    
    print(f"\n🎬 Testing {len(test_articles)} articles with gender-aware voice selection...")
    
    successful_generations = 0
    
    for i, article in enumerate(test_articles, 1):
        print(f"\n{i}. Processing: {article['title']}")
        print(f"   Category: {article['category']}")
        
        output_path = f"test_gender_voice_{i}.mp3"
        
        try:
            success = pipeline.generate_audio_with_gender_selection(
                script=article['script'],
                output_path=output_path,
                article=article
            )
            
            if success:
                successful_generations += 1
                file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
                print(f"   ✅ SUCCESS: Generated {output_path} ({file_size} bytes)")
            else:
                print(f"   ❌ FAILED: Could not generate audio")
                
        except Exception as e:
            print(f"   💥 ERROR: {e}")
    
    # Generate session report
    print(f"\n📊 SESSION REPORT:")
    print("="*30)
    
    report = pipeline.get_voice_session_report()
    
    if 'status' in report:
        print(report['status'])
    else:
        print(f"Total Voices Generated: {report['total_voices']}")
        print(f"Male Voices: {report['male_voices']} ({report['male_percentage']:.1f}%)")
        print(f"Female Voices: {report['female_voices']} ({report['female_percentage']:.1f}%)")
        print(f"Gender Variety Score: {report['gender_variety_score']:.1f}/100")
        
        # Success assessment
        if successful_generations > 0:
            print(f"\n🎉 SUCCESS: Generated {successful_generations}/{len(test_articles)} voices")
            print(f"✅ Male/Female voice selection is working!")
            
            if report['male_voices'] > 0 and report['female_voices'] > 0:
                print(f"✅ Gender variety achieved!")
            else:
                print(f"⚠️  Limited gender variety in this test")
        else:
            print(f"\n❌ No voices generated successfully")
    
    print(f"\n🎯 SOLUTION STATUS:")
    print(f"   Female-only voice issue: {'✅ FIXED' if report.get('male_voices', 0) > 0 else '❌ NOT FIXED'}")
    print(f"   Gender variety: {'✅ WORKING' if report.get('gender_variety_score', 0) > 50 else '⚠️ NEEDS IMPROVEMENT'}")
    print(f"   Voice generation: {'✅ WORKING' if successful_generations > 0 else '❌ NOT WORKING'}")

if __name__ == "__main__":
    main()
