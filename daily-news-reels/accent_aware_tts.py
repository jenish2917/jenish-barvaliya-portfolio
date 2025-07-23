"""
Accent-Aware TTS Generator
Dynamically adjusts accent, tone, and pronunciation based on content meaning and emotion
"""

import os
import sys
from gtts import gTTS
import pygame
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import tempfile
import logging
from typing import Dict, List, Optional, Tuple
import re
import random

class AccentAwareTTS:
    """Advanced TTS with dynamic accent and tone adjustments"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        
        # Accent mappings based on content type and emotion
        self.accent_profiles = {
            'breaking_news': {
                'primary_accent': 'com',      # American - authoritative
                'backup_accents': ['co.uk', 'com.au'],
                'speech_rate': 1.1,
                'pitch_variation': 'high',
                'emphasis_words': ['breaking', 'urgent', 'alert', 'developing']
            },
            'tech_news': {
                'primary_accent': 'com',      # American - tech industry standard
                'backup_accents': ['com.au', 'co.uk'],
                'speech_rate': 1.0,
                'pitch_variation': 'medium',
                'emphasis_words': ['revolutionary', 'breakthrough', 'innovation', 'AI', 'technology']
            },
            'business_news': {
                'primary_accent': 'co.uk',    # British - professional/financial
                'backup_accents': ['com', 'com.au'],
                'speech_rate': 0.95,
                'pitch_variation': 'low',
                'emphasis_words': ['billion', 'profit', 'market', 'financial', 'economic']
            },
            'entertainment': {
                'primary_accent': 'com',      # American - Hollywood standard
                'backup_accents': ['co.uk', 'com.au'],
                'speech_rate': 1.05,
                'pitch_variation': 'high',
                'emphasis_words': ['celebrity', 'movie', 'star', 'hollywood', 'exclusive']
            },
            'sports': {
                'primary_accent': 'com',      # American - sports commentary
                'backup_accents': ['co.uk', 'com.au'],
                'speech_rate': 1.15,
                'pitch_variation': 'very_high',
                'emphasis_words': ['goal', 'win', 'champion', 'record', 'victory']
            },
            'international': {
                'primary_accent': 'co.uk',    # British - BBC international style
                'backup_accents': ['com', 'com.au'],
                'speech_rate': 0.98,
                'pitch_variation': 'medium',
                'emphasis_words': ['global', 'international', 'world', 'nations']
            }
        }
        
        # Emotional tone adjustments
        self.emotion_modifiers = {
            'exciting': {
                'speed_multiplier': 1.1,
                'pitch_boost': 3,
                'volume_boost': 2,
                'accent_intensity': 'high'
            },
            'urgent': {
                'speed_multiplier': 1.15,
                'pitch_boost': 4,
                'volume_boost': 3,
                'accent_intensity': 'very_high'
            },
            'surprising': {
                'speed_multiplier': 0.9,   # Slower for dramatic effect
                'pitch_boost': 5,
                'volume_boost': 2,
                'accent_intensity': 'high'
            },
            'professional': {
                'speed_multiplier': 0.95,
                'pitch_boost': 1,
                'volume_boost': 1,
                'accent_intensity': 'medium'
            },
            'dramatic': {
                'speed_multiplier': 0.85,
                'pitch_boost': 6,
                'volume_boost': 4,
                'accent_intensity': 'very_high'
            }
        }
        
        # Word-specific pronunciation adjustments
        self.pronunciation_rules = {
            # Financial terms - more formal British pronunciation
            'billion': {'preferred_accent': 'co.uk', 'emphasis': 'strong'},
            'trillion': {'preferred_accent': 'co.uk', 'emphasis': 'strong'},
            'economic': {'preferred_accent': 'co.uk', 'emphasis': 'medium'},
            'financial': {'preferred_accent': 'co.uk', 'emphasis': 'medium'},
            
            # Tech terms - American pronunciation
            'AI': {'preferred_accent': 'com', 'emphasis': 'strong', 'expand_to': 'A I'},
            'startup': {'preferred_accent': 'com', 'emphasis': 'medium'},
            'silicon valley': {'preferred_accent': 'com', 'emphasis': 'medium'},
            
            # Dramatic words - enhanced emphasis regardless of accent
            'shocking': {'emphasis': 'very_strong', 'pause_after': '0.5s'},
            'incredible': {'emphasis': 'very_strong', 'pause_after': '0.3s'},
            'devastating': {'emphasis': 'very_strong', 'pause_after': '0.5s'},
            'revolutionary': {'emphasis': 'very_strong', 'pause_after': '0.3s'},
            
            # Names and places - specific accent preferences
            'london': {'preferred_accent': 'co.uk'},
            'new york': {'preferred_accent': 'com'},
            'sydney': {'preferred_accent': 'com.au'},
            'hollywood': {'preferred_accent': 'com'},
        }
        
        # Emotion detection patterns based on news content
        self.emotion_detection_patterns = {
            'urgent': {
                'keywords': ['breaking', 'urgent', 'alert', 'emergency', 'crisis', 'attack', 'disaster', 'crash', 'collapse'],
                'intensity': 'very_high',
                'voice_characteristics': {'speed': 1.2, 'pitch': 4, 'volume': 3}
            },
            'exciting': {
                'keywords': ['amazing', 'incredible', 'revolutionary', 'breakthrough', 'spectacular', 'fantastic', 'remarkable', 'extraordinary'],
                'intensity': 'high',
                'voice_characteristics': {'speed': 1.1, 'pitch': 3, 'volume': 2}
            },
            'shocking': {
                'keywords': ['shocking', 'stunned', 'unexpected', 'surprising', 'unbelievable', 'devastating', 'tragic', 'horrific'],
                'intensity': 'very_high',
                'voice_characteristics': {'speed': 0.9, 'pitch': 5, 'volume': 3}
            },
            'celebratory': {
                'keywords': ['wins', 'victory', 'champion', 'celebrates', 'triumph', 'success', 'achievement', 'record'],
                'intensity': 'high',
                'voice_characteristics': {'speed': 1.1, 'pitch': 3, 'volume': 2}
            },
            'concerned': {
                'keywords': ['worried', 'concerned', 'fears', 'threatens', 'risks', 'danger', 'warns', 'cautions'],
                'intensity': 'medium',
                'voice_characteristics': {'speed': 0.95, 'pitch': 1, 'volume': 1}
            },
            'mysterious': {
                'keywords': ['mysterious', 'unknown', 'unexplained', 'puzzling', 'bizarre', 'strange', 'peculiar'],
                'intensity': 'medium',
                'voice_characteristics': {'speed': 0.9, 'pitch': 2, 'volume': 1}
            },
            'hopeful': {
                'keywords': ['hope', 'optimistic', 'positive', 'promising', 'bright', 'improving', 'progress', 'recovery'],
                'intensity': 'medium',
                'voice_characteristics': {'speed': 1.0, 'pitch': 2, 'volume': 1}
            },
            'dramatic': {
                'keywords': ['drama', 'intense', 'explosive', 'confrontation', 'scandal', 'controversy', 'feud'],
                'intensity': 'high',
                'voice_characteristics': {'speed': 0.85, 'pitch': 4, 'volume': 3}
            }
        }
        
        # Sentiment intensity markers
        self.intensity_amplifiers = {
            'very': 1.5,
            'extremely': 2.0,
            'incredibly': 1.8,
            'absolutely': 1.7,
            'completely': 1.6,
            'totally': 1.5,
            'massive': 1.4,
            'huge': 1.3,
            'major': 1.2
        }
        
        # Geographic location detection and accent mapping
        self.location_accent_mapping = {
            # English-speaking countries with distinct accents
            'united_states': {
                'accent': 'com',
                'keywords': ['usa', 'united states', 'america', 'american', 'washington dc', 'new york', 'california', 'texas', 'florida', 'chicago', 'los angeles', 'boston', 'atlanta', 'miami', 'seattle', 'denver', 'las vegas', 'detroit', 'philadelphia'],
                'cities': ['new york', 'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia', 'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'fort worth', 'columbus', 'charlotte', 'san francisco', 'indianapolis', 'seattle', 'denver', 'washington', 'boston', 'el paso', 'detroit', 'nashville', 'portland', 'oklahoma city', 'las vegas', 'baltimore', 'louisville', 'milwaukee', 'albuquerque', 'tucson', 'fresno', 'sacramento', 'kansas city', 'mesa', 'atlanta', 'colorado springs', 'raleigh', 'omaha', 'miami', 'oakland', 'tulsa', 'minneapolis', 'cleveland', 'wichita', 'arlington', 'new orleans', 'bakersfield', 'tampa', 'honolulu', 'anaheim', 'aurora', 'santa ana', 'st. louis', 'riverside', 'corpus christi', 'lexington', 'pittsburgh', 'anchorage', 'stockton', 'cincinnati', 'st. paul', 'toledo', 'greensboro', 'newark', 'plano', 'henderson', 'lincoln', 'buffalo', 'jersey city', 'chula vista', 'fort wayne', 'orlando', 'st. petersburg', 'chandler', 'laredo', 'norfolk', 'durham', 'madison', 'lubbock', 'irvine', 'winston-salem', 'glendale', 'garland', 'hialeah', 'reno', 'chesapeake', 'gilbert', 'baton rouge', 'irving', 'scottsdale', 'north las vegas', 'fremont', 'boise', 'richmond', 'san bernardino', 'birmingham', 'spokane', 'rochester', 'des moines', 'modesto', 'fayetteville', 'tacoma', 'oxnard', 'fontana', 'columbus', 'montgomery', 'moreno valley', 'shreveport', 'aurora', 'yonkers', 'akron', 'huntington beach', 'little rock', 'augusta', 'amarillo', 'glendale', 'mobile', 'grand rapids', 'salt lake city', 'tallahassee', 'huntsville', 'grand prairie', 'knoxville', 'worcester', 'newport news', 'brownsville', 'overland park', 'santa clarita', 'providence', 'garden grove', 'chattanooga', 'oceanside', 'jackson', 'fort lauderdale', 'santa rosa', 'rancho cucamonga', 'port st. lucie', 'tempe', 'ontario', 'vancouver', 'cape coral', 'sioux falls', 'springfield', 'peoria', 'pembroke pines', 'elk grove', 'salem', 'lancaster', 'corona', 'eugene', 'palmdale', 'salinas', 'springfield', 'pasadena', 'fort collins', 'hayward', 'pomona', 'cary', 'rockford', 'alexandria', 'escondido', 'mckinney', 'kansas city', 'joliet', 'sunnyvale', 'torrance', 'bridgeport', 'lakewood', 'hollywood', 'paterson', 'naperville', 'syracuse', 'mesquite', 'dayton', 'savannah', 'clarksville', 'orange', 'pasadena', 'fullerton', 'killeen', 'frisco', 'hampton', 'mcallen', 'warren', 'west valley city', 'columbia', 'olathe', 'sterling heights', 'new haven', 'miramar', 'waco', 'thousand oaks', 'cedar rapids', 'charleston', 'sioux city', 'round rock', 'fargo', 'west jordan', 'pasadena', 'daly city', 'hialeah', 'pearland', 'richardson', 'lafayette', 'champaign', 'abilene', 'beaumont', 'murfreesboro', 'ann arbor', 'roseville', 'berkeley', 'norman', 'manchester', 'evansville', 'independence', 'lansing', 'concord', 'miami gardens', 'carlsbad', 'temecula', 'green bay', 'springfield', 'college station', 'carrollton', 'coral springs', 'westminster', 'costa mesa', 'boulder', 'west palm beach'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 1.0, 'pitch': 0, 'clarity': 'high'}
            },
            'united_kingdom': {
                'accent': 'co.uk',
                'keywords': ['uk', 'united kingdom', 'britain', 'british', 'england', 'scotland', 'wales', 'northern ireland', 'london', 'manchester', 'birmingham', 'liverpool', 'glasgow', 'edinburgh', 'cardiff', 'belfast', 'oxford', 'cambridge', 'bristol', 'leeds', 'sheffield', 'newcastle'],
                'cities': ['london', 'birmingham', 'manchester', 'glasgow', 'liverpool', 'edinburgh', 'leeds', 'sheffield', 'bristol', 'cardiff', 'belfast', 'newcastle', 'nottingham', 'southampton', 'plymouth', 'reading', 'bradford', 'bournemouth', 'norwich', 'swindon', 'swansea', 'wolverhampton', 'stoke-on-trent', 'derby', 'portsmouth', 'brighton', 'hull', 'middlesbrough', 'york', 'luton', 'stockport', 'coventry', 'blackpool', 'oxford', 'cambridge', 'bath', 'chester', 'worcester', 'carlisle', 'durham', 'exeter', 'gloucester', 'hereford', 'lancaster', 'lichfield', 'lincoln', 'peterborough', 'preston', 'ripon', 'salford', 'salisbury', 'truro', 'wakefield', 'wells', 'winchester', 'st albans', 'st davids', 'armagh', 'bangor', 'stirling', 'inverness', 'perth', 'dundee', 'aberdeen'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 0.95, 'pitch': 1, 'clarity': 'very_high'}
            },
            'australia': {
                'accent': 'com.au',
                'keywords': ['australia', 'australian', 'sydney', 'melbourne', 'brisbane', 'perth', 'adelaide', 'canberra', 'darwin', 'hobart', 'gold coast', 'newcastle', 'wollongong', 'geelong', 'townsville', 'cairns'],
                'cities': ['sydney', 'melbourne', 'brisbane', 'perth', 'adelaide', 'gold coast', 'newcastle', 'canberra', 'wollongong', 'geelong', 'hobart', 'townsville', 'cairns', 'toowoomba', 'darwin', 'launceston', 'albury', 'ballarat', 'bendigo', 'mandurah', 'mackay', 'rockhampton', 'bunbury', 'bundaberg', 'wagga wagga', 'hervey bay', 'mildura', 'shepparton', 'port macquarie', 'gladstone', 'tamworth', 'traralgon', 'orange', 'dubbo', 'geraldton', 'bowral', 'bathurst', 'nowra', 'warrnambool', 'kalgoorlie', 'devonport', 'mount gambier'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 1.05, 'pitch': 2, 'clarity': 'high'}
            },
            'canada': {
                'accent': 'ca',
                'keywords': ['canada', 'canadian', 'toronto', 'vancouver', 'montreal', 'calgary', 'ottawa', 'edmonton', 'mississauga', 'winnipeg', 'quebec city', 'hamilton', 'brampton', 'surrey', 'laval', 'halifax', 'london', 'markham', 'vaughan', 'gatineau'],
                'cities': ['toronto', 'montreal', 'vancouver', 'calgary', 'ottawa', 'edmonton', 'mississauga', 'winnipeg', 'quebec city', 'hamilton', 'brampton', 'kitchener', 'surrey', 'laval', 'halifax', 'london', 'markham', 'vaughan', 'longueuil', 'burnaby', 'saskatoon', 'regina', 'richmond', 'richmond hill', 'oakville', 'burlington', 'greater sudbury', 'sherbrooke', 'oshawa', 'saguenay', 'lévis', 'barrie', 'abbotsford', 'st. catharines', 'coquitlam', 'trois-rivières', 'guelph', 'cambridge', 'whitby', 'ajax', 'langley', 'saanich', 'terrebonne', 'milton', 'st. johns', 'moncton', 'thunder bay', 'dieppe', 'waterloo', 'delta', 'chatham-kent', 'red deer', 'kamloops', 'brantford', 'cape breton', 'lethbridge', 'saint-jean-sur-richelieu', 'clarington', 'pickering', 'nanaimo', 'sudbury', 'north vancouver', 'brossard', 'repentigny', 'newmarket', 'chilliwack', 'white rock', 'maple ridge', 'peterborough', 'kawartha lakes', 'prince george', 'sault ste. marie', 'sarnia', 'wood buffalo', 'new westminster', 'châteauguay', 'saint-jérôme', 'drummondville', 'saint-john', 'caledon', 'st. albert', 'granby', 'medicine hat', 'grande prairie', 'st. thomas', 'airdrie', 'halton hills', 'saint-hyacinthe', 'lac-brome', 'port coquitlam', 'fredericton', 'blainville', 'aurora', 'welland', 'north bay', 'beloeil', 'belleville', 'mirabel', 'shawinigan'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 0.98, 'pitch': 1, 'clarity': 'high'}
            },
            'india': {
                'accent': 'co.in',
                'keywords': ['india', 'indian', 'delhi', 'mumbai', 'bangalore', 'kolkata', 'chennai', 'hyderabad', 'pune', 'ahmedabad', 'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'patna', 'indore', 'thane', 'bhopal', 'visakhapatnam', 'pimpri-chinchwad', 'vadodara', 'ghaziabad', 'ludhiana', 'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'kalyan-dombivli', 'vasai-virar', 'varanasi', 'srinagar', 'aurangabad', 'dhanbad', 'amritsar', 'navi mumbai', 'allahabad', 'ranchi', 'howrah', 'coimbatore', 'jabalpur', 'gwalior', 'vijayawada', 'jodhpur', 'madurai', 'raipur', 'kota', 'guwahati', 'chandigarh', 'solapur', 'hubballi-dharwad', 'tiruchirappalli', 'bareilly', 'mysore', 'tiruppur', 'gurgaon', 'aligarh', 'jalandhar', 'bhubaneswar', 'salem', 'warangal', 'guntur', 'bhiwandi', 'saharanpur', 'gorakhpur', 'bikaner', 'amravati', 'noida', 'jamshedpur', 'bhilai', 'cuttack', 'firozabad', 'kochi', 'nellore', 'bhavnagar', 'dehradun', 'durgapur', 'asansol', 'rourkela', 'nanded', 'kolhapur', 'ajmer', 'akola', 'gulbarga', 'jamnagar', 'ujjain', 'loni', 'siliguri', 'jhansi', 'ulhasnagar', 'jammu', 'sangli-miraj & kupwad', 'mangalore', 'erode', 'belgaum', 'ambattur', 'tirunelveli', 'malegaon', 'gaya', 'jalgaon', 'udaipur', 'maheshtala'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 0.92, 'pitch': 2, 'clarity': 'medium'}
            },
            'south_africa': {
                'accent': 'co.za',
                'keywords': ['south africa', 'south african', 'johannesburg', 'cape town', 'durban', 'pretoria', 'port elizabeth', 'bloemfontein', 'kimberley', 'nelspruit', 'polokwane', 'rustenburg', 'pietermaritzburg', 'potchefstroom', 'welkom', 'klerksdorp', 'george', 'witbank', 'emalahleni', 'springs'],
                'cities': ['johannesburg', 'cape town', 'durban', 'pretoria', 'port elizabeth', 'pietermaritzburg', 'benoni', 'tembisa', 'east london', 'vereeniging', 'bloemfontein', 'boksburg', 'welkom', 'newcastle', 'krugersdorp', 'diepsloot', 'botshabelo', 'brakpan', 'witbank', 'richards bay', 'vanderbijlpark', 'centurion', 'uitenhage', 'roodepoort', 'paarl', 'springs', 'carletonville', 'klerksdorp', 'midrand', 'westonaria', 'middelburg', 'vryheid', 'orkney', 'kimberley', 'embalenhle', 'nigel', 'mpumalanga', 'bhisho', 'upington', 'potchefstroom', 'rustenburg', 'polokwane', 'nelspruit', 'mafikeng', 'lichtenburg', 'queenstown', 'ladysmith', 'phalaborwa', 'bethal', 'hermanus', 'knysna', 'oudtshoorn', 'worcester', 'stellenbosch', 'mossel bay'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 0.96, 'pitch': 1, 'clarity': 'high'}
            },
            'new_zealand': {
                'accent': 'co.nz',
                'keywords': ['new zealand', 'zealand', 'auckland', 'wellington', 'christchurch', 'hamilton', 'tauranga', 'napier-hastings', 'dunedin', 'palmerston north', 'nelson', 'rotorua', 'new plymouth', 'whangarei', 'invercargill', 'whanganui', 'gisborne'],
                'cities': ['auckland', 'wellington', 'christchurch', 'hamilton', 'tauranga', 'lower hutt', 'dunedin', 'palmerston north', 'hastings', 'napier', 'porirua', 'rotorua', 'new plymouth', 'whangarei', 'nelson', 'upper hutt', 'invercargill', 'whanganui', 'gisborne', 'kapiti', 'taupo', 'masterton', 'levin', 'timaru', 'oamaru', 'pukekohe', 'papakura', 'kerikeri', 'tokoroa', 'whakatane', 'kaitaia', 'dargaville', 'papatoetoe', 'te awamutu', 'cambridge', 'morrinsville', 'thames', 'whitianga', 'taumarunui', 'otorohanga', 'matamata', 'huntly', 'putaruru', 'mangakino', 'raglan', 'ngaruawahia', 'tuakau', 'waiuku', 'helensville', 'kumeu', 'snells beach'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 1.02, 'pitch': 2, 'clarity': 'high'}
            },
            'ireland': {
                'accent': 'ie',
                'keywords': ['ireland', 'irish', 'dublin', 'cork', 'limerick', 'galway', 'waterford'],
                'cities': ['dublin', 'cork', 'limerick', 'galway', 'waterford', 'drogheda', 'dundalk', 'swords', 'bray', 'navan', 'ennis', 'kilkenny', 'carlow', 'naas', 'athlone', 'portlaoise', 'mullingar', 'wexford', 'sligo', 'clonmel', 'letterkenny', 'celbridge', 'tralee', 'maynooth', 'wicklow', 'arklow', 'cobh', 'castlebar', 'midleton', 'ballina', 'enniscorthy', 'killarney', 'newbridge', 'mallow', 'blackrock', 'carrigaline', 'tullamore', 'kitty', 'shannon', 'longford', 'dungarvan', 'nenagh', 'trim', 'thurles', 'youghal', 'monaghan', 'buncrana', 'ballinasloe', 'fermoy', 'westport', 'carrick-on-suir', 'kells', 'birr', 'tipperary', 'kildare', 'leixlip', 'athy', 'laytown-bettystown-mornington', 'tuam', 'kilrush', 'callan', 'thomastown', 'bailieborough', 'boyle', 'bundoran', 'templemore', 'macroom', 'lismore', 'clonakilty', 'ballybay', 'roscrea', 'belturbet', 'moate', 'castleblayney', 'cavan', 'edgeworthstown', 'mitchelstown'],
                'language_code': 'en',
                'voice_characteristics': {'speed': 0.94, 'pitch': 3, 'clarity': 'high'}
            }
        }
        
        # Regional news source patterns
        self.news_source_mapping = {
            'com': ['cnn', 'fox', 'nbc', 'abc', 'cbs', 'usa today', 'new york times', 'washington post', 'wall street journal', 'bloomberg us', 'reuters us'],
            'co.uk': ['bbc', 'guardian', 'telegraph', 'times', 'independent', 'sky news', 'daily mail', 'financial times', 'reuters uk', 'bloomberg uk'],
            'com.au': ['abc australia', 'news.com.au', 'herald sun', 'sydney morning herald', 'australian', 'age', 'seven news', 'nine news', '10 news'],
            'co.in': ['times of india', 'hindustan times', 'indian express', 'ndtv', 'zee news', 'aaj tak', 'india today', 'deccan herald', 'economic times'],
            'ca': ['cbc', 'ctv', 'globe and mail', 'national post', 'toronto star', 'montreal gazette', 'vancouver sun', 'calgary herald'],
            'co.za': ['news24', 'iol', 'times live', 'sowetan', 'city press', 'mail & guardian', 'business day', 'fin24'],
            'co.nz': ['nz herald', 'stuff', 'newshub', 'tvnz', 'radio new zealand', 'otago daily times', 'dominion post'],
            'ie': ['rte', 'irish times', 'irish independent', 'irish examiner', 'thejournal.ie', 'breaking news', 'newstalk']
        }

        # Initialize pygame for audio processing
        try:
            pygame.mixer.init()
        except:
            self.logger.warning("Could not initialize pygame mixer")
    
    def _setup_logger(self):
        logger = logging.getLogger('AccentAwareTTS')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def generate_contextual_audio(self, 
                                text: str,
                                output_path: str,
                                category: str = 'general',
                                emotion: str = 'auto',
                                target_audience: str = 'international',
                                news_source: str = None) -> bool:
        """Generate audio with context-aware accent and tone"""
        
        try:
            # Auto-detect geographic location and corresponding accent
            detected_location, location_confidence = self._detect_geographic_location(text, news_source)
            self._last_location_confidence = location_confidence  # Store for later use
            
            # Auto-detect emotion from text content if not specified
            if emotion == 'auto':
                detected_emotion = self._detect_emotion_from_content(text)
                self.logger.info(f"🎭 Auto-detected emotion: {detected_emotion}")
                emotion = detected_emotion
            
            self.logger.info(f"🌍 Detected location: {detected_location} (confidence: {location_confidence:.2f})")
            self.logger.info(f"🎭 Generating contextual audio: {category} | {emotion} | {target_audience}")
            
            # Analyze text for optimal accent and tone
            accent_analysis = self._analyze_text_for_accent(text, category, emotion, detected_location)
            
            # Process text with pronunciation rules
            processed_text = self._apply_pronunciation_rules(text, accent_analysis)
            
            # Generate base audio with optimal accent
            temp_files = self._generate_layered_audio(processed_text, accent_analysis)
            
            if not temp_files:
                return False
            
            # Apply contextual enhancements
            enhanced_audio = self._apply_contextual_enhancements(
                temp_files, accent_analysis, emotion
            )
            
            # Save final audio
            enhanced_audio.export(output_path, format="wav")
            self.logger.info(f"🎵 Contextual audio saved: {output_path}")
            
            # Cleanup temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating contextual audio: {e}")
            return False
    
    def _detect_geographic_location(self, text: str, news_source: str = None) -> tuple:
        """Detect geographic location from news content and return appropriate accent"""
        
        text_lower = text.lower()
        location_scores = {}
        
        # Step 1: Check news source for regional hints
        if news_source:
            source_lower = news_source.lower()
            matches = []
            
            for accent, sources in self.news_source_mapping.items():
                for source in sources:
                    # Use exact match or check if source appears as whole words
                    if source == source_lower or f" {source} " in f" {source_lower} ":
                        matches.append((source, accent, len(source)))
            
            # Sort by length (longer matches are more specific)
            if matches:
                matches.sort(key=lambda x: x[2], reverse=True)
                best_source, best_accent, _ = matches[0]
                # High confidence if source is clearly regional
                return self._get_location_by_accent(best_accent), 0.9
        
        # Step 2: Analyze text content for geographic indicators
        for location, location_data in self.location_accent_mapping.items():
            score = 0
            
            # Check for direct country/region mentions
            for keyword in location_data['keywords']:
                if keyword in text_lower:
                    # Higher score for exact country matches
                    if keyword in ['usa', 'united states', 'america', 'uk', 'united kingdom', 'britain', 'australia', 'india', 'canada', 'south africa', 'new zealand', 'ireland']:
                        score += 50
                    else:
                        score += 20
            
            # Check for city mentions (if cities exist for this location)
            if 'cities' in location_data:
                for city in location_data['cities']:
                    if city in text_lower:
                        # Different scores based on city prominence
                        if city in ['new york', 'london', 'sydney', 'mumbai', 'toronto', 'johannesburg', 'auckland', 'dublin']:
                            score += 30  # Major cities get high score
                        else:
                            score += 15  # Other cities get moderate score
            
            location_scores[location] = score
        
        # Step 3: Find the most likely location
        if location_scores:
            best_location = max(location_scores, key=location_scores.get)
            max_score = location_scores[best_location]
            
            # Calculate confidence based on score
            confidence = min(max_score / 50.0, 1.0)  # Normalize to 0-1
            
            if confidence >= 0.3:  # Minimum confidence threshold
                self.logger.info(f"🌍 Location detected: {best_location} (score: {max_score}, confidence: {confidence:.2f})")
                return best_location, confidence
        
        # Step 4: Fallback analysis based on linguistic patterns
        fallback_location = self._analyze_linguistic_patterns(text_lower)
        self.logger.info(f"🌍 Fallback location detection: {fallback_location}")
        return fallback_location, 0.2  # Low confidence for fallback
    
    def _get_location_by_accent(self, accent: str) -> str:
        """Get location name by accent code"""
        accent_to_location = {
            'com': 'united_states',
            'co.uk': 'united_kingdom', 
            'com.au': 'australia',
            'co.in': 'india',
            'ca': 'canada',
            'co.za': 'south_africa',
            'co.nz': 'new_zealand',
            'ie': 'ireland'
        }
        return accent_to_location.get(accent, 'united_states')
    
    def _analyze_linguistic_patterns(self, text: str) -> str:
        """Analyze text for linguistic patterns that suggest origin"""
        
        # Check for spelling patterns
        british_spellings = ['colour', 'honour', 'favour', 'labour', 'centre', 'theatre', 'realise', 'organise', 'analyse']
        american_spellings = ['color', 'honor', 'favor', 'labor', 'center', 'theater', 'realize', 'organize', 'analyze']
        
        british_count = sum(1 for word in british_spellings if word in text)
        american_count = sum(1 for word in american_spellings if word in text)
        
        if british_count > american_count:
            return 'united_kingdom'
        elif american_count > british_count:
            return 'united_states'
        
        # Check for currency mentions
        if any(currency in text for currency in ['dollar', '$', 'usd']):
            # Could be US, Canada, Australia - check for other hints
            if any(word in text for word in ['federal reserve', 'wall street', 'nasdaq', 'dow jones']):
                return 'united_states'
            elif any(word in text for word in ['reserve bank of australia', 'asx']):
                return 'australia'
            elif any(word in text for word in ['bank of canada', 'tsx']):
                return 'canada'
            else:
                return 'united_states'  # Default to US for dollar
        
        if any(currency in text for currency in ['pound', '£', 'gbp', 'sterling']):
            return 'united_kingdom'
        
        if any(currency in text for currency in ['rupee', '₹', 'inr']):
            return 'india'
        
        if any(currency in text for currency in ['rand', 'zar']):
            return 'south_africa'
        
        if any(currency in text for currency in ['euro', '€', 'eur']):
            return 'ireland'  # Among English-speaking countries
        
        # Check for time zone mentions
        if any(tz in text for tz in ['est', 'pst', 'mst', 'cst', 'eastern time', 'pacific time']):
            return 'united_states'
        elif any(tz in text for tz in ['gmt', 'bst', 'greenwich']):
            return 'united_kingdom'
        elif any(tz in text for tz in ['aest', 'awst', 'acst']):
            return 'australia'
        elif any(tz in text for tz in ['ist', 'india standard time']):
            return 'india'
        
        # Default fallback based on global prevalence
        return 'united_states'
    
    def _detect_emotion_from_content(self, text: str) -> str:
        """Automatically detect emotion based on news content analysis"""
        
        text_lower = text.lower()
        emotion_scores = {}
        
        # Analyze each emotion pattern
        for emotion, pattern_data in self.emotion_detection_patterns.items():
            score = 0
            
            # Count keyword matches
            for keyword in pattern_data['keywords']:
                if keyword in text_lower:
                    base_score = 10
                    
                    # Check for intensity amplifiers
                    for amplifier, multiplier in self.intensity_amplifiers.items():
                        if f"{amplifier} {keyword}" in text_lower or f"{keyword} {amplifier}" in text_lower:
                            base_score *= multiplier
                            break
                    
                    score += base_score
            
            # Boost score based on pattern intensity
            if pattern_data['intensity'] == 'very_high':
                score *= 1.5
            elif pattern_data['intensity'] == 'high':
                score *= 1.2
            
            emotion_scores[emotion] = score
        
        # Find dominant emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[dominant_emotion]
            
            # Only return detected emotion if confidence is high enough
            if max_score >= 10:
                self.logger.info(f"🧠 Detected emotion '{dominant_emotion}' with score {max_score}")
                return dominant_emotion
        
        # Fallback: analyze sentence structure for emotion
        fallback_emotion = self._analyze_sentence_structure(text_lower)
        self.logger.info(f"🧠 Fallback emotion detection: {fallback_emotion}")
        return fallback_emotion
    
    def _analyze_sentence_structure(self, text: str) -> str:
        """Analyze sentence structure and punctuation for emotional cues"""
        
        # Check punctuation patterns
        if '!' in text:
            if text.count('!') >= 2:
                return 'exciting'  # Multiple exclamations = excitement
            else:
                return 'urgent'    # Single exclamation = urgency
        
        if '?' in text and ('how' in text or 'why' in text or 'what' in text):
            return 'mysterious'    # Questions suggest mystery/curiosity
        
        # Check for ALL CAPS (indicates emphasis/urgency)
        caps_words = [word for word in text.split() if word.isupper() and len(word) > 2]
        if len(caps_words) >= 2:
            return 'urgent'
        
        # Check for numbers/statistics (business-like)
        if any(char.isdigit() for char in text):
            if any(word in text for word in ['billion', 'million', 'percent', '%', 'profit', 'loss']):
                return 'concerned'  # Financial numbers often indicate concern
        
        # Check sentence length and complexity
        sentences = text.split('.')
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        
        if avg_length > 20:
            return 'professional'  # Long sentences = formal/professional
        elif avg_length < 8:
            return 'urgent'        # Short sentences = urgency
        
        return 'professional'  # Default fallback
    
    def _analyze_text_for_accent(self, text: str, category: str, emotion: str, detected_location: str = None) -> Dict:
        """Analyze text to determine optimal accent and tone settings"""
        
        text_lower = text.lower()
        
        # Step 1: Use detected geographic location for accent selection
        if detected_location and detected_location in self.location_accent_mapping:
            location_data = self.location_accent_mapping[detected_location]
            primary_accent = location_data['accent']
            backup_accents = ['com', 'co.uk', 'com.au']  # Common fallbacks
            
            # Remove primary accent from backups to avoid duplication
            backup_accents = [acc for acc in backup_accents if acc != primary_accent]
            
            self.logger.info(f"🗣️ Using {detected_location} accent: {primary_accent}")
        else:
            # Step 2: Fallback to category-based accent selection
            profile = self.accent_profiles.get(category, self.accent_profiles['tech_news'])
            primary_accent = profile['primary_accent']
            backup_accents = profile['backup_accents']
        
        # Step 3: Override accent based on content analysis (secondary)
        # Detect international context
        international_keywords = ['global', 'international', 'world', 'nations', 'countries']
        if any(keyword in text_lower for keyword in international_keywords):
            if not detected_location:  # Only override if location wasn't detected
                primary_accent = 'co.uk'  # BBC international style
        
        # Detect business/financial context
        financial_keywords = ['billion', 'trillion', 'market', 'economic', 'financial', 'profit']
        if any(keyword in text_lower for keyword in financial_keywords):
            if not detected_location and primary_accent not in ['co.uk', 'co.in']:
                # Use British for financial authority, unless location suggests otherwise
                if 'wall street' in text_lower or 'nasdaq' in text_lower:
                    primary_accent = 'com'  # American for US financial markets
                else:
                    primary_accent = 'co.uk'  # British for general financial news
        
        # Detect urgency/breaking news
        urgent_keywords = ['breaking', 'urgent', 'alert', 'developing', 'just in']
        if any(keyword in text_lower for keyword in urgent_keywords):
            # Use local accent for breaking news (more relatable)
            if not detected_location:
                primary_accent = 'com'  # Default to American for global reach
        
        # Step 4: Get base profile for other settings
        profile = self.accent_profiles.get(category, self.accent_profiles['tech_news'])
        
        # Step 5: Analyze emotional content and adjust accordingly
        detected_emotion_data = self.emotion_detection_patterns.get(emotion)
        if detected_emotion_data:
            # Override emotion modifier with detected emotion characteristics
            emotion_modifier = {
                'speed_multiplier': detected_emotion_data['voice_characteristics']['speed'],
                'pitch_boost': detected_emotion_data['voice_characteristics']['pitch'],
                'volume_boost': detected_emotion_data['voice_characteristics']['volume'],
                'accent_intensity': detected_emotion_data['intensity']
            }
        else:
            # Use default emotion modifier
            emotion_modifier = self.emotion_modifiers.get(emotion, self.emotion_modifiers['professional'])
        
        # Step 6: Apply location-specific voice characteristics if available
        if detected_location and detected_location in self.location_accent_mapping:
            location_voice_data = self.location_accent_mapping[detected_location]['voice_characteristics']
            
            # Blend location characteristics with emotion
            emotion_modifier['speed_multiplier'] *= location_voice_data['speed']
            emotion_modifier['pitch_boost'] += location_voice_data['pitch']
            
            # Adjust clarity for accent
            if location_voice_data['clarity'] == 'very_high':
                emotion_modifier['accent_intensity'] = 'high'
            elif location_voice_data['clarity'] == 'medium':
                emotion_modifier['accent_intensity'] = 'medium'
        
        # Find emphasis words in text
        emphasis_words = []
        for word in profile['emphasis_words']:
            if word.lower() in text_lower:
                emphasis_words.append(word)
        
        # Check for special pronunciation rules
        special_pronunciations = []
        for word, rules in self.pronunciation_rules.items():
            if word.lower() in text_lower:
                special_pronunciations.append((word, rules))
        
        return {
            'primary_accent': primary_accent,
            'backup_accents': backup_accents,
            'speech_rate': profile['speech_rate'] * emotion_modifier['speed_multiplier'],
            'pitch_variation': profile['pitch_variation'],
            'emphasis_words': emphasis_words,
            'special_pronunciations': special_pronunciations,
            'emotion_modifier': emotion_modifier,
            'detected_emotion': emotion,
            'detected_location': detected_location,
            'location_confidence': getattr(self, '_last_location_confidence', 0.0)
        }
    
    def _apply_pronunciation_rules(self, text: str, accent_analysis: Dict) -> str:
        """Apply pronunciation rules and emphasis markers"""
        
        processed_text = text
        
        # Apply emotional emphasis based on detected patterns
        emotion = accent_analysis.get('detected_emotion', 'professional')
        if emotion in self.emotion_detection_patterns:
            emotion_data = self.emotion_detection_patterns[emotion]
            
            # Add extra emphasis to emotion-specific keywords
            for keyword in emotion_data['keywords']:
                if keyword.lower() in processed_text.lower():
                    pattern = rf'\\b{re.escape(keyword)}\\b'
                    
                    # Apply different emphasis styles based on emotion
                    if emotion in ['urgent', 'shocking']:
                        replacement = f"{keyword.upper()}!!!"  # Very strong emphasis
                    elif emotion in ['exciting', 'celebratory']:
                        replacement = f"{keyword.upper()}!"   # Strong emphasis
                    else:
                        replacement = f"{keyword.upper()}"    # Moderate emphasis
                    
                    processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
        
        # Apply special pronunciations
        for word, rules in accent_analysis['special_pronunciations']:
            if 'expand_to' in rules:
                # Replace abbreviations with expanded form
                pattern = rf'\\b{re.escape(word)}\\b'
                processed_text = re.sub(pattern, rules['expand_to'], processed_text, flags=re.IGNORECASE)
            
            if 'pause_after' in rules:
                # Add pauses after dramatic words
                pattern = rf'\\b{re.escape(word)}\\b'
                replacement = f"{word}..."  # gTTS will interpret ... as a pause
                processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
        
        # Add emphasis to key words
        for emphasis_word in accent_analysis['emphasis_words']:
            # Make emphasis words uppercase for gTTS emphasis
            if emphasis_word.lower() in processed_text.lower():
                pattern = rf'\\b{re.escape(emphasis_word)}\\b'
                processed_text = re.sub(pattern, emphasis_word.upper(), processed_text, flags=re.IGNORECASE)
        
        # Clean up any TTS markup that gTTS doesn't support
        processed_text = re.sub(r'<[^>]+>', '', processed_text)
        
        # Add emotional pauses based on detected emotion
        if emotion in ['shocking', 'dramatic', 'mysterious']:
            processed_text = processed_text.replace('!', '!...')
            processed_text = processed_text.replace('?', '?...')
        elif emotion in ['urgent', 'exciting']:
            processed_text = processed_text.replace('!', '!')  # Keep urgency without long pauses
        
        return processed_text
    
    def _generate_layered_audio(self, text: str, accent_analysis: Dict) -> List[str]:
        """Generate multiple audio layers with different accents for blending"""
        
        temp_files = []
        accents_to_try = [accent_analysis['primary_accent']] + accent_analysis['backup_accents']
        
        # Split text into segments for varied accent treatment
        segments = self._split_text_by_importance(text, accent_analysis)
        
        for i, (segment_text, segment_accent) in enumerate(segments):
            try:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_segment_{i}.mp3')
                temp_path = temp_file.name
                temp_file.close()
                
                # Choose best accent for this segment
                accent = segment_accent if segment_accent in accents_to_try else accent_analysis['primary_accent']
                
                tts = gTTS(
                    text=segment_text,
                    lang='en',
                    tld=accent,
                    slow=False
                )
                
                tts.save(temp_path)
                temp_files.append(temp_path)
                
                self.logger.info(f"✅ Generated segment {i+1} with {accent} accent")
                
            except Exception as e:
                self.logger.warning(f"Failed to generate segment {i+1} with accent {accent}: {e}")
                # Try fallback accent
                if accent_analysis['backup_accents']:
                    try:
                        fallback_accent = accent_analysis['backup_accents'][0]
                        tts = gTTS(text=segment_text, lang='en', tld=fallback_accent, slow=False)
                        tts.save(temp_path)
                        temp_files.append(temp_path)
                        self.logger.info(f"✅ Generated segment {i+1} with fallback {fallback_accent} accent")
                    except:
                        self.logger.error(f"Failed to generate segment {i+1} even with fallback")
        
        return temp_files
    
    def _split_text_by_importance(self, text: str, accent_analysis: Dict) -> List[Tuple[str, str]]:
        """Split text into segments with appropriate accent choices"""
        
        segments = []
        primary_accent = accent_analysis['primary_accent']
        
        # Split by sentences for now (could be enhanced to split by phrases)
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Determine best accent for this sentence
            sentence_accent = primary_accent
            
            # Check for words that prefer specific accents
            for word, rules in accent_analysis['special_pronunciations']:
                if word.lower() in sentence.lower() and 'preferred_accent' in rules:
                    sentence_accent = rules['preferred_accent']
                    break
            
            segments.append((sentence + '.', sentence_accent))
        
        return segments
    
    def _apply_contextual_enhancements(self, temp_files: List[str], accent_analysis: Dict, emotion: str) -> AudioSegment:
        """Apply contextual audio enhancements based on analysis"""
        
        if not temp_files:
            raise ValueError("No audio files to process")
        
        # Combine segments
        combined_audio = None
        for temp_file in temp_files:
            try:
                segment = AudioSegment.from_mp3(temp_file)
                
                if combined_audio is None:
                    combined_audio = segment
                else:
                    # Add small gap between segments
                    gap = AudioSegment.silent(duration=100)  # 100ms gap
                    combined_audio = combined_audio + gap + segment
                    
            except Exception as e:
                self.logger.warning(f"Error processing segment {temp_file}: {e}")
        
        if combined_audio is None:
            raise ValueError("Failed to combine audio segments")
        
        # Apply speed adjustment
        if accent_analysis['speech_rate'] != 1.0:
            combined_audio = combined_audio.speedup(playback_speed=accent_analysis['speech_rate'])
        
        # Apply emotional enhancements
        emotion_mod = accent_analysis['emotion_modifier']
        
        # Volume boost for emotion
        if emotion_mod['volume_boost'] > 0:
            combined_audio = combined_audio + emotion_mod['volume_boost']
        
        # Pitch adjustment (rough approximation)
        if emotion_mod['pitch_boost'] > 0:
            new_sample_rate = int(combined_audio.frame_rate * (1 + emotion_mod['pitch_boost'] * 0.03))
            combined_audio = combined_audio._spawn(combined_audio.raw_data, overrides={"frame_rate": new_sample_rate})
            combined_audio = combined_audio.set_frame_rate(22050)
        
        # Dynamic range processing based on emotion intensity
        if emotion_mod['accent_intensity'] in ['high', 'very_high']:
            combined_audio = compress_dynamic_range(combined_audio, threshold=-15.0, ratio=4.0)
        else:
            combined_audio = compress_dynamic_range(combined_audio, threshold=-20.0, ratio=2.0)
        
        # Normalize and add professional touches
        combined_audio = normalize(combined_audio)
        
        # Add fade in/out
        fade_duration = min(150, len(combined_audio) // 20)
        combined_audio = combined_audio.fade_in(fade_duration).fade_out(fade_duration)
        
        return combined_audio
    
    def test_accent_variations(self):
        """Test different accent and emotional combinations with auto-detection and geographic accents"""
        
        test_cases = [
            {
                'text': "🚨 BREAKING: Devastating earthquake hits Los Angeles! Emergency crews rush to save lives as shocking destruction unfolds across California!",
                'category': 'breaking_news',
                'emotion': 'auto',  # Will auto-detect: urgent + shocking
                'news_source': 'CNN',
                'filename': 'test_us_urgent_disaster.wav',
                'expected_location': 'United States',
                'expected_accent': 'American'
            },
            {
                'text': "INCREDIBLE breakthrough! London-based researchers announce revolutionary AI technology that absolutely transforms everything we know about artificial intelligence!",
                'category': 'tech_news',
                'emotion': 'auto',  # Will auto-detect: exciting
                'news_source': 'BBC',
                'filename': 'test_uk_exciting_tech.wav',
                'expected_location': 'United Kingdom', 
                'expected_accent': 'British'
            },
            {
                'text': "In a bizarre and mysterious turn of events in Mumbai, the unexplained phenomenon has puzzled scientists across India. What could this strange discovery mean?",
                'category': 'general',
                'emotion': 'auto',  # Will auto-detect: mysterious
                'news_source': 'Times of India',
                'filename': 'test_india_mysterious_science.wav',
                'expected_location': 'India',
                'expected_accent': 'Indian'
            },
            {
                'text': "Champion celebrates incredible victory! The Sydney-based team's spectacular triumph brings hope and joy to millions of Australian fans across the nation!",
                'category': 'sports',
                'emotion': 'auto',  # Will auto-detect: celebratory + hopeful
                'news_source': 'ABC Australia',
                'filename': 'test_australia_celebratory_sports.wav',
                'expected_location': 'Australia',
                'expected_accent': 'Australian'
            },
            {
                'text': "Economic experts in Toronto warn of concerning trends as Canadian market instability threatens recovery. Bank of Canada officials remain worried about future risks.",
                'category': 'business_news',
                'emotion': 'auto',  # Will auto-detect: concerned
                'news_source': 'CBC',
                'filename': 'test_canada_concerned_business.wav',
                'expected_location': 'Canada',
                'expected_accent': 'Canadian'
            },
            {
                'text': "Hollywood drama explodes! Intense confrontation between major celebrities creates explosive scandal that rocks the entertainment industry in Los Angeles!",
                'category': 'entertainment',
                'emotion': 'auto',  # Will auto-detect: dramatic
                'news_source': 'Entertainment Tonight',
                'filename': 'test_us_dramatic_entertainment.wav',
                'expected_location': 'United States',
                'expected_accent': 'American'
            },
            {
                'text': "Johannesburg financial markets soar as South African rand strengthens against the dollar. Economic recovery shows promising signs across the nation.",
                'category': 'business_news',
                'emotion': 'auto',  # Will auto-detect: hopeful
                'news_source': 'News24',
                'filename': 'test_south_africa_hopeful_business.wav',
                'expected_location': 'South Africa',
                'expected_accent': 'South African'
            },
            {
                'text': "Wellington earthquake preparedness programme receives massive funding boost as New Zealand authorities focus on strengthening infrastructure nationwide.",
                'category': 'general',
                'emotion': 'auto',  # Will auto-detect: professional
                'news_source': 'NZ Herald',
                'filename': 'test_new_zealand_professional_news.wav',
                'expected_location': 'New Zealand',
                'expected_accent': 'New Zealand'
            }
        ]
        
        print("🎭 Testing Geographic Accent-Aware TTS with Auto Detection...")
        print("🌍 Each test demonstrates automatic accent selection based on news location")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\\n📝 Test {i}: {test_case['expected_location']} News - {test_case['expected_accent']} Accent")
            print(f"Source: {test_case['news_source']}")
            print(f"Text: {test_case['text'][:80]}...")
            
            success = self.generate_contextual_audio(
                text=test_case['text'],
                output_path=test_case['filename'],
                category=test_case['category'],
                emotion=test_case['emotion'],
                news_source=test_case['news_source']
            )
            
            if success:
                print(f"✅ Generated: {test_case['filename']}")
                print(f"🗣️ Expected accent: {test_case['expected_accent']}")
            else:
                print(f"❌ Failed: {test_case['filename']}")
        
        print(f"\\n🎯 Geographic Accent Mapping Demonstrated:")
        print(f"• 🇺🇸 US news (Los Angeles, Hollywood) → American accent")
        print(f"• 🇬🇧 UK news (London) → British accent")
        print(f"• 🇮🇳 Indian news (Mumbai) → Indian accent")
        print(f"• 🇦🇺 Australian news (Sydney) → Australian accent")
        print(f"• 🇨🇦 Canadian news (Toronto) → Canadian accent")
        print(f"• 🇿🇦 South African news (Johannesburg) → South African accent")
        print(f"• 🇳🇿 New Zealand news (Wellington) → New Zealand accent")

def main():
    """Test the accent-aware TTS system with emotion detection"""
    
    tts = AccentAwareTTS()
    tts.test_accent_variations()
    
    print("\\n🎯 Emotion Detection Features:")
    print("• 🚨 URGENT: Fast pace, high pitch for breaking news/disasters")
    print("• 🎉 EXCITING: Enthusiastic delivery for breakthroughs/victories")  
    print("• 😮 SHOCKING: Dramatic pauses and emphasis for surprises")
    print("• 🏆 CELEBRATORY: Upbeat tone for wins and achievements")
    print("• 😟 CONCERNED: Cautious tone for warnings and risks")
    print("• 🎭 DRAMATIC: Intense delivery for scandals and confrontations")
    print("• 🔍 MYSTERIOUS: Curious tone for unexplained phenomena")
    print("• 🌟 HOPEFUL: Optimistic delivery for positive developments")
    
    print("\\n🗣️ Accent Adaptations:")
    print("• 🇺🇸 American accent for tech/entertainment news")
    print("• 🇬🇧 British accent for business/international news")
    print("• 🌍 Context-aware accent selection based on content")
    print("• 📍 Location-specific pronunciation (London=British, NYC=American)")
    
    print("\\n🎵 Voice Characteristics:")
    print("• Speed adjusts based on urgency and emotion")
    print("• Pitch varies for emphasis and emotional impact")
    print("• Pauses add drama and allow information to sink in")
    print("• Volume emphasizes important words and phrases")

if __name__ == "__main__":
    main()
