"""
Enhanced Content Processor with Humor and Emotions
Creates engaging, funny, and emotionally-rich news scripts
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from dataclasses import dataclass
import time
from datetime import datetime
import json
import re
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add src to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.emotional_voice_system import EmotionalVoiceSystem, VoiceEmotion

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    import spacy
    from textstat import flesch_reading_ease, flesch_kincaid_grade
    QUALITY_ANALYSIS_AVAILABLE = True
except ImportError:
    QUALITY_ANALYSIS_AVAILABLE = False

load_dotenv('config.env')

@dataclass
class ProcessedContent:
    """Enhanced processed content with emotional metadata"""
    original_title: str
    original_content: str
    summary: str
    script: str
    keywords: List[str]
    sentiment: str
    estimated_duration: float
    quality_score: float
    humor_level: str
    emotion: str
    engagement_score: float
    personality_traits: List[str]

class EnhancedFunnyContentProcessor:
    """Enhanced content processor with humor, emotions, and engaging scripts"""
    
    def __init__(self):
        self.model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        self.host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.logger = self._setup_logger()
        
        # Quality thresholds - MUCH SHORTER for TikTok-style content
        self.min_summary_length = int(os.getenv('MIN_SUMMARY_LENGTH', '20'))
        self.max_summary_length = int(os.getenv('MAX_SUMMARY_LENGTH', '100'))
        self.min_script_length = int(os.getenv('MIN_SCRIPT_LENGTH', '30'))
        self.max_script_length = int(os.getenv('MAX_SCRIPT_LENGTH', '150'))
        self.quality_threshold = float(os.getenv('QUALITY_THRESHOLD', '70'))
        
        # Initialize emotional voice system
        self.emotional_voice = EmotionalVoiceSystem()
        
        # Humor and engagement elements
        self.humor_styles = self._init_humor_styles()
        self.engagement_hooks = self._init_engagement_hooks()
        self.personality_templates = self._init_personality_templates()
        
        # Threading lock for parallel processing
        self.processing_lock = threading.Lock()
        
        # Initialize quality analyzer if available
        self.quality_analyzer = None
        if QUALITY_ANALYSIS_AVAILABLE:
            try:
                self.quality_analyzer = spacy.load("en_core_web_sm")
                self.logger.info("Spacy model loaded successfully")
            except:
                self.logger.warning("Could not load spacy model")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('EnhancedContentProcessor')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _init_humor_styles(self) -> Dict[str, List[str]]:
        """Initialize different humor styles for different content types"""
        return {
            'technology': [
                "Welcome to another episode of 'Humans vs. Robots: Who's Winning?'",
                "In today's tech news, where science fiction becomes awkward reality...",
                "Breaking: Technology continues to make us all feel ancient...",
                "Your daily reminder that we're living in the future (sort of)..."
            ],
            'business': [
                "Money moves and corporate drama - it's like reality TV but with suits!",
                "In today's business news, where numbers go brrr and executives say things...",
                "Corporate world update: Someone made money, someone lost money, everyone's confused...",
                "Business news that's more dramatic than your favorite Netflix series..."
            ],
            'sports': [
                "Sports update where people run fast, jump high, and emotions run higher!",
                "Today in the world of athletic humans doing athletic things...",
                "Sports news: Where grown adults take games VERY seriously...",
                "Your dose of sports drama that's better than soap operas..."
            ],
            'entertainment': [
                "Celebrity news that's somehow both important and completely ridiculous...",
                "Entertainment update from the land of beautiful people doing beautiful things...",
                "Pop culture news that will definitely change your life (probably not)...",
                "Today's celebrity tea is piping hot and absolutely essential..."
            ],
            'health': [
                "Health news that will either make you paranoid or give you hope...",
                "Science discovers another thing about our weird human bodies...",
                "Health update: Your body is still a mystery, even to doctors...",
                "Today's health news brought to you by confused scientists..."
            ],
            'general': [
                "Breaking news from planet Earth, where humans continue to human...",
                "Today's news proves that reality is stranger than fiction...",
                "Current events that sound like someone's making them up...",
                "News update from the simulation we call reality..."
            ]
        }
    
    def _init_engagement_hooks(self) -> Dict[str, List[str]]:
        """Initialize engagement hooks for different emotions"""
        return {
            'excited': [
                "Okay, this is actually incredible!",
                "I'm not even kidding when I say this is mind-blowing...",
                "Hold up, because this just happened and it's HUGE:",
                "Plot twist of the century alert!"
            ],
            'surprised': [
                "Wait, what? Did this really just happen?",
                "I had to read this twice because... what?!",
                "Breaking: The universe just got a little weirder...",
                "File this under 'Things I didn't expect today'..."
            ],
            'playful': [
                "Buckle up, buttercup, because this story is wild!",
                "Today's dose of 'You can't make this stuff up'...",
                "Cue the dramatic music because this is peak human behavior:",
                "And the award for most unexpected news goes to..."
            ],
            'dramatic': [
                "This just in, and it's kind of a big deal:",
                "Breaking news that's about to change everything:",
                "Stop what you're doing because this just happened:",
                "Major alert that you need to know about right now:"
            ]
        }
    
    def _init_personality_templates(self) -> Dict[str, Dict]:
        """Initialize personality templates for different voice styles"""
        return {
            'gen_z_influencer': {
                'style_markers': ['bestie', 'literally', 'no cap', 'periodt', 'and that\'s on'],
                'transitions': ['But like', 'Also', 'Not gonna lie', 'Real talk'],
                'endings': ['And that\'s the tea!', 'We love to see it!', 'No notes!']
            },
            'millennial_friend': {
                'style_markers': ['honestly', 'basically', 'I mean', 'obviously', 'literally'],
                'transitions': ['So basically', 'Here\'s the thing', 'Plot twist', 'Meanwhile'],
                'endings': ['And honestly? We\'re here for it!', 'I mean... wow.', 'This is fine.']
            },
            'excited_newscaster': {
                'style_markers': ['folks', 'absolutely', 'incredible', 'amazing', 'fantastic'],
                'transitions': ['And here\'s where it gets good', 'But wait', 'And then', 'Now this'],
                'endings': ['What a time to be alive!', 'Stay tuned!', 'More at eleven!']
            },
            'sassy_commentator': {
                'style_markers': ['honey', 'darling', 'sweetie', 'bless their heart', 'imagine that'],
                'transitions': ['But here\'s the kicker', 'Oh, but wait', 'And surprise, surprise'],
                'endings': ['*sips tea*', 'Make it make sense!', 'I\'m just saying...']
            }
        }
    
    def process_article(self, title: str, content: str, country: str, category: str) -> Optional[ProcessedContent]:
        """Process article with enhanced humor and emotional intelligence"""
        
        try:
            start_time = time.time()
            
            # Select humor style and personality
            humor_style = self._select_humor_style(category, title, content)
            personality = self._select_personality(category, title, content)
            
            # Analyze emotional context
            emotion = self.emotional_voice.select_emotion_for_content(category, title, content)
            
            # Create enhanced summary
            summary = self._create_funny_summary(title, content, country, category, humor_style)
            if not summary:
                return None
            
            # Generate engaging script with personality
            script = self._generate_engaging_script(
                title, summary, country, category, 
                humor_style, personality, emotion
            )
            if not script:
                return None
            
            # Extract keywords and analyze sentiment
            keywords = self._extract_keywords(title, content)
            sentiment = self._analyze_enhanced_sentiment(title, content, script)
            
            # Calculate metrics
            estimated_duration = self._estimate_duration(script)
            quality_score = self._calculate_enhanced_quality_score(title, summary, script, content)
            engagement_score = self._calculate_engagement_score(script, emotion, humor_style)
            
            processing_time = time.time() - start_time
            
            processed_content = ProcessedContent(
                original_title=title,
                original_content=content,
                summary=summary,
                script=script,
                keywords=keywords,
                sentiment=sentiment,
                estimated_duration=estimated_duration,
                quality_score=quality_score,
                humor_level=humor_style,
                emotion=emotion.value,
                engagement_score=engagement_score,
                personality_traits=[personality, humor_style, emotion.value]
            )
            
            self.logger.info(f"Processed successfully - Quality: {quality_score:.1f}%, "
                           f"Engagement: {engagement_score:.1f}%, Duration: {estimated_duration:.1f}s")
            
            return processed_content
            
        except Exception as e:
            self.logger.error(f"Error processing article: {e}")
            return None
    
    def _select_humor_style(self, category: str, title: str, content: str) -> str:
        """Select appropriate humor style based on content"""
        
        # Analyze content for humor cues
        text_to_analyze = f"{title} {content}".lower()
        
        if any(word in text_to_analyze for word in ['funny', 'hilarious', 'joke', 'viral', 'meme']):
            return 'playful'
        elif any(word in text_to_analyze for word in ['breakthrough', 'innovation', 'tech', 'ai']):
            return 'tech_savvy'
        elif any(word in text_to_analyze for word in ['celebrity', 'star', 'famous', 'hollywood']):
            return 'pop_culture'
        elif any(word in text_to_analyze for word in ['business', 'money', 'corporate', 'market']):
            return 'business_casual'
        else:
            return 'witty_general'
    
    def _select_personality(self, category: str, title: str, content: str) -> str:
        """Select personality template based on content and target audience"""
        
        text = f"{title} {content}".lower()
        
        # Tech content -> Gen Z influencer
        if 'tech' in category or any(word in text for word in ['app', 'social', 'viral', 'trend']):
            return 'gen_z_influencer'
        
        # Entertainment -> Sassy commentator
        elif 'entertainment' in category or any(word in text for word in ['celebrity', 'drama', 'scandal']):
            return 'sassy_commentator'
        
        # Sports/excitement -> Excited newscaster
        elif 'sports' in category or any(word in text for word in ['win', 'victory', 'championship']):
            return 'excited_newscaster'
        
        # Default -> Millennial friend
        else:
            return 'millennial_friend'
    
    def _create_funny_summary(self, title: str, content: str, country: str, category: str, humor_style: str) -> Optional[str]:
        """Create an engaging summary with humor"""
        
        try:
            # If Ollama is not available, use a simple fallback
            if not OLLAMA_AVAILABLE:
                return self._create_fallback_summary(title, content, category)
            
            humor_prompts = self.humor_styles.get(category, self.humor_styles['general'])
            hook = random.choice(humor_prompts)
            
            prompt = f"""Create a SUPER SHORT summary. Maximum 80 characters total!

