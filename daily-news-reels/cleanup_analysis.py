"""
File Cleanup Analysis
Identifies files used in the core pipeline vs. unused files that can be removed
"""

import os
import json
from pathlib import Path

def analyze_project_files():
    """Analyze which files are part of the core pipeline"""
    
    # Core pipeline files that should be kept
    core_files = {
        # Main entry points
        'enhanced_main.py': 'Primary entry point for the enhanced pipeline',
        'enhanced_main_v2.py': 'Alternative main script',
        
        # Configuration
        'config.env': 'Environment configuration',
        'requirements.txt': 'Core dependencies',
        'enhanced_requirements.txt': 'Enhanced dependencies',
        'setup.py': 'Setup script',
        
        # Core pipeline
        'src/': 'Complete source code directory',
        
        # Enhanced video generation (current working solution)
        'simple_video_creator.py': 'Video creation without MoviePy dependencies',
        'enhanced_video_pipeline.py': 'Enhanced video processing pipeline',
        
        # Quality analysis
        'analyze_quality.py': 'Quality analysis tools',
        'final_attractiveness_assessment.py': 'Attractiveness metrics',
        
        # Testing
        'test_enhanced.py': 'Core pipeline tests',
        'run_tests.py': 'Test runner',
        
        # Documentation  
        'README.md': 'Project documentation',
        'ENHANCED_README_COMPLETE.md': 'Complete enhanced documentation',
        
        # Output directories
        'output/': 'Generated content directory',
        'assets/': 'Static assets directory',
        'reels/': 'Generated reels directory',
    }
    
    # Files that can be removed (not part of core pipeline)
    removable_files = {
        # Old/deprecated main scripts
        'main.py': 'Old main script - replaced by enhanced_main.py',
        'powerful_main.py': 'Alternative implementation - not core',
        'ultimate_pipeline.py': 'Experimental version',
        'final_demo.py': 'Demo script - not core',
        'demo_enhanced_system.py': 'Demo script - not core',
        'enhanced_demo.py': 'Demo script - not core',
        
        # Alternative TTS implementations  
        'powerful_tts.py': 'Alternative TTS - not used in core',
        'simple_powerful_tts.py': 'Alternative TTS - not used in core',
        'ultra_powerful_tts.py': 'Alternative TTS - not used in core',
        'tts_generator.py': 'Old TTS implementation',
        'engaging_gtts.py': 'Alternative TTS implementation',
        'enhanced_bark_tts.py': 'Bark TTS - experimental',
        'accent_aware_tts.py': 'Accent TTS - experimental',
        
        # Alternative video generators
        'video_generator.py': 'Old video generator - replaced',
        'ultra_enhanced_video_generator.py': 'Alternative implementation',
        'avatar_generator.py': 'Avatar system - experimental',
        'avatar_system.py': 'Avatar system - experimental', 
        'enhanced_avatar_system.py': 'Avatar system - experimental',
        
        # Alternative content generators
        'script_generator.py': 'Old script generator - replaced',
        'summarizer.py': 'Old summarizer - replaced',
        'engaging_script_generator.py': 'Alternative implementation',
        'engaging_news_reels.py': 'Alternative implementation',
        
        # Alternative news services
        'daily_reel_generator.py': 'Old implementation',
        'simple_daily_reel.py': 'Simple implementation - not core',
        'enhanced_rss_service.py': 'RSS alternative - not core',
        'rss_news_service.py': 'RSS service - not core',
        'ultimate_rss_bark_app.py': 'RSS + Bark experimental',
        
        # Audio/video analysis tools (not core pipeline)
        'analyze_videos.py': 'Video analysis tool - optional',
        'showcase_video_analyzer.py': 'Video analyzer showcase',
        'audio_demo.py': 'Audio demo - not core',
        'demo_geographic_accents.py': 'Accent demo - not core',
        
        # Test components (optional)
        'test_components.py': 'Component tests - optional',
        'test_components_simple.py': 'Simple component tests',
        
        # Setup files (optional after setup)
        'setup_check.py': 'Setup verification - optional after setup',
        'setup.bat': 'Windows setup batch file',
        'run_video_analyzer.bat': 'Video analyzer batch file',
        
        # Documentation files (cleanup related)
        'CLEANUP_COMPLETE.md': 'Cleanup documentation',
        'CLEANUP_REPORT.md': 'Cleanup report',
        'IMPROVEMENTS.md': 'Improvement notes',
        'ENHANCED_README.md': 'Old enhanced readme',
        'VIDEO_ANALYZER_README.md': 'Video analyzer docs',
        'project_summary.py': 'Project summary script',
        
        # Test audio files
        'test_australia_celebratory_sports.wav': 'Test audio file',
        'test_business_urgent.wav': 'Test audio file',
        'test_canada_concerned_business.wav': 'Test audio file',
        'test_india_mysterious_science.wav': 'Test audio file',
        'test_new_zealand_professional_news.wav': 'Test audio file',
        'test_south_africa_hopeful_business.wav': 'Test audio file',
        'test_sports_exciting.wav': 'Test audio file',
        'test_tech_exciting.wav': 'Test audio file',
        'test_uk_exciting_tech.wav': 'Test audio file',
        'test_us_dramatic_entertainment.wav': 'Test audio file',
        'test_us_urgent_disaster.wav': 'Test audio file',
        
        # Additional directories that might be removable
        'config/': 'Alternative config directory - check if used',
        'resources/': 'Resources directory - check if used',
        'tests/': 'Alternative tests directory',
    }
    
    # Directories to keep but might be empty/removable
    optional_dirs = {
        '.pytest_cache/': 'Pytest cache - can be regenerated',
        '.venv/': 'Virtual environment - project specific',
        '__pycache__/': 'Python cache - can be regenerated',
    }
    
    return core_files, removable_files, optional_dirs

