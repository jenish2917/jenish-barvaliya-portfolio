"""
Voice Gender & Avatar Matching System
Professional male/female voice selection with realistic avatar matching
"""

import os
import random
import logging
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import Enum
import json

class VoiceGender(Enum):
    MALE = "male"
    FEMALE = "female"
    RANDOM = "random"

class VoiceStyle(Enum):
    PROFESSIONAL = "professional"
    ENERGETIC = "energetic"
    AUTHORITATIVE = "authoritative"
    CASUAL = "casual"

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    gender: VoiceGender
    style: VoiceStyle
    tld: str  # For gTTS
    language: str
    speed: float
    pitch_shift: int
    avatar_style: str
    description: str

class VoiceGenderSystem:
    """Advanced voice gender and avatar matching system"""
    
    def __init__(self):
        self.logger = logging.getLogger('VoiceGenderSystem')
        
        # Define voice profiles for different genders and styles
        self.voice_profiles = {
            # Male voices - deeper, more authoritative
            'male_professional': VoiceProfile(
                gender=VoiceGender.MALE,
                style=VoiceStyle.PROFESSIONAL,
                tld='co.uk',  # British male accent - deeper, more authoritative
                language='en',
                speed=0.95,
                pitch_shift=-2,  # Lower pitch for male voice
                avatar_style='professional_male',
                description='Professional British male news anchor'
            ),
            'male_energetic': VoiceProfile(
                gender=VoiceGender.MALE,
                style=VoiceStyle.ENERGETIC,
                tld='com',  # American male accent - energetic
                language='en',
                speed=1.1,
                pitch_shift=-1,  # Slightly lower pitch
                avatar_style='energetic_male',
                description='Energetic American male presenter'
            ),
            'male_authoritative': VoiceProfile(
                gender=VoiceGender.MALE,
                style=VoiceStyle.AUTHORITATIVE,
                tld='co.uk',  # British authority
                language='en',
                speed=0.9,
                pitch_shift=-3,  # Much lower pitch for authority
                avatar_style='commanding_male',
                description='Authoritative British male anchor'
            ),
            'male_casual': VoiceProfile(
                gender=VoiceGender.MALE,
                style=VoiceStyle.CASUAL,
                tld='com.au',  # Australian casual male
                language='en',
                speed=1.05,
                pitch_shift=-1,
                avatar_style='casual_male',
                description='Casual Australian male presenter'
            ),
            
            # Female voices - higher pitch, different characteristics
            'female_professional': VoiceProfile(
                gender=VoiceGender.FEMALE,
                style=VoiceStyle.PROFESSIONAL,
                tld='com',  # American female professional
                language='en',
                speed=1.0,
                pitch_shift=0,  # Default pitch for female
                avatar_style='professional_female',
                description='Professional American female anchor'
            ),
            'female_energetic': VoiceProfile(
                gender=VoiceGender.FEMALE,
                style=VoiceStyle.ENERGETIC,
                tld='com',  # American female energetic
                language='en',
                speed=1.15,
                pitch_shift=1,  # Slightly higher pitch
                avatar_style='energetic_female',
                description='Energetic American female presenter'
            ),
            'female_authoritative': VoiceProfile(
                gender=VoiceGender.FEMALE,
                style=VoiceStyle.AUTHORITATIVE,
                tld='co.uk',  # British female authority
                language='en',
                speed=0.95,
                pitch_shift=0,  # Professional female pitch
                avatar_style='authoritative_female',
                description='Authoritative British female anchor'
            ),
            'female_casual': VoiceProfile(
                gender=VoiceGender.FEMALE,
                style=VoiceStyle.CASUAL,
                tld='com.au',  # Australian casual female
                language='en',
                speed=1.08,
                pitch_shift=1,
                avatar_style='casual_female',
                description='Casual Australian female presenter'
            )
        }
        
        # Category-based preferences for realistic presentation
        self.category_preferences = {
            'business': {
                'preferred_gender': [VoiceGender.MALE, VoiceGender.FEMALE],
                'preferred_style': VoiceStyle.PROFESSIONAL,
                'weight': {'male': 0.6, 'female': 0.4}  # Slightly prefer male for business
            },
            'technology': {
                'preferred_gender': [VoiceGender.MALE, VoiceGender.FEMALE],
                'preferred_style': VoiceStyle.ENERGETIC,
                'weight': {'male': 0.5, 'female': 0.5}  # Equal preference
            },
            'sports': {
                'preferred_gender': [VoiceGender.MALE, VoiceGender.FEMALE],
                'preferred_style': VoiceStyle.ENERGETIC,
                'weight': {'male': 0.7, 'female': 0.3}  # Prefer male for sports
            },
            'entertainment': {
                'preferred_gender': [VoiceGender.FEMALE, VoiceGender.MALE],
                'preferred_style': VoiceStyle.CASUAL,
                'weight': {'male': 0.4, 'female': 0.6}  # Prefer female for entertainment
            },
            'breaking_news': {
                'preferred_gender': [VoiceGender.MALE, VoiceGender.FEMALE],
                'preferred_style': VoiceStyle.AUTHORITATIVE,
                'weight': {'male': 0.8, 'female': 0.2}  # Strong male preference for authority
            },
            'health': {
                'preferred_gender': [VoiceGender.FEMALE, VoiceGender.MALE],
                'preferred_style': VoiceStyle.PROFESSIONAL,
                'weight': {'male': 0.3, 'female': 0.7}  # Prefer female for health
            },
            'science': {
                'preferred_gender': [VoiceGender.MALE, VoiceGender.FEMALE],
                'preferred_style': VoiceStyle.PROFESSIONAL,
                'weight': {'male': 0.6, 'female': 0.4}  # Slightly prefer male for science
            },
            'general': {
                'preferred_gender': [VoiceGender.MALE, VoiceGender.FEMALE],
                'preferred_style': VoiceStyle.PROFESSIONAL,
                'weight': {'male': 0.5, 'female': 0.5}  # Equal preference
            }
        }
        
        # Session state for consistency
        self.session_preferences = {}
        self.session_file = 'output/sessions/voice_session.json'
    
    def select_voice_profile(self, 
                           category: str = 'general',
                           preferred_gender: Optional[VoiceGender] = None,
                           preferred_style: Optional[VoiceStyle] = None,
                           session_consistency: bool = True) -> VoiceProfile:
        """
        Select optimal voice profile based on category and preferences
        
        Args:
            category: News category
            preferred_gender: Force specific gender
            preferred_style: Force specific style
            session_consistency: Maintain same gender/style within session
        
        Returns:
            VoiceProfile: Selected voice profile
        """
        
        # Load session preferences if needed
        if session_consistency:
            self._load_session_preferences()
        
        # Get category preferences
        cat_prefs = self.category_preferences.get(category, self.category_preferences['general'])
        
        # Determine gender
        if preferred_gender:
            selected_gender = preferred_gender
        elif session_consistency and 'gender' in self.session_preferences:
            selected_gender = VoiceGender(self.session_preferences['gender'])
        else:
            # Weighted random selection based on category
            weights = cat_prefs['weight']
            if random.random() < weights['male']:
                selected_gender = VoiceGender.MALE
            else:
                selected_gender = VoiceGender.FEMALE
        
        # Determine style
        if preferred_style:
            selected_style = preferred_style
        elif session_consistency and 'style' in self.session_preferences:
            selected_style = VoiceStyle(self.session_preferences['style'])
        else:
            selected_style = cat_prefs['preferred_style']
        
        # Find matching voice profile
        profile_key = f"{selected_gender.value}_{selected_style.value}"
        
        if profile_key not in self.voice_profiles:
            # Fallback to professional if specific style not found
            profile_key = f"{selected_gender.value}_professional"
        
        selected_profile = self.voice_profiles[profile_key]
        
        # Save to session if consistency enabled
        if session_consistency:
            self.session_preferences.update({
                'gender': selected_gender.value,
                'style': selected_style.value,
                'category': category
            })
            self._save_session_preferences()
        
        self.logger.info(f"🎤 Selected voice: {selected_profile.description}")
        self.logger.info(f"👤 Avatar style: {selected_profile.avatar_style}")
        
        return selected_profile
    
    def get_voice_settings_for_gtts(self, profile: VoiceProfile) -> Dict:
        """Convert voice profile to gTTS settings"""
        return {
            'language': profile.language,
            'tld': profile.tld,
            'slow': False,
            'voice_profile': profile
        }
    
    def get_avatar_settings(self, profile: VoiceProfile) -> Dict:
        """Get avatar configuration matching the voice"""
        avatar_configs = {
            'professional_male': {
                'gender': 'male',
                'age_range': (35, 50),
                'style': 'business_suit',
                'background': 'professional_studio',
                'expression': 'confident',
                'hair_style': 'professional',
                'skin_tone': 'medium'
            },
            'professional_female': {
                'gender': 'female',
                'age_range': (30, 45),
                'style': 'business_attire',
                'background': 'professional_studio',
                'expression': 'confident',
                'hair_style': 'professional',
                'skin_tone': 'medium'
            },
            'energetic_male': {
                'gender': 'male',
                'age_range': (25, 40),
                'style': 'smart_casual',
                'background': 'modern_studio',
                'expression': 'enthusiastic',
                'hair_style': 'modern',
                'skin_tone': 'medium'
            },
            'energetic_female': {
                'gender': 'female',
                'age_range': (25, 40),
                'style': 'smart_casual',
                'background': 'modern_studio',
                'expression': 'enthusiastic',
                'hair_style': 'modern',
                'skin_tone': 'medium'
            },
            'commanding_male': {
                'gender': 'male',
                'age_range': (40, 60),
                'style': 'formal_suit',
                'background': 'news_studio',
                'expression': 'authoritative',
                'hair_style': 'executive',
                'skin_tone': 'medium'
            },
            'authoritative_female': {
                'gender': 'female',
                'age_range': (35, 55),
                'style': 'formal_attire',
                'background': 'news_studio',
                'expression': 'authoritative',
                'hair_style': 'executive',
                'skin_tone': 'medium'
            }
        }
        
        return avatar_configs.get(profile.avatar_style, avatar_configs['professional_male'])
    
    def get_available_profiles(self) -> Dict[str, str]:
        """Get list of available voice profiles with descriptions"""
        return {key: profile.description for key, profile in self.voice_profiles.items()}
    
    def reset_session(self):
        """Reset session preferences"""
        self.session_preferences = {}
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
        self.logger.info("🔄 Voice session reset")
    
    def _load_session_preferences(self):
        """Load session preferences from file"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    self.session_preferences = json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load session preferences: {e}")
            self.session_preferences = {}
    
    def _save_session_preferences(self):
        """Save session preferences to file"""
        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(self.session_preferences, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save session preferences: {e}")
    
    def generate_session_report(self) -> Dict:
        """Generate report of voice selections in current session"""
        if not self.session_preferences:
            return {"status": "No session data available"}
        
        profile_key = f"{self.session_preferences.get('gender', 'unknown')}_{self.session_preferences.get('style', 'unknown')}"
        profile = self.voice_profiles.get(profile_key)
        
        return {
            "session_gender": self.session_preferences.get('gender'),
            "session_style": self.session_preferences.get('style'),
            "session_category": self.session_preferences.get('category'),
            "voice_description": profile.description if profile else "Unknown",
            "avatar_style": profile.avatar_style if profile else "Unknown",
            "voice_settings": {
                "tld": profile.tld if profile else "Unknown",
                "language": profile.language if profile else "Unknown",
                "speed": profile.speed if profile else "Unknown",
                "pitch_shift": profile.pitch_shift if profile else "Unknown"
            }
        }

def test_voice_gender_system():
    """Test the voice gender system"""
    print("🎤 Testing Voice Gender System...")
    
    system = VoiceGenderSystem()
    
    # Test different categories
    categories = ['business', 'technology', 'sports', 'entertainment', 'breaking_news']
    
    for category in categories:
        print(f"\n📂 Testing category: {category}")
        
        # Test male preference
        male_profile = system.select_voice_profile(
            category=category,
            preferred_gender=VoiceGender.MALE,
            session_consistency=False
        )
        print(f"   🚹 Male: {male_profile.description}")
        
        # Test female preference
        female_profile = system.select_voice_profile(
            category=category,
            preferred_gender=VoiceGender.FEMALE,
            session_consistency=False
        )
        print(f"   🚺 Female: {female_profile.description}")
        
        # Test automatic selection
        auto_profile = system.select_voice_profile(
            category=category,
            session_consistency=False
        )
        print(f"   🎯 Auto: {auto_profile.description}")
    
    # Test session consistency
    print(f"\n🔄 Testing session consistency...")
    system.reset_session()
    
    for i in range(3):
        profile = system.select_voice_profile(
            category='general',
            session_consistency=True
        )
        print(f"   Article {i+1}: {profile.description}")
    
    # Generate session report
    report = system.generate_session_report()
    print(f"\n📊 Session Report:")
    for key, value in report.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    test_voice_gender_system()
