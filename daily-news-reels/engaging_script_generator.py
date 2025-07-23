"""
Enhanced Script Generator for Engaging News Reels
Creates catchy, attention-grabbing scripts with hooks, emotions, and cliffhangers
"""

import os
import sys
import random
from typing import Dict, List, Optional
import logging
from datetime import datetime

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

class EngagingScriptGenerator:
    """Generates engaging, catchy news scripts that grab attention"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Attention-grabbing hooks
        self.hooks = [
            "🚨 BREAKING: ",
            "You won't believe what just happened... ",
            "This changes EVERYTHING: ",
            "SHOCKING: ",
            "Wait until you hear this... ",
            "The news everyone's talking about: ",
            "JUST IN: ",
            "This will blow your mind: ",
            "URGENT UPDATE: ",
            "Everyone needs to know this: "
        ]
        
        # Emotional transitions
        self.transitions = [
            "But here's the crazy part...",
            "And it gets even more interesting...",
            "Wait, there's more...",
            "But that's not all...",
            "Here's where it gets wild...",
            "The plot thickens...",
            "But here's the twist...",
            "And here's the kicker...",
            "This is where it gets insane...",
            "But wait for this..."
        ]
        
        # Engaging conclusions
        self.conclusions = [
            "What do you think about this? Drop your thoughts below!",
            "This is just the beginning... Stay tuned for more updates!",
            "Let me know if you want more news like this!",
            "Follow for more breaking news updates!",
            "This story is developing... Don't miss what happens next!",
            "Share this if you found it as shocking as I did!",
            "What's your take on this? Comment below!",
            "Hit that follow button for more exclusive news!",
            "This changes everything... What do you think?",
            "Keep watching for the latest updates on this story!"
        ]
        
        # Power words for impact
        self.power_words = [
            "shocking", "incredible", "unbelievable", "massive", "huge",
            "groundbreaking", "revolutionary", "game-changing", "explosive",
            "dramatic", "stunning", "remarkable", "extraordinary", "mind-blowing"
        ]
    
    def _setup_logger(self):
        logger = logging.getLogger('EngagingScriptGenerator')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def enhance_script(self, original_script: str, article_data: Dict) -> str:
        """Transform a boring script into an engaging one"""
        
        # Extract key elements
        title = article_data.get('title', '')
        category = article_data.get('category', 'general')
        
        # Choose appropriate hook based on category
        hook = self._select_hook(category, title)
        
        # Add emotional elements
        enhanced_script = self._add_emotional_elements(original_script)
        
        # Add transitions and power words
        enhanced_script = self._add_transitions(enhanced_script)
        
        # Add engaging conclusion
        conclusion = random.choice(self.conclusions)
        
        # Combine everything
        final_script = f"{hook}{enhanced_script} {conclusion}"
        
        # Add emphasis and pacing
        final_script = self._add_emphasis_and_pacing(final_script)
        
        self.logger.info(f"Enhanced script from {len(original_script)} to {len(final_script)} characters")
        
        return final_script
    
    def _select_hook(self, category: str, title: str) -> str:
        """Select appropriate hook based on content"""
        
        urgent_keywords = ['breaking', 'urgent', 'emergency', 'crisis', 'attack', 'died', 'killed']
        shocking_keywords = ['shocking', 'scandal', 'exposed', 'leaked', 'secret', 'hidden']
        business_keywords = ['stock', 'market', 'billion', 'million', 'deal', 'merger']
        
        title_lower = title.lower()
        
        if any(word in title_lower for word in urgent_keywords):
            return random.choice(["🚨 BREAKING: ", "URGENT UPDATE: ", "JUST IN: "])
        elif any(word in title_lower for word in shocking_keywords):
            return random.choice(["SHOCKING: ", "You won't believe what just happened... ", "This will blow your mind: "])
        elif category == 'business' or any(word in title_lower for word in business_keywords):
            return random.choice(["HUGE: ", "This changes EVERYTHING: ", "MASSIVE: "])
        else:
            return random.choice(self.hooks)
    
    def _add_emotional_elements(self, script: str) -> str:
        """Add emotional language and emphasis"""
        
        # Split into sentences
        sentences = script.split('. ')
        enhanced_sentences = []
        
        for i, sentence in enumerate(sentences):
            # Add power words occasionally
            if i > 0 and random.random() < 0.3:
                power_word = random.choice(self.power_words)
                sentence = f"This {power_word} development shows that {sentence.lower()}"
            
            # Add emphasis to numbers and key facts
            sentence = self._emphasize_key_facts(sentence)
            
            enhanced_sentences.append(sentence)
        
        return '. '.join(enhanced_sentences)
    
    def _emphasize_key_facts(self, sentence: str) -> str:
        """Add emphasis to important facts and numbers"""
        import re
        
        # Emphasize large numbers
        sentence = re.sub(r'\b(\d+)\s*(billion|million|thousand)\b', r'a MASSIVE \1 \2', sentence, flags=re.IGNORECASE)
        
        # Emphasize percentages
        sentence = re.sub(r'\b(\d+)%\b', r'a whopping \1%', sentence)
        
        # Emphasize company names and people
        # This is a simplified version - in practice, you'd use NER
        companies = ['Apple', 'Google', 'Microsoft', 'Amazon', 'Tesla', 'Meta', 'Netflix']
        for company in companies:
            sentence = sentence.replace(company, f"tech giant {company}")
        
        return sentence
    
    def _add_transitions(self, script: str) -> str:
        """Add engaging transitions between key points"""
        
        sentences = script.split('. ')
        if len(sentences) < 2:
            return script
        
        # Add transition after first sentence if script is long enough
        if len(sentences) >= 3:
            middle_index = len(sentences) // 2
            transition = random.choice(self.transitions)
            sentences[middle_index] = f"{transition} {sentences[middle_index]}"
        
        return '. '.join(sentences)
    
    def _add_emphasis_and_pacing(self, script: str) -> str:
        """Add emphasis marks and pacing for TTS"""
        
        # Add pauses for dramatic effect
        script = script.replace('...', '... <break time="0.8s"/>')
        script = script.replace('!', '! <break time="0.5s"/>')
        script = script.replace('?', '? <break time="0.4s"/>')
        
        # Add emphasis to key phrases
        emphasis_words = ['BREAKING', 'SHOCKING', 'HUGE', 'MASSIVE', 'URGENT']
        for word in emphasis_words:
            script = script.replace(word, f'<emphasis level="strong">{word}</emphasis>')
        
        # Add prosody for excitement
        script = f'<prosody rate="medium" pitch="+2st">{script}</prosody>'
        
        return script

def test_script_enhancement():
    """Test the script enhancement"""
    
    generator = EngagingScriptGenerator()
    
    # Test with a boring script
    boring_script = "Apple announced quarterly earnings today. The company reported revenue of 81 billion dollars. This represents a 5 percent increase from last year."
    
    article_data = {
        'title': 'Apple Reports Q4 Earnings',
        'category': 'business'
    }
    
    enhanced = generator.enhance_script(boring_script, article_data)
    
    print("🔴 BORING ORIGINAL:")
    print(boring_script)
    print("\n✅ ENHANCED VERSION:")
    print(enhanced)
    print(f"\nLength: {len(boring_script)} → {len(enhanced)} characters")

if __name__ == "__main__":
    test_script_enhancement()