def create_cleanup_plan():
    """Create a cleanup plan"""
    core_files, removable_files, optional_dirs = analyze_project_files()
    
    print("="*80)
    print("🧹 PROJECT CLEANUP ANALYSIS")
    print("="*80)
    
    print(f"\n✅ CORE FILES TO KEEP ({len(core_files)} items):")
    print("-"*50)
    for file, description in core_files.items():
        print(f"  📁 {file:30} - {description}")
    
    print(f"\n🗑️  FILES TO REMOVE ({len(removable_files)} items):")
    print("-"*50)  
    for file, description in removable_files.items():
        if os.path.exists(file):
            print(f"  ❌ {file:30} - {description}")
        else:
            print(f"  ⚪ {file:30} - {description} (not found)")
    
    print(f"\n🔍 OPTIONAL DIRECTORIES ({len(optional_dirs)} items):")
    print("-"*50)
    for dir_name, description in optional_dirs.items():
        if os.path.exists(dir_name):
            print(f"  🟡 {dir_name:30} - {description}")
        else:
            print(f"  ⚪ {dir_name:30} - {description} (not found)")
    
    # Calculate space savings
    total_removable = 0
    existing_removable = []
    
    for file in removable_files.keys():
        if os.path.exists(file):
            existing_removable.append(file)
            if os.path.isfile(file):
                total_removable += os.path.getsize(file)
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print("-"*50)
    print(f"  📁 Core files to keep: {len(core_files)}")
    print(f"  🗑️  Files that can be removed: {len(existing_removable)}")
    print(f"  💾 Estimated space savings: {total_removable / 1024 / 1024:.2f} MB")
    
    return existing_removable

if __name__ == "__main__":
    files_to_remove = create_cleanup_plan()
    
    print(f"\n🎯 CLEANUP RECOMMENDATION:")
    print("-"*50)
    print("1. Test the core pipeline with enhanced_main.py")
    print("2. Verify all functionality works correctly")
    print("3. After successful testing, remove the identified files")
    print("4. Keep a backup before deletion")
    
    # Save cleanup list
    with open('cleanup_list.json', 'w') as f:
        json.dump(files_to_remove, f, indent=2)
    
    print(f"\n📋 Cleanup list saved to 'cleanup_list.json'")