Title: {title}
Content: {content[:400]}

Rules:
- One sentence only
- Maximum 15 words
- Maximum 80 characters
- Casual, excited tone
- Include one key fact
- No boring words

Summary:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.6}  # Higher temperature for more creativity
            )
            
            summary = response['message']['content'].strip()
            summary = self._clean_text(summary)
            
            # Force shorter if still too long
            if len(summary) > self.max_summary_length:
                summary = summary[:self.max_summary_length].rsplit(' ', 1)[0] + '!'
            
            if len(summary) < self.min_summary_length or len(summary) > self.max_summary_length:
                self.logger.warning(f"Summary length out of range: {len(summary)} chars")
                return None
                
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creating funny summary: {e}")
            # Fallback to simple summary
            return self._create_fallback_summary(title, content, category)
    
    def _create_fallback_summary(self, title: str, content: str, category: str) -> str:
        """Create a simple engaging summary without Ollama"""
        
        # Extract key words from title
        key_words = [word for word in title.split() if len(word) > 3 and word.lower() not in ['with', 'from', 'that', 'this', 'they', 'have', 'will', 'been']][:3]
        
        # Category-based excitement words
        excitement_words = {
            'technology': ['OMG', 'Whoa', 'HUGE', 'Mind-blowing'],
            'science': ['Incredible', 'Amazing', 'Breakthrough'],
            'business': ['Major', 'Massive', 'Game-changer'],
            'world': ['Historic', 'Breaking', 'Huge'],
            'entertainment': ['Viral', 'Hilarious', 'Epic'],
            'sports': ['Insane', 'Record', 'Victory'],
            'health': ['Life-changing', 'Hope', 'Breakthrough']
        }
        
        excitement = random.choice(excitement_words.get(category, ['Breaking', 'Huge', 'Major']))
        
        if len(key_words) >= 2:
            summary = f"{excitement}: {key_words[0]} {key_words[1]} news!"
        elif len(key_words) == 1:
            summary = f"{excitement} {key_words[0]} update!"
        else:
            summary = f"{excitement} breaking news!"
        
        # Ensure it's within length limits
        if len(summary) > self.max_summary_length:
            summary = summary[:self.max_summary_length-1] + "!"
        
        return summary
    
    def _generate_engaging_script(self, title: str, summary: str, country: str, 
                                category: str, humor_style: str, personality: str, 
                                emotion: VoiceEmotion) -> Optional[str]:
        """Generate highly engaging script with personality and emotions"""
        
        try:
            # If Ollama is not available, use fallback
            if not OLLAMA_AVAILABLE:
                return self._create_fallback_script(title, summary, emotion, personality)
            
            personality_config = self.personality_templates[personality]
            engagement_hooks = self.engagement_hooks.get(emotion.value, self.engagement_hooks['excited'])
            
            hook = random.choice(engagement_hooks)
            style_markers = ', '.join(personality_config['style_markers'][:3])
            transitions = ', '.join(personality_config['transitions'][:2])
            ending_style = random.choice(personality_config['endings'])
            
            prompt = f"""Make this into a super short TikTok-style script. Think 10-15 seconds max!

Summary: {summary}
Emotion: {emotion.value}

Make it:
- 10-15 words ONLY
- Sound excited and fun  
- Use one simple hook
- Add one reaction word (OMG, Wait, Guys)
- End with excitement

Script:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7}  # High creativity for personality
            )
            
            script = response['message']['content'].strip()
            
            # Enhance with emotional voice system
            script = self.emotional_voice.add_funny_transitions(script)
            script = self.emotional_voice.enhance_script_personality(script, emotion)
            
            # Clean and validate
            script = self._clean_script(script)
            script = self._add_vocal_cues(script)
            
            # Force shorter if still too long
            if len(script) > self.max_script_length:
                script = script[:self.max_script_length].rsplit(' ', 1)[0] + '!'
            
            if len(script) < self.min_script_length or len(script) > self.max_script_length:
                self.logger.warning(f"Script length out of range: {len(script)} chars")
                return None
                
            return script
            
        except Exception as e:
            self.logger.error(f"Error generating engaging script: {e}")
            # Fallback to simple script
            return self._create_fallback_script(title, summary, emotion, personality)
    
    def _create_fallback_script(self, title: str, summary: str, emotion: VoiceEmotion, personality: str) -> str:
        """Create a simple engaging script without Ollama"""
        
        # Get reaction words based on emotion
        reaction_words = {
            'excited': ['OMG', 'Whoa', 'GUYS'],
            'surprised': ['Wait', 'What?!', 'No way'],
            'playful': ['LOL', 'Haha', 'Epic'],
            'dramatic': ['BREAKING', 'Alert', 'HUGE'],
            'confident': ['Facts', 'Listen up', 'Real talk'],
            'concerned': ['Yikes', 'Oh no', 'Alert'],
            'sarcastic': ['Really?', 'Sure...', 'Classic'],
            'warm': ['Aww', 'Sweet', 'Love this']
        }
        
        # Get ending words
        ending_words = {
            'excited': ['Amazing!', 'So cool!', 'Mind blown!'],
            'surprised': ['Crazy!', 'Unreal!', 'Wild!'],
            'playful': ['Epic win!', 'Love it!', 'So fun!'],
            'dramatic': ['Huge news!', 'Breaking!', 'Major!'],
            'confident': ['Facts!', 'Truth!', 'Exactly!'],
            'concerned': ['Yikes!', 'Scary!', 'Worrying!'],
            'sarcastic': ['Of course...', 'Typical!', 'Sure...'],
            'warm': ['So sweet!', 'Lovely!', 'Heartwarming!']
        }
        
        reaction = random.choice(reaction_words.get(emotion.value, reaction_words['excited']))
        ending = random.choice(ending_words.get(emotion.value, ending_words['excited']))
        
        # Create simple but engaging script
        script = f"{reaction} {summary} {ending}"
        
        # Ensure it's within length limits
        if len(script) > self.max_script_length:
            script = f"{reaction} {summary[:30]}! {ending}"
        
        if len(script) > self.max_script_length:
            script = f"{reaction} Breaking news! {ending}"
        
        return script
    
    def _add_vocal_cues(self, script: str) -> str:
        """Add vocal emphasis and pause cues for more human-like delivery"""
        
        # Add emphasis markers for TTS
        emphasis_patterns = [
            (r'\b(amazing|incredible|shocking|wow|unbelievable)\b', r'<emphasis level="strong">\1</emphasis>'),
            (r'\b(really|actually|literally|absolutely)\b', r'<emphasis level="moderate">\1</emphasis>'),
            (r'([.!?])\s+', r'\1 <break time="0.5s"/> '),  # Pauses after sentences
            (r'([,:])\s+', r'\1 <break time="0.3s"/> '),   # Shorter pauses
            (r'(\.\.\.)(\s*)', r'<break time="0.8s"/>\2'),  # Dramatic pauses
        ]
        
        for pattern, replacement in emphasis_patterns:
            script = re.sub(pattern, replacement, script, flags=re.IGNORECASE)
        
        return script
    
    def _calculate_engagement_score(self, script: str, emotion: VoiceEmotion, humor_style: str) -> float:
        """Calculate how engaging the script is"""
        
        score = 50.0  # Base score
        
        # Emotional words boost
        emotional_words = ['amazing', 'incredible', 'shocking', 'wow', 'love', 'hate', 'excited']
        emotion_count = sum(1 for word in emotional_words if word.lower() in script.lower())
        score += min(emotion_count * 5, 20)
        
        # Question marks engage audience
        question_count = script.count('?')
        score += min(question_count * 3, 10)
        
        # Direct address to audience
        you_count = script.lower().count('you')
        score += min(you_count * 2, 10)
        
        # Personality markers
        personality_markers = ['honestly', 'literally', 'basically', 'actually', 'I mean']
        personality_count = sum(1 for marker in personality_markers if marker.lower() in script.lower())
        score += min(personality_count * 3, 15)
        
        # Humor elements
        humor_markers = ['haha', 'lol', 'funny', 'hilarious', 'joke', 'ironic']
        humor_count = sum(1 for marker in humor_markers if marker.lower() in script.lower())
        score += min(humor_count * 4, 12)
        
        # Cap at 100
        return min(score, 100.0)
    
    def _calculate_enhanced_quality_score(self, title: str, summary: str, script: str, content: str) -> float:
        """Enhanced quality scoring including engagement factors"""
        
        score = 50.0  # Base score
        
        # Length appropriateness (30%)
        script_words = len(script.split())
        if 120 <= script_words <= 180:
            score += 30
        elif 100 <= script_words <= 200:
            score += 20
        else:
            score += 10
        
        # Readability (20%)
        if QUALITY_ANALYSIS_AVAILABLE:
            try:
                reading_ease = flesch_reading_ease(script)
                if reading_ease >= 70:  # Easy to read
                    score += 20
                elif reading_ease >= 50:
                    score += 15
                else:
                    score += 10
            except:
                score += 10
        else:
            score += 10
        
        # Content relevance (25%)
        title_words = set(title.lower().split())
        script_words = set(script.lower().split())
        overlap = len(title_words.intersection(script_words))
        relevance = min(overlap / max(len(title_words), 1) * 25, 25)
        score += relevance
        
        # Engagement factors (25%)
        engagement_score = self._calculate_engagement_score(script, VoiceEmotion.EXCITED, 'general')
        score += engagement_score * 0.25
        
        return min(score, 100.0)
    
    def _analyze_enhanced_sentiment(self, title: str, content: str, script: str) -> str:
        """Enhanced sentiment analysis including script tone"""
        
        # Combine all text for analysis
        full_text = f"{title} {content} {script}".lower()
        
        positive_words = ['good', 'great', 'amazing', 'excellent', 'success', 'win', 'breakthrough', 'achievement']
        negative_words = ['bad', 'terrible', 'crisis', 'problem', 'failure', 'loss', 'concern', 'danger']
        neutral_words = ['update', 'change', 'announcement', 'report', 'study', 'research']
        
        positive_count = sum(1 for word in positive_words if word in full_text)
        negative_count = sum(1 for word in negative_words if word in full_text)
        neutral_count = sum(1 for word in neutral_words if word in full_text)
        
        # Determine sentiment with humor bias (humor tends to be more positive)
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _clean_script(self, script: str) -> str:
        """Enhanced script cleaning"""
        if not script:
            return ""
        
        # Remove common unwanted phrases
        unwanted = ["Here's the script:", "Script:", "News script:", "Here is the"]
        for phrase in unwanted:
            script = script.replace(phrase, "")
        
        # Clean up multiple spaces and line breaks
        script = re.sub(r'\s+', ' ', script)
        script = script.strip()
        
        # Ensure proper punctuation
        if not script.endswith('.') and not script.endswith('!') and not script.endswith('?'):
            script += '!'
        
        return script
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove markdown and formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'```[^`]*```', '', text)
        
        # Clean up spacing
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def _extract_keywords(self, title: str, content: str) -> List[str]:
        """Extract keywords from content"""
        try:
            prompt = f"""Extract 5-8 relevant keywords from this news article. Focus on main topics, organizations, people, and key concepts.

