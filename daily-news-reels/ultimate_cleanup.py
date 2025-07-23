"""
Ultimate Cleanup Script
Removes all unnecessary and duplicate files, keeping only essential working components
"""

import os
import shutil
import glob
from datetime import datetime

class UltimateCleanup:
    def __init__(self):
        self.root_dir = "."
        
        # ESSENTIAL FILES TO KEEP (Final working system)
        self.essential_files = {
            # Core working scripts
            'batch_todays_news_generator.py',  # Main batch news reel generator
            'show_reel_locations.py',         # File location manager
            
            # Configuration
            'requirements.txt',               # Dependencies
            'README.md',                     # Documentation
            '.gitignore',                    # Git config
            
            # Core source code (keep src/ directory structure)
        }
        
        # ESSENTIAL DIRECTORIES TO KEEP
        self.essential_dirs = {
            'src',           # Core source code
            'output',        # Generated reels storage
            'assets',        # Assets like backgrounds, fonts
            '.venv',         # Virtual environment
            '__pycache__'    # Python cache (will regenerate)
        }
        
        # FILES TO DEFINITELY DELETE (test files, demos, duplicates)
        self.delete_patterns = [
            # All test files
            'test_*.py',
            'demo_*.py',
            'debug_*.py',
            
            # Enhanced/broken versions
            'enhanced_*.py',
            '*_broken.py',
            '*_fixed.py',
            '*_v2.py',
            
            # Audio test files
            '*.mp3',
            
            # Analysis and temporary files
            'analyze_*.py',
            'cleanup_*.py',
            'safe_cleanup.py',
            
            # Duplicate main files
            'main*.py',
            'ultimate_*.py',
            'final_*.py',
            'integrated_*.py',
            'realistic_*.py',
            'parallel_*.py',
            
            # Single-purpose demos
            '*_demo.py',
            '*_test.py',
            'quick_*.py',
            'simple_*.py',
            'solution_*.py',
            'showcase_*.py',
            
            # Documentation drafts
            '*.md',  # Will keep README.md separately
            'FIX_*.md',
            'ENHANCED_*.md',
            'VIDEO_*.md',
            'COMPLETE_*.py',
            
            # Batch files
            '*.bat',
            
            # Old systems
            'accent_*.py',
            'gender_*.py',
            'voice_*.py',
            'engaging_*.py',
            'rss_*.py',
            'avatar_*.py',
            
            # Video experiments
            'video_*.py',
            
            # Old pipelines
            '*_pipeline.py',
            '*_service.py',
            '*_system.py',
            'create_*.py',
            'make_*.py',
            'run_*.py'
        ]
    
    def analyze_files(self):
        """Analyze current file structure"""
        print("🔍 ANALYZING CURRENT FILE STRUCTURE")
        print("=" * 50)
        
        all_files = []
        for root, dirs, files in os.walk(self.root_dir):
            if root.startswith('./.venv') or root.startswith('./output'):
                continue
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), self.root_dir)
                all_files.append(rel_path)
        
        print(f"📊 Total files found: {len(all_files)}")
        
        # Categorize files
        keep_files = []
        delete_files = []
        
        for file in all_files:
            filename = os.path.basename(file)
            directory = os.path.dirname(file)
            
            # Check if it's an essential file
            if filename in self.essential_files:
                keep_files.append(file)
                continue
            
            # Check if it's in an essential directory
            if any(dir_name in file for dir_name in self.essential_dirs):
                keep_files.append(file)
                continue
            
            # Check if it matches delete patterns
            should_delete = False
            for pattern in self.delete_patterns:
                if self.matches_pattern(filename, pattern):
                    should_delete = True
                    break
            
            if should_delete:
                delete_files.append(file)
            else:
                keep_files.append(file)
        
        return keep_files, delete_files
    
    def matches_pattern(self, filename, pattern):
        """Check if filename matches pattern"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def create_backup(self, files_to_delete):
        """Create backup of files before deletion"""
        backup_dir = f"cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        print(f"📦 Creating backup in: {backup_dir}")
        
        for file in files_to_delete:
            try:
                src_path = file
                dst_path = os.path.join(backup_dir, file)
                
                # Create directory structure in backup
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                if os.path.exists(src_path):
                    shutil.copy2(src_path, dst_path)
            except Exception as e:
                print(f"⚠️  Warning: Could not backup {file}: {e}")
        
        return backup_dir
    
    def delete_files(self, files_to_delete):
        """Delete unnecessary files"""
        deleted_count = 0
        failed_count = 0
        
        for file in files_to_delete:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    deleted_count += 1
                    print(f"🗑️  Deleted: {file}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Failed to delete {file}: {e}")
        
        return deleted_count, failed_count
    
    def cleanup_empty_dirs(self):
        """Remove empty directories"""
        removed_dirs = []
        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):  # Directory is empty
                        os.rmdir(dir_path)
                        removed_dirs.append(dir_path)
                        print(f"📁 Removed empty directory: {dir_path}")
                except:
                    pass  # Directory not empty or permission issue
        
        return removed_dirs
    
    def run_cleanup(self, create_backup_flag=True):
        """Run the complete cleanup process"""
        print("🧹 ULTIMATE CLEANUP STARTING")
        print("=" * 60)
        
        # Analyze files
        keep_files, delete_files = self.analyze_files()
        
        print()
        print("📊 CLEANUP ANALYSIS:")
        print(f"   ✅ Files to keep: {len(keep_files)}")
        print(f"   🗑️  Files to delete: {len(delete_files)}")
        print()
        
        # Show some examples of what will be deleted
        print("🗑️  EXAMPLES OF FILES TO DELETE:")
        for file in delete_files[:10]:  # Show first 10
            print(f"   • {file}")
        if len(delete_files) > 10:
            print(f"   ... and {len(delete_files) - 10} more files")
        
        print()
        print("✅ ESSENTIAL FILES TO KEEP:")
        essential_shown = [f for f in keep_files if os.path.basename(f) in self.essential_files]
        for file in essential_shown:
            print(f"   • {file}")
        
        # Create backup if requested
        backup_dir = None
        if create_backup_flag and delete_files:
            backup_dir = self.create_backup(delete_files)
        
        # Delete files
        print()
        print("🗑️  DELETING UNNECESSARY FILES...")
        deleted_count, failed_count = self.delete_files(delete_files)
        
        # Clean up empty directories
        print()
        print("📁 CLEANING UP EMPTY DIRECTORIES...")
        removed_dirs = self.cleanup_empty_dirs()
        
        # Final summary
        print()
        print("🎉 CLEANUP COMPLETE!")
        print("=" * 30)
        print(f"✅ Files deleted: {deleted_count}")
        print(f"❌ Failed deletions: {failed_count}")
        print(f"📁 Empty directories removed: {len(removed_dirs)}")
        if backup_dir:
            print(f"📦 Backup created in: {backup_dir}")
        
        print()
        print("🚀 REMAINING ESSENTIAL SYSTEM:")
        print("   • batch_todays_news_generator.py - Main news reel generator")
        print("   • show_reel_locations.py - File location manager")
        print("   • src/ - Core source code directory")
        print("   • output/ - Generated reels storage")
        print("   • assets/ - Media assets")
        print("   • requirements.txt - Dependencies")
        print("   • README.md - Documentation")
        
        return {
            'deleted': deleted_count,
            'failed': failed_count,
            'backup_dir': backup_dir,
            'removed_dirs': len(removed_dirs)
        }

def main():
    cleanup = UltimateCleanup()
    
    print("⚠️  WARNING: This will delete many files!")
    print("📦 A backup will be created before deletion.")
    print()
    
    # Run cleanup with backup
    results = cleanup.run_cleanup(create_backup_flag=True)
    
    print()
    print("✨ Your workspace is now clean and organized!")
    print("🎬 Ready to generate emotional news reels efficiently!")

if __name__ == "__main__":
    main()
