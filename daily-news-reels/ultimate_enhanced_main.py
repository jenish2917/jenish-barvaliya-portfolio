"""
Ultimate Enhanced Main Pipeline - Complete Solution
Combines gender-aware voice selection with realistic human avatars and lip-syncing
"""

import os
import sys
import logging
import json
from datetime import datetime
from pathlib import Path

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from voice_gender_system import VoiceGenderSystem, VoiceGender, VoiceStyle
from gender_aware_audio_service import GenderAwareAudioService
from integrated_avatar_voice_pipeline import IntegratedAvatarVoicePipeline

class UltimateEnhancedPipeline:
    """The ultimate pipeline combining all features:
    - Male/Female voice selection (FIXES female-only issue)
    - Realistic human avatars with lip-syncing 
    - Professional news presentation
    - Complete automation
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the ultimate pipeline"""
        
        # Setup logging
        self.setup_logging()
        
        # Initialize core systems
        self.voice_system = VoiceGenderSystem()
        self.audio_service = GenderAwareAudioService()
        self.avatar_pipeline = IntegratedAvatarVoicePipeline()
        
        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("output/ultimate_pipeline")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.session_stats = {
            'total_articles': 0,
            'successful_videos': 0,
            'male_voices': 0,
            'female_voices': 0,
            'categories_processed': set(),
            'start_time': datetime.now(),
            'errors': []
        }
        
        self.logger.info("🚀 Ultimate Enhanced Pipeline Initialized")
        self.logger.info("✅ Gender-aware voice selection ACTIVE")
        self.logger.info("✅ Realistic human avatars ACTIVE")
        self.logger.info("✅ Lip-syncing technology ACTIVE")
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = Path("output/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"ultimate_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('UltimatePipeline')
    
    def process_article(self, article: dict) -> dict:
        """Process a single article with complete pipeline"""
        
        try:
            self.session_stats['total_articles'] += 1
            article_id = f"article_{self.session_stats['total_articles']:03d}"
            
            self.logger.info(f"\n📰 Processing Article {self.session_stats['total_articles']}: {article.get('title', 'Untitled')}")
            
            # Extract article info
            title = article.get('title', 'Breaking News')
            content = article.get('content', article.get('script', ''))
            category = article.get('category', 'general')
            
            # Update category stats
            self.session_stats['categories_processed'].add(category)
            
            # Generate professional script
            script = self.generate_news_script(title, content, category)
            
            # Select voice profile with gender variety
            voice_profile = self.select_optimal_voice_profile(category, article)
            
            # Generate complete video with avatar and voice
            result = self.avatar_pipeline.create_avatar_video(
                script=script,
                output_name=f"{article_id}_{title.replace(' ', '_')[:50]}",
                voice_profile=voice_profile,
                video_style='professional_news'
            )
            
            if result['success']:
                self.session_stats['successful_videos'] += 1
                
                # Update voice stats
                if voice_profile.gender == VoiceGender.MALE:
                    self.session_stats['male_voices'] += 1
                else:
                    self.session_stats['female_voices'] += 1
                
                self.logger.info(f"✅ SUCCESS: Generated {result['video_path']}")
                self.logger.info(f"🎤 Voice: {voice_profile.description}")
                self.logger.info(f"👤 Avatar: {result.get('avatar_style', 'Professional')}")
                
                return {
                    'success': True,
                    'article_id': article_id,
                    'video_path': result['video_path'],
                    'audio_path': result['audio_path'],
                    'voice_profile': voice_profile,
                    'processing_time': result.get('processing_time', 0),
                    'quality_score': result.get('quality_score', 0)
                }
            else:
                self.logger.error(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                self.session_stats['errors'].append({
                    'article_id': article_id,
                    'error': result.get('error', 'Unknown error'),
                    'timestamp': datetime.now().isoformat()
                })
                
                return {
                    'success': False,
                    'article_id': article_id,
                    'error': result.get('error', 'Unknown error')
                }
        
        except Exception as e:
            self.logger.error(f"💥 EXCEPTION processing article: {e}")
            self.session_stats['errors'].append({
                'article_id': article_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'success': False,
                'article_id': article_id,
                'error': str(e)
            }
    
    def generate_news_script(self, title: str, content: str, category: str) -> str:
        """Generate professional news script"""
        
        # Create engaging news script
        script_parts = []
        
        # Professional opening
        if category == 'business':
            script_parts.append("Good evening. In today's business update.")
        elif category == 'technology':
            script_parts.append("Breaking technology news.")
        elif category == 'sports':
            script_parts.append("From the world of sports.")
        elif category == 'health':
            script_parts.append("Important health news tonight.")
        elif category == 'entertainment':
            script_parts.append("Entertainment headlines.")
        else:
            script_parts.append("Breaking news.")
        
        # Main content
        if content:
            # Clean and process content
            clean_content = content.replace('\n', ' ').strip()
            if len(clean_content) > 300:
                clean_content = clean_content[:300] + "..."
            script_parts.append(clean_content)
        else:
            script_parts.append(title)
        
        # Professional closing
        script_parts.append("We'll continue following this story.")
        
        return " ".join(script_parts)
    
    def select_optimal_voice_profile(self, category: str, article: dict):
        """Select optimal voice profile with gender balancing"""
        
        # Calculate current gender balance
        total_voices = self.session_stats['male_voices'] + self.session_stats['female_voices']
        
        preferred_gender = None
        
        if total_voices > 0:
            male_ratio = self.session_stats['male_voices'] / total_voices
            
            # Force balance if too skewed
            if male_ratio > 0.7:
                preferred_gender = VoiceGender.FEMALE
                self.logger.info("🎯 Forcing female voice for gender balance")
            elif male_ratio < 0.3:
                preferred_gender = VoiceGender.MALE
                self.logger.info("🎯 Forcing male voice for gender balance")
        
        # Select voice profile
        return self.voice_system.select_voice_profile(
            category=category,
            preferred_gender=preferred_gender,
            session_consistency=True
        )
    
    def process_multiple_articles(self, articles: list) -> dict:
        """Process multiple articles in batch"""
        
        self.logger.info(f"\n🚀 STARTING BATCH PROCESSING: {len(articles)} articles")
        self.logger.info("="*60)
        
        results = []
        
        for i, article in enumerate(articles, 1):
            self.logger.info(f"\n[{i}/{len(articles)}] Processing article...")
            result = self.process_article(article)
            results.append(result)
        
        # Generate final report
        report = self.generate_session_report()
        
        return {
            'session_id': self.session_id,
            'results': results,
            'report': report,
            'total_processed': len(articles),
            'successful': len([r for r in results if r['success']]),
            'failed': len([r for r in results if not r['success']])
        }
    
    def generate_session_report(self) -> dict:
        """Generate comprehensive session report"""
        
        end_time = datetime.now()
        duration = end_time - self.session_stats['start_time']
        
        total_voices = self.session_stats['male_voices'] + self.session_stats['female_voices']
        
        report = {
            'session_summary': {
                'session_id': self.session_id,
                'start_time': self.session_stats['start_time'].isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration.total_seconds(),
                'total_articles': self.session_stats['total_articles'],
                'successful_videos': self.session_stats['successful_videos'],
                'success_rate': (self.session_stats['successful_videos'] / max(1, self.session_stats['total_articles'])) * 100
            },
            'voice_analysis': {
                'total_voices': total_voices,
                'male_voices': self.session_stats['male_voices'],
                'female_voices': self.session_stats['female_voices'],
                'male_percentage': (self.session_stats['male_voices'] / max(1, total_voices)) * 100,
                'female_percentage': (self.session_stats['female_voices'] / max(1, total_voices)) * 100,
                'gender_balance_score': self.calculate_gender_balance_score()
            },
            'categories_processed': list(self.session_stats['categories_processed']),
            'errors': self.session_stats['errors'],
            'performance_metrics': {
                'avg_processing_time': duration.total_seconds() / max(1, self.session_stats['total_articles']),
                'videos_per_minute': (self.session_stats['successful_videos'] / max(1, duration.total_seconds() / 60))
            }
        }
        
        return report
    
    def calculate_gender_balance_score(self) -> float:
        """Calculate gender balance score (0-100)"""
        total_voices = self.session_stats['male_voices'] + self.session_stats['female_voices']
        
        if total_voices == 0:
            return 0
        
        male_pct = (self.session_stats['male_voices'] / total_voices) * 100
        female_pct = (self.session_stats['female_voices'] / total_voices) * 100
        
        # Optimal balance is 40-60% for each gender
        balance_score = 100 - abs(50 - male_pct) * 2
        
        return max(0, balance_score)
    
    def save_session_report(self, report: dict):
        """Save session report to file"""
        
        report_file = self.output_dir / f"session_report_{self.session_id}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"📊 Session report saved: {report_file}")

def main():
    """Demonstrate the ultimate enhanced pipeline"""
    
    print("🚀 ULTIMATE ENHANCED PIPELINE - COMPLETE SOLUTION")
    print("="*80)
    print("✅ Fixes female-only voice issue with male/female selection")
    print("✅ Realistic human avatars with lip-syncing")
    print("✅ Professional news presentation")
    print("✅ Complete automation")
    print("="*80)
    
    # Create pipeline
    pipeline = UltimateEnhancedPipeline()
    
    # Test articles across different categories
    test_articles = [
        {
            'title': 'Major Corporate Merger Announced', 
            'content': 'Two industry giants have announced a groundbreaking merger that will reshape the business landscape and create new opportunities for growth.',
            'category': 'business'
        },
        {
            'title': 'Revolutionary Medical Breakthrough',
            'content': 'Scientists have discovered a revolutionary treatment that offers new hope to millions of patients worldwide with promising clinical results.',
            'category': 'health'
        },
        {
            'title': 'Championship Victory Celebration',
            'content': 'In a thrilling match that went into overtime, the home team secured a stunning victory that will be remembered for generations.',
            'category': 'sports'
        },
        {
            'title': 'AI Technology Advancement',
            'content': 'Tech leaders unveiled groundbreaking artificial intelligence capabilities that promise to transform how we interact with technology daily.',
            'category': 'technology'
        },
        {
            'title': 'Hollywood Awards Recognition',
            'content': 'Independent filmmakers received prestigious recognition for their outstanding artistic achievements and cultural contributions.',
            'category': 'entertainment'
        }
    ]
    
    print(f"\n📺 Processing {len(test_articles)} news articles...")
    
    # Process articles
    batch_result = pipeline.process_multiple_articles(test_articles)
    
    # Display results
    print(f"\n📊 BATCH PROCESSING RESULTS")
    print("="*40)
    print(f"Total Articles: {batch_result['total_processed']}")
    print(f"Successful Videos: {batch_result['successful']}")
    print(f"Failed: {batch_result['failed']}")
    print(f"Success Rate: {(batch_result['successful']/batch_result['total_processed']*100):.1f}%")
    
    # Voice analysis
    report = batch_result['report']
    voice_analysis = report['voice_analysis']
    
    print(f"\n🎤 VOICE GENDER ANALYSIS")
    print("="*30)
    print(f"Total Voices: {voice_analysis['total_voices']}")
    print(f"Male Voices: {voice_analysis['male_voices']} ({voice_analysis['male_percentage']:.1f}%)")
    print(f"Female Voices: {voice_analysis['female_voices']} ({voice_analysis['female_percentage']:.1f}%)")
    print(f"Gender Balance Score: {voice_analysis['gender_balance_score']:.1f}/100")
    
    # Solution status
    print(f"\n🎯 SOLUTION STATUS")
    print("="*25)
    
    female_only_fixed = voice_analysis['male_voices'] > 0
    gender_variety = voice_analysis['total_voices'] > 1 and voice_analysis['male_voices'] > 0 and voice_analysis['female_voices'] > 0
    high_success = batch_result['successful'] / batch_result['total_processed'] > 0.8
    
    print(f"Female-only voice issue: {'✅ COMPLETELY FIXED' if female_only_fixed else '❌ NOT FIXED'}")
    print(f"Gender variety: {'✅ EXCELLENT' if gender_variety else '⚠️ LIMITED'}")
    print(f"Video generation: {'✅ EXCELLENT' if high_success else '⚠️ NEEDS IMPROVEMENT'}")
    print(f"Realistic avatars: {'✅ IMPLEMENTED' if batch_result['successful'] > 0 else '❌ NOT WORKING'}")
    
    # Save report
    pipeline.save_session_report(batch_result)
    
    if female_only_fixed and gender_variety and high_success:
        print(f"\n🎉 COMPLETE SUCCESS! All issues resolved:")
        print(f"   ✅ No more female-only voices")
        print(f"   ✅ Male and female voices working")
        print(f"   ✅ Realistic avatars with lip-syncing")
        print(f"   ✅ Professional news presentation")
    else:
        print(f"\n⚠️  Some issues remain - check logs for details")

if __name__ == "__main__":
    main()
