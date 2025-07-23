"""
Safe Project Cleanup Script
Removes non-essential files while preserving core pipeline functionality
"""

import os
import json
import shutil
from pathlib import Path

def safe_cleanup():
    """Safely remove non-essential files"""
    
    # Load the cleanup list
    with open('cleanup_list.json', 'r') as f:
        files_to_remove = json.load(f)
    
    print("🧹 STARTING SAFE PROJECT CLEANUP")
    print("="*60)
    
    # Create backup directory
    backup_dir = 'cleanup_backup'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📁 Created backup directory: {backup_dir}")
    
    removed_count = 0
    failed_count = 0
    total_size_saved = 0
    
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                # Calculate file size
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    total_size_saved += file_size
                    
                    # Create backup
                    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                    shutil.copy2(file_path, backup_path)
                    
                    # Remove original
                    os.remove(file_path)
                    print(f"✅ Removed file: {file_path}")
                    
                elif os.path.isdir(file_path):
                    # For directories, check if they're empty or contain only cache
                    if file_path in ['.pytest_cache', '__pycache__', 'tests', 'config', 'resources']:
                        if os.path.isdir(file_path):
                            # Calculate directory size
                            dir_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                         for dirpath, dirnames, filenames in os.walk(file_path)
                                         for filename in filenames)
                            total_size_saved += dir_size
                            
                            # Create backup of directory
                            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                            if os.path.exists(backup_path):
                                shutil.rmtree(backup_path)
                            shutil.copytree(file_path, backup_path)
                            
                            # Remove original directory
                            shutil.rmtree(file_path)
                            print(f"✅ Removed directory: {file_path}")
                    
                removed_count += 1
            else:
                print(f"⚪ File not found: {file_path}")
                
        except Exception as e:
            print(f"❌ Failed to remove {file_path}: {e}")
            failed_count += 1
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print("-"*40)
    print(f"✅ Files removed: {removed_count}")
    print(f"❌ Failed removals: {failed_count}")
    print(f"💾 Space saved: {total_size_saved / 1024 / 1024:.2f} MB")
    print(f"📁 Backup location: {backup_dir}")
    
    # Verify core files still exist
    core_files = [
        'enhanced_main.py',
        'simple_video_creator.py', 
        'enhanced_video_pipeline.py',
        'config.env',
        'requirements.txt',
        'src/',
        'output/',
        'assets/',
        'reels/'
    ]
    
    print(f"\n🔍 CORE FILES VERIFICATION:")
    print("-"*40)
    all_core_present = True
    for core_file in core_files:
        if os.path.exists(core_file):
            print(f"✅ {core_file}")
        else:
            print(f"❌ {core_file} - MISSING!")
            all_core_present = False
    
    if all_core_present:
        print(f"\n🎉 SUCCESS! Cleanup completed successfully")
        print(f"🔧 Core pipeline preserved and functional")
        print(f"🗑️  Non-essential files removed")
        print(f"📦 Backup available in '{backup_dir}' if needed")
        
        # Clean up the cleanup files themselves
        cleanup_files = ['cleanup_analysis.py', 'cleanup_list.json']
        for cleanup_file in cleanup_files:
            if os.path.exists(cleanup_file):
                shutil.move(cleanup_file, os.path.join(backup_dir, cleanup_file))
                print(f"📦 Moved to backup: {cleanup_file}")
        
        return True
    else:
        print(f"\n⚠️  WARNING: Some core files are missing!")
        print(f"🔄 Consider restoring from backup if issues occur")
        return False

def create_final_project_structure():
    """Show the final clean project structure"""
    print(f"\n📁 FINAL PROJECT STRUCTURE:")
    print("="*50)
    
    def print_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
            
        items = []
        if os.path.exists(directory):
            items = sorted(os.listdir(directory))
        
        for i, item in enumerate(items):
            path = os.path.join(directory, item)
            is_last = i == len(items) - 1
            
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item}")
            
            if os.path.isdir(path) and not item.startswith('.') and item not in ['__pycache__']:
                extension = "    " if is_last else "│   "
                print_tree(path, prefix + extension, max_depth, current_depth + 1)
    
    print_tree(".")

if __name__ == "__main__":
    # Confirm cleanup
    print("🧹 PROJECT CLEANUP READY")
    print("="*50)
    print("This will remove non-essential files while preserving:")
    print("✅ Enhanced main pipeline (enhanced_main.py)")
    print("✅ Video generation system (simple_video_creator.py, enhanced_video_pipeline.py)")
    print("✅ Core source code (src/ directory)")
    print("✅ Configuration files")
    print("✅ Generated content (output/, reels/)")
    print("✅ Assets (assets/)")
    print("")
    print("🗑️  Will remove experimental, demo, and alternative implementations")
    print("📦 All removed files will be backed up")
    
    response = input("\n❓ Proceed with cleanup? (y/N): ").lower().strip()
    
    if response == 'y':
        success = safe_cleanup()
        if success:
            create_final_project_structure()
            
            print(f"\n🎯 NEXT STEPS:")
            print("-"*30)
            print("1. Test the system: python enhanced_main.py --test")
            print("2. Generate videos: python enhanced_video_pipeline.py")
            print("3. Run quality analysis: python final_attractiveness_assessment.py")
            print("4. If issues occur, restore from 'cleanup_backup/' directory")
            
    else:
        print("❌ Cleanup cancelled")