Title: {title}
Content: {content[:800]}

Return only the keywords separated by commas, no explanations:"""

            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2}
            )
            
            keywords_text = response['message']['content'].strip()
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            
            return keywords[:8]  # Limit to 8 keywords
            
        except Exception as e:
            self.logger.error(f"Error extracting keywords: {e}")
            return []
    
    def _estimate_duration(self, script: str) -> float:
        """Estimate speech duration accounting for emotional delivery"""
        if not script:
            return 0.0
        
        word_count = len(script.split())
        
        # Account for emotional pauses and emphasis
        pause_count = script.count('...') + script.count('<break')
        emphasis_count = script.count('<emphasis')
        
        # Base rate: 150 words per minute (2.5 words per second)
        base_duration = word_count / 2.5
        
        # Add time for pauses and emphasis
        pause_time = pause_count * 0.5
        emphasis_time = emphasis_count * 0.2
        
        total_duration = base_duration + pause_time + emphasis_time
        
        return round(total_duration, 1)
    
    def process_batch(self, articles: List[Dict], max_workers: int = 4) -> List[ProcessedContent]:
        """Process multiple articles in parallel with enhanced features"""
        
        self.logger.info(f"🚀 Processing {len(articles)} articles in parallel with {max_workers} workers...")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all articles for processing
            future_to_article = {
                executor.submit(
                    self.process_article,
                    article['title'],
                    article['content'],
                    article.get('country', 'unknown'),
                    article.get('category', 'general')
                ): article for article in articles
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_article):
                article = future_to_article[future]
                try:
                    result = future.result()
                    if result and result.quality_score >= self.quality_threshold:
                        results.append(result)
                        self.logger.info(f"✅ Completed {len(results)}/{len(articles)} articles")
                    else:
                        self.logger.warning(f"Article failed quality check: {article['title'][:50]}...")
                except Exception as e:
                    self.logger.error(f"Error processing article: {e}")
        
        self.logger.info(f"🎉 Successfully processed {len(results)}/{len(articles)} articles in parallel")
        return results
