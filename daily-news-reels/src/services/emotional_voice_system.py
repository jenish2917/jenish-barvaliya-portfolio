"""
Emotional Voice System
Adds emotions, modulation, and human-like characteristics to TTS
"""

import os
import random
import re
from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass

class VoiceEmotion(Enum):
    """Voice emotions for different content types"""
    EXCITED = "excited"      # Tech breakthroughs, sports wins
    SURPRISED = "surprised"  # Unexpected news, shocking events
    CONCERNED = "concerned"  # Health issues, serious problems
    CONFIDENT = "confident"  # Business news, achievements
    PLAYFUL = "playful"      # Entertainment, light news
    DRAMATIC = "dramatic"    # Breaking news, major events
    SARCASTIC = "sarcastic"  # Controversial topics, irony
    WARM = "warm"           # Human interest, positive stories

@dataclass
class EmotionalVoiceProfile:
    """Profile for emotional voice generation"""
    emotion: VoiceEmotion
    speed_modifier: float    # 0.8 = slower, 1.2 = faster
    pitch_variation: float   # How much pitch varies
    pause_emphasis: bool     # Add dramatic pauses
    volume_dynamics: bool    # Vary volume for emphasis
    tone_descriptors: List[str]  # Words to describe the tone

class EmotionalVoiceSystem:
    """System to add emotions and human-like characteristics to voice"""
    
    def __init__(self):
        self.emotion_patterns = self._init_emotion_patterns()
        self.funny_transitions = self._init_funny_transitions()
        self.emotional_emphasis = self._init_emotional_emphasis()
        
    def _init_emotion_patterns(self) -> Dict[str, VoiceEmotion]:
        """Map content categories to appropriate emotions"""
        return {
            'technology': VoiceEmotion.EXCITED,
            'business': VoiceEmotion.CONFIDENT,
            'sports': VoiceEmotion.EXCITED,
            'entertainment': VoiceEmotion.PLAYFUL,
            'health': VoiceEmotion.CONCERNED,
            'science': VoiceEmotion.SURPRISED,
            'general': VoiceEmotion.DRAMATIC
        }
    
    def _init_funny_transitions(self) -> List[str]:
        """Funny transition phrases to make content more engaging"""
        return [
            "And here's where it gets interesting...",
            "Plot twist:",
            "But wait, there's more!",
            "Hold onto your coffee because...",
            "Meanwhile, in the real world...",
            "And then reality said 'hold my beer'...",
            "Cue the dramatic music because...",
            "In a shocking turn of events that surprised absolutely no one...",
            "Breaking: humans continue to be humans by...",
            "And in today's episode of 'You Can't Make This Up'...",
            "Somewhere, a screenwriter is taking notes because...",
            "Update from the department of 'Well, Obviously'...",
            "In news that will shock your grandparents but not you..."
        ]
    
    def _init_emotional_emphasis(self) -> Dict[VoiceEmotion, Dict]:
        """Define how each emotion should modify speech"""
        return {
            VoiceEmotion.EXCITED: {
                'speed_modifier': 1.15,
                'pitch_variation': 0.3,
                'pause_emphasis': True,
                'volume_dynamics': True,
                'emphasis_words': ['amazing', 'incredible', 'breakthrough', 'wow', 'fantastic'],
                'ssml_prosody': 'rate="fast" pitch="+10%" volume="loud"'
            },
            VoiceEmotion.SURPRISED: {
                'speed_modifier': 0.95,
                'pitch_variation': 0.4,
                'pause_emphasis': True,
                'volume_dynamics': True,
                'emphasis_words': ['shocking', 'unexpected', 'believe', 'surprising'],
                'ssml_prosody': 'rate="medium" pitch="+15%" volume="medium"'
            },
            VoiceEmotion.CONCERNED: {
                'speed_modifier': 0.9,
                'pitch_variation': 0.2,
                'pause_emphasis': True,
                'volume_dynamics': False,
                'emphasis_words': ['serious', 'important', 'concern', 'attention'],
                'ssml_prosody': 'rate="slow" pitch="-5%" volume="medium"'
            },
            VoiceEmotion.CONFIDENT: {
                'speed_modifier': 1.0,
                'pitch_variation': 0.15,
                'pause_emphasis': False,
                'volume_dynamics': True,
                'emphasis_words': ['success', 'achievement', 'growth', 'positive'],
                'ssml_prosody': 'rate="medium" pitch="0%" volume="loud"'
            },
            VoiceEmotion.PLAYFUL: {
                'speed_modifier': 1.1,
                'pitch_variation': 0.35,
                'pause_emphasis': True,
                'volume_dynamics': True,
                'emphasis_words': ['fun', 'hilarious', 'entertaining', 'wild'],
                'ssml_prosody': 'rate="fast" pitch="+20%" volume="loud"'
            },
            VoiceEmotion.DRAMATIC: {
                'speed_modifier': 0.85,
                'pitch_variation': 0.25,
                'pause_emphasis': True,
                'volume_dynamics': True,
                'emphasis_words': ['breaking', 'major', 'significant', 'urgent'],
                'ssml_prosody': 'rate="slow" pitch="+5%" volume="loud"'
            },
            VoiceEmotion.SARCASTIC: {
                'speed_modifier': 0.95,
                'pitch_variation': 0.3,
                'pause_emphasis': True,
                'volume_dynamics': True,
                'emphasis_words': ['obviously', 'surely', 'definitely', 'clearly'],
                'ssml_prosody': 'rate="medium" pitch="+8%" volume="medium"'
            },
            VoiceEmotion.WARM: {
                'speed_modifier': 0.95,
                'pitch_variation': 0.2,
                'pause_emphasis': False,
                'volume_dynamics': False,
                'emphasis_words': ['heartwarming', 'beautiful', 'touching', 'inspiring'],
                'ssml_prosody': 'rate="medium" pitch="-3%" volume="medium"'
            }
        }
    
    def select_emotion_for_content(self, category: str, title: str, content: str) -> VoiceEmotion:
        """Select appropriate emotion based on content analysis"""
        
        # Keyword-based emotion detection
        excitement_keywords = ['breakthrough', 'record', 'first time', 'achievement', 'victory', 'wins']
        surprise_keywords = ['shocking', 'unexpected', 'sudden', 'surprise', 'bizarre', 'weird']
        concern_keywords = ['crisis', 'problem', 'danger', 'warning', 'serious', 'concern']
        playful_keywords = ['funny', 'hilarious', 'amusing', 'entertaining', 'quirky', 'viral']
        dramatic_keywords = ['breaking', 'urgent', 'major', 'massive', 'huge', 'critical']
        
        text_to_analyze = f"{title} {content}".lower()
        
        # Check for specific emotional triggers
        if any(word in text_to_analyze for word in excitement_keywords):
            return VoiceEmotion.EXCITED
        elif any(word in text_to_analyze for word in surprise_keywords):
            return VoiceEmotion.SURPRISED
        elif any(word in text_to_analyze for word in concern_keywords):
            return VoiceEmotion.CONCERNED
        elif any(word in text_to_analyze for word in playful_keywords):
            return VoiceEmotion.PLAYFUL
        elif any(word in text_to_analyze for word in dramatic_keywords):
            return VoiceEmotion.DRAMATIC
        
        # Fall back to category-based emotion
        return self.emotion_patterns.get(category, VoiceEmotion.CONFIDENT)
    
    def add_emotional_markers(self, script: str, emotion: VoiceEmotion) -> str:
        """Add emotional emphasis markers to script for TTS processing"""
        
        emphasis_config = self.emotional_emphasis[emotion]
        emphasis_words = emphasis_config['emphasis_words']
        
        # Add emphasis to key words
        for word in emphasis_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            replacement = f'<emphasis level="strong">{word}</emphasis>'
            script = re.sub(pattern, replacement, script, flags=re.IGNORECASE)
        
        # Add dramatic pauses if needed
        if emphasis_config['pause_emphasis']:
            script = re.sub(r'([.!?])', r'\1<break time="0.5s"/>', script)
            script = re.sub(r'([,:])', r'\1<break time="0.3s"/>', script)
        
        # Wrap in prosody tags for emotion
        prosody = emphasis_config['ssml_prosody']
        script = f'<prosody {prosody}>{script}</prosody>'
        
        return script
    
    def get_voice_profile(self, category: str, title: str, content: str) -> EmotionalVoiceProfile:
        """Get complete emotional voice profile for content"""
        
        emotion = self.select_emotion_for_content(category, title, content)
        config = self.emotional_emphasis[emotion]
        
        return EmotionalVoiceProfile(
            emotion=emotion,
            speed_modifier=config['speed_modifier'],
            pitch_variation=config['pitch_variation'],
            pause_emphasis=config['pause_emphasis'],
            volume_dynamics=config['volume_dynamics'],
            tone_descriptors=[emotion.value, 'human-like', 'expressive']
        )
    
    def add_funny_transitions(self, script: str) -> str:
        """Add funny transition phrases to make script more entertaining"""
        
        sentences = script.split('. ')
        if len(sentences) < 2:
            return script
        
        # Add funny transition between sentences (randomly)
        if random.random() < 0.3:  # 30% chance
            transition = random.choice(self.funny_transitions)
            # Insert transition between first and second sentence
            sentences.insert(1, transition)
        
        return '. '.join(sentences)
    
    def enhance_script_personality(self, script: str, emotion: VoiceEmotion) -> str:
        """Add personality and human-like elements to script"""
        
        # Emotion-specific personality enhancements
        personality_enhancers = {
            VoiceEmotion.EXCITED: [
                lambda s: s.replace('This is', "Guys, this is absolutely"),
                lambda s: s.replace('announced', "just dropped the news that"),
                lambda s: s + " And honestly? We're here for it!"
            ],
            VoiceEmotion.PLAYFUL: [
                lambda s: s.replace('reported', "spilled the tea that"),
                lambda s: s.replace('said', "was like"),
                lambda s: s + " I mean, you can't write this stuff!"
            ],
            VoiceEmotion.SARCASTIC: [
                lambda s: s.replace('Unfortunately', "Shocking absolutely no one"),
                lambda s: s.replace('However', "But plot twist"),
                lambda s: s + " *insert surprised Pikachu face here*"
            ],
            VoiceEmotion.SURPRISED: [
                lambda s: s.replace('revealed', "wait for it... revealed"),
                lambda s: s.replace('announced', "dropped this bombshell:"),
                lambda s: s + " Did NOT see that coming!"
            ]
        }
        
        enhancers = personality_enhancers.get(emotion, [])
        
        for enhancer in enhancers:
            try:
                script = enhancer(script)
            except:
                continue  # Skip if enhancement fails
        
        return script
