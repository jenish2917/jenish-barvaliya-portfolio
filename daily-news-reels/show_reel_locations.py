"""
Show where your emotional news reels are saved
Lists all generated reels with their locations and details
"""

import os
from datetime import datetime
import json

def show_reel_locations():
    print("🎬 YOUR EMOTIONAL NEWS REELS LOCATIONS")
    print("=" * 60)
    
    # Main reels directory
    sessions_dir = "output/sessions"
    
    print(f"📁 Main Directory: {os.path.abspath(sessions_dir)}")
    print()
    
    if not os.path.exists(sessions_dir):
        print("❌ No reels directory found")
        return
    
    # Get all session directories (sorted by date, newest first)
    session_dirs = []
    for item in os.listdir(sessions_dir):
        session_path = os.path.join(sessions_dir, item)
        if os.path.isdir(session_path) and item.startswith("202"):
            session_dirs.append((item, session_path))
    
    session_dirs.sort(reverse=True)  # Newest first
    
    print(f"📊 Found {len(session_dirs)} total sessions")
    print()
    
    # Show recent emotional reels
    recent_reels = []
    
    for session_name, session_path in session_dirs[:10]:  # Show last 10 sessions
        audio_dir = os.path.join(session_path, "audio")
        
        if os.path.exists(audio_dir):
            audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
            
            if audio_files:
                # Parse session timestamp
                try:
                    session_dt = datetime.strptime(session_name, "%Y%m%d_%H%M%S")
                    date_str = session_dt.strftime("%B %d, %Y at %I:%M %p")
                except:
                    date_str = session_name
                
                print(f"🎬 Session: {session_name}")
                print(f"📅 Created: {date_str}")
                print(f"📁 Location: {os.path.abspath(audio_dir)}")
                
                for audio_file in audio_files:
                    file_path = os.path.join(audio_dir, audio_file)
                    file_size = os.path.getsize(file_path)
                    
                    # Extract reel info from filename
                    if "emotional_" in audio_file:
                        # It's an emotional reel
                        title_part = audio_file.replace("emotional_", "").replace("_emotional.mp3", "")
                        title_clean = title_part.replace("_", " ")[:50] + ("..." if len(title_part) > 50 else "")
                        
                        print(f"   🎤 {audio_file}")
                        print(f"   📰 Title: {title_clean}")
                        print(f"   💾 Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
                        
                        recent_reels.append({
                            'session': session_name,
                            'file': audio_file,
                            'path': file_path,
                            'size': file_size,
                            'title': title_clean
                        })
                print()
    
    # Summary of path structure
    print("🗂️  REEL STORAGE STRUCTURE")
    print("=" * 40)
    print("📁 output/")
    print("   📁 sessions/")
    print("      📁 YYYYMMDD_HHMMSS/")
    print("         📁 audio/")
    print("            🎵 emotional_[title]_[timestamp]_emotional.mp3")
    print("         📁 videos/")
    print("            🎬 [title].mp4 (if video generation enabled)")
    print()
    
    # Show today's reels specifically
    today = datetime.now().strftime("%Y%m%d")
    todays_reels = [r for r in recent_reels if r['session'].startswith(today)]
    
    if todays_reels:
        print(f"🎯 TODAY'S EMOTIONAL REELS ({len(todays_reels)} files)")
        print("=" * 40)
        for reel in todays_reels:
            print(f"🎤 {reel['file']}")
            print(f"   📰 {reel['title']}")
            print(f"   📁 {reel['path']}")
            print()
    
    # Quick access info
    print("🚀 QUICK ACCESS")
    print("=" * 20)
    print(f"📁 Open sessions folder: {os.path.abspath(sessions_dir)}")
    print("🎵 All audio files are in the 'audio' subfolder of each session")
    print("🎬 Video files (if generated) are in the 'videos' subfolder")
    print(f"📊 Total reels generated today: {len(todays_reels)}")
    
    if recent_reels:
        latest_reel = recent_reels[0]
        print(f"🆕 Latest reel: {latest_reel['file']}")
        print(f"📁 Latest reel path: {latest_reel['path']}")

if __name__ == "__main__":
    show_reel_locations()
