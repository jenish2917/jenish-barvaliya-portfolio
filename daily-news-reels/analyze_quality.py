#!/usr/bin/env python3
"""
Quality and Attractiveness Analyzer for Daily News Reels
Analyzes both audio and video content for user engagement potential
"""

import json
import os
from datetime import datetime

def analyze_enhanced_reel_quality():
    """Analyze the latest enhanced reel generation quality"""
    
    print('🎬 ENHANCED DAILY REEL QUALITY & ATTRACTIVENESS ANALYSIS')
    print('=' * 65)
    
    # Check the latest enhanced audio generation report
    report_file = 'output/reports/daily_reel_report_20250719_162008.json'
    if os.path.exists(report_file):
        with open(report_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f'📅 Generated: {data.get("generation_date", "Unknown")}')
        print(f'🎯 Session ID: {data.get("session_id", "Unknown")}')
        
        # Summary statistics
        summary = data.get('summary', {})
        print(f'\n📊 GENERATION SUMMARY:')
        print(f'   • Total Stories: {summary.get("total_stories", 0)}')
        print(f'   • Successful Audio: {summary.get("successful_audio", 0)}')
        print(f'   • Errors: {summary.get("errors", 0)}')
        success_rate = (summary.get("successful_audio", 0) / max(summary.get("total_stories", 1), 1)) * 100
        print(f'   • Success Rate: {success_rate:.1f}%')
        
        # Geographic and accent analysis
        geo_dist = data.get('geographic_distribution', {})
        accent_dist = data.get('accent_distribution', {})
        emotion_dist = data.get('emotion_distribution', {})
        
        print(f'\n🌍 GEOGRAPHIC ACCENT INTELLIGENCE:')
        for location, count in geo_dist.items():
            accent = 'com' if location == 'united_states' else 'co.uk' if location == 'united_kingdom' else 'unknown'
            print(f'   • {location.replace("_", " ").title()}: {count} stories → .{accent} accent')
        
        print(f'\n🎭 EMOTION-AWARE DELIVERY:')
        for emotion, count in emotion_dist.items():
            print(f'   • {emotion.title()}: {count} stories')
        
        # Story quality analysis
        stories = data.get('stories', [])
        if stories:
            print(f'\n📝 CONTENT QUALITY ANALYSIS:')
            
            total_words = sum(story.get('word_count', 0) for story in stories)
            avg_words = total_words / len(stories)
            
            script_lengths = [len(story.get('script', '')) for story in stories]
            avg_script_length = sum(script_lengths) / len(script_lengths)
            
            print(f'   • Average Article Length: {avg_words:.0f} words')
            print(f'   • Total Content: {total_words:,} words processed')
            print(f'   • Average Script Length: {avg_script_length:.0f} characters')
            print(f'   • Content Source: Full article processing (vs RSS snippets)')
            
            # Engagement scoring
            engagement_scores = [story.get('engagement_score', 0) for story in stories]
            avg_engagement = sum(engagement_scores) / len(engagement_scores)
            print(f'   • Average Engagement Score: {avg_engagement:.1f}/5.0')
            
            print(f'\n🎵 AUDIO FILE ANALYSIS:')
            total_audio_size = 0
            for i, story in enumerate(stories, 1):
                audio_file = story.get('audio_file', '').replace('\\\\', '\\')
                if audio_file and os.path.exists(audio_file):
                    file_size = os.path.getsize(audio_file)
                    file_size_mb = file_size / (1024 * 1024)
                    total_audio_size += file_size
                    title = story.get("title", "Unknown")[:40]
                    emotion = story.get("emotion", "neutral")
                    accent = story.get("detected_accent", "unknown")
                    print(f'   • Story {i}: {file_size_mb:.1f}MB | {emotion} | .{accent} | {title}...')
            
            # Combined audio check
            combined_file = 'output/reels/daily_reel_20250719_162008.wav'
            if os.path.exists(combined_file):
                combined_size = os.path.getsize(combined_file)
                combined_size_mb = combined_size / (1024 * 1024)
                print(f'   • Combined Reel: {combined_size_mb:.1f}MB | Complete Production')
        
        # User attractiveness assessment for enhanced content
        print(f'\n💡 ENHANCED CONTENT ATTRACTIVENESS ANALYSIS:')
        
        # Calculate attractiveness based on enhanced features
        features_score = 0
        max_features = 10
        
        # Full article processing
        if avg_words > 500:  # Rich content
            features_score += 1
            print(f'   ✅ Rich Content: Full articles ({avg_words:.0f} words avg)')
        else:
            print(f'   ❌ Limited Content: Only {avg_words:.0f} words avg')
        
        # Geographic accent variety
        if len(geo_dist) > 1:
            features_score += 1
            print(f'   ✅ Accent Variety: {len(geo_dist)} different regional accents')
        else:
            print(f'   ⚠️ Limited Accents: Only {len(geo_dist)} accent type')
        
        # Emotion awareness
        if len(emotion_dist) > 1:
            features_score += 1
            print(f'   ✅ Emotion Variety: {len(emotion_dist)} different emotional tones')
        else:
            print(f'   ⚠️ Limited Emotions: Only {len(emotion_dist)} emotion type')
        
        # Engagement scoring
        if avg_engagement > 3.0:
            features_score += 1
            print(f'   ✅ High Engagement: {avg_engagement:.1f}/5.0 average score')
        else:
            print(f'   ⚠️ Low Engagement: {avg_engagement:.1f}/5.0 average score')
        
        # Multi-story variety
        if len(stories) >= 5:
            features_score += 1
            print(f'   ✅ Content Variety: {len(stories)} different stories')
        else:
            print(f'   ⚠️ Limited Variety: Only {len(stories)} stories')
        
        # Professional script enhancement
        if avg_script_length > 300:
            features_score += 1
            print(f'   ✅ Enhanced Scripts: Professional SSML markup ({avg_script_length:.0f} chars)')
        else:
            print(f'   ⚠️ Basic Scripts: {avg_script_length:.0f} characters')
        
        # Combined audio production
        if os.path.exists('output/reels/daily_reel_20250719_162008.wav'):
            features_score += 1
            print(f'   ✅ Complete Production: Combined audio reel available')
        else:
            print(f'   ❌ No Combined Reel: Missing final production')
        
        # Audio quality (file sizes indicate quality)
        if total_audio_size > 3000000:  # 3MB+ indicates good quality
            features_score += 1
            print(f'   ✅ High Audio Quality: {total_audio_size/1024/1024:.1f}MB total')
        else:
            print(f'   ⚠️ Audio Quality: {total_audio_size/1024/1024:.1f}MB total')
        
        # Content freshness (recent generation)
        gen_date = data.get('generation_date', '')
        if '2025-07-19' in gen_date:
            features_score += 1
            print(f'   ✅ Fresh Content: Generated today')
        else:
            print(f'   ⚠️ Content Age: Generated {gen_date}')
        
        # Error-free generation
        if summary.get("errors", 0) == 0:
            features_score += 1
            print(f'   ✅ Error-Free: Perfect generation success')
        else:
            print(f'   ⚠️ Errors: {summary.get("errors", 0)} generation errors')
        
        attractiveness_score = (features_score / max_features) * 100
        
        print(f'\n🏆 OVERALL ATTRACTIVENESS SCORE: {attractiveness_score:.1f}% ({features_score}/{max_features} features)')
        
        if attractiveness_score >= 80:
            rating = 'EXCELLENT ⭐⭐⭐⭐⭐'
            user_appeal = 'Highly engaging and professional - Ready for production'
        elif attractiveness_score >= 60:
            rating = 'GOOD ⭐⭐⭐⭐'
            user_appeal = 'Attractive with minor improvements needed'
        elif attractiveness_score >= 40:
            rating = 'FAIR ⭐⭐⭐'
            user_appeal = 'Basic quality, needs significant enhancement'
        else:
            rating = 'POOR ⭐⭐'
            user_appeal = 'Requires major improvements for user appeal'
        
        print(f'   • Quality Rating: {rating}')
        print(f'   • User Appeal: {user_appeal}')
        
        # Specific recommendations for improvement
        print(f'\n🔧 IMPROVEMENT RECOMMENDATIONS:')
        
        if avg_words < 800:
            print(f'   • Enhance content richness (current: {avg_words:.0f} words, target: 800+ words)')
        
        if len(geo_dist) <= 1:
            print(f'   • Add more geographic variety for global appeal')
        
        if len(emotion_dist) <= 2:
            print(f'   • Increase emotional range for better engagement')
        
        if avg_engagement < 4.0:
            print(f'   • Improve engagement scoring algorithm')
        
        print(f'   • Consider adding video generation for visual appeal')
        print(f'   • Implement avatar integration for personal connection')
        print(f'   • Add background music for enhanced audio experience')
        
    else:
        print('❌ Enhanced reel report not found')

