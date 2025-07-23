"""
Integrated Realistic Avatar + Voice Pipeline
Combines realistic human avatars with gender-matched voice selection
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json
from datetime import datetime

# Import our systems
from realistic_avatar_system import RealisticAvatarSystem
from gender_aware_audio_service import GenderAwareAudioService, VoiceGender, VoiceStyle
from voice_gender_system import VoiceGenderSystem

class IntegratedAvatarVoicePipeline:
    """Complete pipeline combining realistic avatars with gender-matched voices"""
    
    def __init__(self):
        self.logger = logging.getLogger('IntegratedPipeline')
        
        # Initialize systems
        self.avatar_system = RealisticAvatarSystem()
        self.audio_service = GenderAwareAudioService()
        self.voice_system = VoiceGenderSystem()
        
        # Pipeline settings
        self.output_dir = Path("output")
        self.quality_threshold = 85
        
        # Session tracking
        self.session_stats = {
            'videos_created': 0,
            'male_voices': 0,
            'female_voices': 0,
            'average_quality': 0,
            'avatar_styles_used': [],
            'voice_profiles_used': []
        }
        
        self._setup_output_dirs()
    
    def _setup_output_dirs(self):
        """Setup output directories"""
        dirs = ['videos', 'audio', 'avatars', 'sessions', 'reports']
        for dir_name in dirs:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    def create_realistic_news_video(self,
                                  title: str,
                                  script: str,
                                  category: str = 'general',
                                  preferred_gender: Optional[VoiceGender] = None,
                                  preferred_style: Optional[VoiceStyle] = None,
                                  avatar_customization: Optional[Dict] = None) -> Optional[Dict]:
        """
        Create a complete news video with realistic avatar and matching voice
        
        Args:
            title: Video title
            script: News script text
            category: News category for optimal voice selection
            preferred_gender: Force specific gender
            preferred_style: Force specific voice style
            avatar_customization: Custom avatar settings
        
        Returns:
            Dict with video info and quality metrics or None if failed
        """
        
        try:
            self.logger.info(f"🎬 Creating realistic news video: {title[:50]}...")
            
            # Generate timestamp for unique naming
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"{timestamp}_{title[:30].replace(' ', '_')}"
            
            # Paths
            audio_path = self.output_dir / "audio" / f"{base_name}.wav"
            video_path = self.output_dir / "videos" / f"{base_name}.mp4"
            
            # Step 1: Generate gender-appropriate voice
            self.logger.info("🎤 Generating gender-matched voiceover...")
            audio_result = self.audio_service.generate_gendered_voiceover(
                script=script,
                output_path=str(audio_path),
                category=category,
                preferred_gender=preferred_gender,
                preferred_style=preferred_style,
                session_consistency=True
            )
            
            if not audio_result:
                self.logger.error("Failed to generate voiceover")
                return None
            
            audio_path_final, audio_metrics, avatar_config = audio_result
            
            # Merge custom avatar settings if provided
            if avatar_customization:
                avatar_config.update(avatar_customization)
            
            # Step 2: Create realistic avatar with lip-syncing
            self.logger.info("👤 Creating realistic avatar with lip-syncing...")
            avatar_result = self.avatar_system.create_realistic_avatar(
                audio_path=audio_path_final,
                output_path=str(video_path),
                avatar_style=avatar_config.get('gender', 'professional_male'),
                background_style=avatar_config.get('background', 'professional_studio'),
                customization=avatar_config
            )
            
            if not avatar_result:
                self.logger.error("Failed to create realistic avatar")
                return None
            
            # Step 3: Analyze overall quality
            overall_quality = self._analyze_video_quality(
                video_path=str(video_path),
                audio_metrics=audio_metrics,
                avatar_config=avatar_config
            )
            
            # Step 4: Update session statistics
            self._update_session_stats(audio_metrics, avatar_config, overall_quality)
            
            # Create video info
            video_info = {
                'title': title,
                'video_path': str(video_path),
                'audio_path': audio_path_final,
                'timestamp': timestamp,
                'category': category,
                'quality_metrics': {
                    'overall_quality': overall_quality,
                    'audio_quality': audio_metrics.quality_score,
                    'avatar_quality': avatar_result.get('quality_score', 85),
                    'lip_sync_quality': avatar_result.get('lip_sync_score', 80),
                    'voice_profile': audio_metrics.voice_profile,
                    'avatar_style': avatar_config.get('gender', 'unknown')
                },
                'technical_specs': {
                    'duration': audio_metrics.duration,
                    'voice_gender': avatar_config.get('gender'),
                    'voice_style': avatar_config.get('style', 'professional'),
                    'background': avatar_config.get('background'),
                    'resolution': '1080x1920',
                    'fps': 30
                },
                'avatar_config': avatar_config
            }
            
            # Log success
            self.logger.info(f"✅ Created realistic news video!")
            self.logger.info(f"   📊 Overall Quality: {overall_quality:.1f}%")
            self.logger.info(f"   🎤 Voice: {audio_metrics.voice_profile}")
            self.logger.info(f"   👤 Avatar: {avatar_config.get('gender', 'unknown')} {avatar_config.get('style', 'professional')}")
            self.logger.info(f"   ⏱️  Duration: {audio_metrics.duration:.1f}s")
            self.logger.info(f"   📁 Output: {video_path}")
            
            return video_info
            
        except Exception as e:
            self.logger.error(f"Error creating realistic news video: {e}")
            return None
    
    def create_news_batch(self,
                         articles: List[Dict],
                         force_gender_variety: bool = True,
                         quality_threshold: float = 85) -> List[Dict]:
        """
        Create a batch of news videos with gender variety
        
        Args:
            articles: List of article dictionaries with title, script, category
            force_gender_variety: Ensure gender variety across videos
            quality_threshold: Minimum quality threshold
        
        Returns:
            List of successful video info dictionaries
        """
        
        self.logger.info(f"🎬 Creating batch of {len(articles)} realistic news videos...")
        
        successful_videos = []
        gender_rotation = [VoiceGender.MALE, VoiceGender.FEMALE] if force_gender_variety else [None]
        gender_index = 0
        
        for i, article in enumerate(articles):
            try:
                # Rotate gender if variety is enabled
                preferred_gender = None
                if force_gender_variety:
                    preferred_gender = gender_rotation[gender_index % len(gender_rotation)]
                    gender_index += 1
                
                # Create video
                video_info = self.create_realistic_news_video(
                    title=article.get('title', f'News Article {i+1}'),
                    script=article.get('script', article.get('content', '')),
                    category=article.get('category', 'general'),
                    preferred_gender=preferred_gender
                )
                
                if video_info and video_info['quality_metrics']['overall_quality'] >= quality_threshold:
                    successful_videos.append(video_info)
                    self.logger.info(f"✅ Video {i+1}/{len(articles)} created successfully")
                else:
                    self.logger.warning(f"⚠️  Video {i+1}/{len(articles)} failed quality check")
                
            except Exception as e:
                self.logger.error(f"Error creating video {i+1}: {e}")
                continue
        
        self.logger.info(f"🎉 Batch complete: {len(successful_videos)}/{len(articles)} videos created")
        return successful_videos
    
    def _analyze_video_quality(self,
                             video_path: str,
                             audio_metrics,
                             avatar_config: Dict) -> float:
        """Analyze overall video quality"""
        
        # Quality components
        audio_quality = audio_metrics.quality_score
        avatar_quality = 85  # Base avatar quality (would be from avatar system)
        lip_sync_quality = 80  # Base lip-sync quality (would be from avatar system)
        
        # Gender matching bonus
        gender_match_bonus = 5  # Bonus for proper gender matching
        
        # Style appropriateness
        style_bonus = 0
        if avatar_config.get('style') in ['professional', 'business_suit', 'business_attire']:
            style_bonus = 3
        
        # Overall calculation
        overall_quality = (
            audio_quality * 0.4 +  # 40% audio quality
            avatar_quality * 0.25 +  # 25% avatar quality
            lip_sync_quality * 0.25 +  # 25% lip-sync quality
            gender_match_bonus +  # Gender matching bonus
            style_bonus  # Style appropriateness bonus
        ) * 0.9  # Scale to realistic range
        
        return min(100, max(0, overall_quality))
    
    def _update_session_stats(self, audio_metrics, avatar_config: Dict, overall_quality: float):
        """Update session statistics"""
        self.session_stats['videos_created'] += 1
        
        # Gender tracking
        if avatar_config.get('gender') == 'male':
            self.session_stats['male_voices'] += 1
        else:
            self.session_stats['female_voices'] += 1
        
        # Quality tracking
        current_avg = self.session_stats['average_quality']
        videos_count = self.session_stats['videos_created']
        self.session_stats['average_quality'] = (
            (current_avg * (videos_count - 1) + overall_quality) / videos_count
        )
        
        # Track styles
        avatar_style = f"{avatar_config.get('gender', 'unknown')}_{avatar_config.get('style', 'unknown')}"
        if avatar_style not in self.session_stats['avatar_styles_used']:
            self.session_stats['avatar_styles_used'].append(avatar_style)
        
        voice_profile = audio_metrics.voice_profile
        if voice_profile not in self.session_stats['voice_profiles_used']:
            self.session_stats['voice_profiles_used'].append(voice_profile)
    
    def generate_session_report(self) -> Dict:
        """Generate comprehensive session report"""
        
        # Get voice session info
        voice_info = self.audio_service.get_session_voice_info()
        
        # Calculate gender distribution
        total_videos = self.session_stats['videos_created']
        male_percentage = (self.session_stats['male_voices'] / total_videos * 100) if total_videos > 0 else 0
        female_percentage = (self.session_stats['female_voices'] / total_videos * 100) if total_videos > 0 else 0
        
        report = {
            'session_summary': {
                'total_videos': total_videos,
                'average_quality': self.session_stats['average_quality'],
                'male_voices': self.session_stats['male_voices'],
                'female_voices': self.session_stats['female_voices'],
                'gender_distribution': {
                    'male_percentage': male_percentage,
                    'female_percentage': female_percentage
                }
            },
            'variety_metrics': {
                'avatar_styles_used': len(self.session_stats['avatar_styles_used']),
                'voice_profiles_used': len(self.session_stats['voice_profiles_used']),
                'style_variety_score': min(100, len(self.session_stats['avatar_styles_used']) * 20)
            },
            'quality_metrics': {
                'average_quality': self.session_stats['average_quality'],
                'quality_grade': self._get_quality_grade(self.session_stats['average_quality'])
            },
            'voice_session_info': voice_info,
            'detailed_styles': {
                'avatar_styles': self.session_stats['avatar_styles_used'],
                'voice_profiles': self.session_stats['voice_profiles_used']
            }
        }
        
        return report
    
    def _get_quality_grade(self, quality_score: float) -> str:
        """Convert quality score to letter grade"""
        if quality_score >= 95:
            return 'A+'
        elif quality_score >= 90:
            return 'A'
        elif quality_score >= 85:
            return 'B+'
        elif quality_score >= 80:
            return 'B'
        elif quality_score >= 75:
            return 'C+'
        elif quality_score >= 70:
            return 'C'
        else:
            return 'D'
    
    def reset_session(self):
        """Reset session for fresh start"""
        self.session_stats = {
            'videos_created': 0,
            'male_voices': 0,
            'female_voices': 0,
            'average_quality': 0,
            'avatar_styles_used': [],
            'voice_profiles_used': []
        }
        self.audio_service.reset_voice_session()
        self.logger.info("🔄 Pipeline session reset")
    
    def test_gender_variety(self):
        """Test gender variety in video creation"""
        print("🎭 Testing Gender Variety in Realistic Avatar Pipeline...")
        
        test_articles = [
            {
                'title': 'Tech Industry Breakthrough',
                'script': 'Breaking news from Silicon Valley: A revolutionary AI advancement promises to transform the technology industry.',
                'category': 'technology'
            },
            {
                'title': 'Business Market Update',
                'script': 'Stock markets surge as major corporations report record quarterly profits across multiple sectors.',
                'category': 'business'
            },
            {
                'title': 'Sports Championship Victory',
                'script': 'In an incredible comeback, the underdog team secured victory in the championship finals last night.',
                'category': 'sports'
            },
            {
                'title': 'Entertainment Industry News',
                'script': 'Hollywood celebrates as independent filmmakers receive recognition at the prestigious awards ceremony.',
                'category': 'entertainment'
            }
        ]
        
        # Test batch creation with gender variety
        print("\n🎬 Creating test batch with gender variety...")
        videos = self.create_news_batch(test_articles, force_gender_variety=True)
        
        # Generate and display report
        report = self.generate_session_report()
        
        print(f"\n📊 SESSION REPORT:")
        print(f"  Total Videos: {report['session_summary']['total_videos']}")
        print(f"  Average Quality: {report['session_summary']['average_quality']:.1f}% ({report['quality_metrics']['quality_grade']})")
        print(f"  Male Voices: {report['session_summary']['male_voices']} ({report['session_summary']['gender_distribution']['male_percentage']:.1f}%)")
        print(f"  Female Voices: {report['session_summary']['female_voices']} ({report['session_summary']['gender_distribution']['female_percentage']:.1f}%)")
        print(f"  Avatar Styles Used: {report['variety_metrics']['avatar_styles_used']}")
        print(f"  Voice Profiles Used: {report['variety_metrics']['voice_profiles_used']}")
        print(f"  Style Variety Score: {report['variety_metrics']['style_variety_score']}/100")
        
        print(f"\n🎭 DETAILED BREAKDOWN:")
        for style in report['detailed_styles']['avatar_styles']:
            print(f"  Avatar Style: {style}")
        for profile in report['detailed_styles']['voice_profiles']:
            print(f"  Voice Profile: {profile}")
        
        return videos, report

def main():
    """Test the integrated pipeline"""
    print("🚀 Testing Integrated Realistic Avatar + Voice Pipeline...")
    
    # Create pipeline
    pipeline = IntegratedAvatarVoicePipeline()
    
    # Test single video creation
    print("\n🎬 Testing single video creation...")
    
    video_info = pipeline.create_realistic_news_video(
        title="Breaking Tech News",
        script="This is a test of our revolutionary realistic avatar system with gender-matched voice generation. The system now creates human-like presenters with proper lip-syncing and professional appearance.",
        category="technology",
        preferred_gender=VoiceGender.MALE
    )
    
    if video_info:
        print(f"✅ Single video created successfully!")
        print(f"   Quality: {video_info['quality_metrics']['overall_quality']:.1f}%")
        print(f"   Voice: {video_info['quality_metrics']['voice_profile']}")
        print(f"   Avatar: {video_info['quality_metrics']['avatar_style']}")
    
    # Test gender variety
    print("\n🎭 Testing gender variety...")
    pipeline.test_gender_variety()

if __name__ == "__main__":
    main()