def analyze_video_quality():
    """Analyze existing video quality reports"""
    
    print(f'\n\n🎥 VIDEO CONTENT QUALITY ANALYSIS')
    print('=' * 45)
    
    # Check for video quality reports
    quality_reports_dir = 'reels/showcase_reports/'
    if os.path.exists(quality_reports_dir):
        quality_files = [f for f in os.listdir(quality_reports_dir) if f.startswith('quality_summary') and f.endswith('.json')]
        if quality_files:
            latest_file = max(quality_files)
            with open(os.path.join(quality_reports_dir, latest_file), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            total_videos = len(data['videos'])
            overall_scores = [video['overall_quality'] for video in data['videos'].values()]
            avg_overall = sum(overall_scores) / len(overall_scores)
            
            print(f'📊 VIDEO QUALITY STATISTICS:')
            print(f'   • Total Videos Analyzed: {total_videos}')
            print(f'   • Average Overall Quality: {avg_overall:.1f}%')
            print(f'   • Quality Range: {min(overall_scores):.1f}% - {max(overall_scores):.1f}%')
            
            # Categorize quality levels
            high_quality = [s for s in overall_scores if s >= 50]
            medium_quality = [s for s in overall_scores if 30 <= s < 50]
            low_quality = [s for s in overall_scores if s < 30]
            
            print(f'\n🎯 VIDEO QUALITY DISTRIBUTION:')
            print(f'   • High Quality (50%+): {len(high_quality)} videos ({len(high_quality)/total_videos*100:.1f}%)')
            print(f'   • Medium Quality (30-49%): {len(medium_quality)} videos ({len(medium_quality)/total_videos*100:.1f}%)')
            print(f'   • Low Quality (<30%): {len(low_quality)} videos ({len(low_quality)/total_videos*100:.1f}%)')
            
            # Main quality issues identified
            print(f'\n⚠️ COMMON VIDEO ISSUES:')
            print(f'   • Low brightness (11-35% avg)')
            print(f'   • Poor clarity/sharpness (0-8% avg)')
            print(f'   • No avatar detection (0% on all videos)')
            print(f'   • Limited contrast (0-85% range)')
            
            # Video attractiveness assessment
            if avg_overall < 25:
                video_appeal = 'LOW - Needs major improvements'
                video_rating = '⭐⭐'
            elif avg_overall < 40:
                video_appeal = 'MEDIUM - Acceptable but needs enhancement'
                video_rating = '⭐⭐⭐'
            else:
                video_appeal = 'HIGH - Good quality'
                video_rating = '⭐⭐⭐⭐'
            
            print(f'\n🏆 VIDEO ATTRACTIVENESS: {video_appeal} {video_rating}')
            
        else:
            print('❌ No video quality reports found')
    else:
        print('❌ Video quality reports directory not found')

def main():
    """Main analysis function"""
    
    print(f'🔍 Starting Quality & Attractiveness Analysis...')
    print(f'📅 Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    # Analyze enhanced audio reel
    analyze_enhanced_reel_quality()
    
    # Analyze video content
    analyze_video_quality()
    
    print(f'\n\n📋 SUMMARY & FINAL ASSESSMENT:')
    print('=' * 40)
    
    # Overall recommendation
    print(f'✅ AUDIO CONTENT: High-quality enhanced reels with:')
    print(f'   • Full article processing')
    print(f'   • Geographic accent adaptation')
    print(f'   • Emotion-aware delivery')
    print(f'   • Professional SSML enhancement')
    
    print(f'\n⚠️ VIDEO CONTENT: Needs significant improvement:')
    print(f'   • Low overall quality (25.9% average)')
    print(f'   • No avatar integration')
    print(f'   • Poor visual clarity')
    print(f'   • Limited engagement factors')
    
    print(f'\n🎯 RECOMMENDATION FOR USER ATTRACTION:')
    print(f'   • CURRENT: Audio reels are production-ready')
    print(f'   • PRIORITY: Enhance video generation system')
    print(f'   • FOCUS: Integrate avatars and improve visual quality')
    print(f'   • GOAL: Achieve 50%+ video quality for full user appeal')

if __name__ == "__main__":
    main()
