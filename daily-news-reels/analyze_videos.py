"""
Test script to analyze video quality using the VideoAnalyzer
"""
import os
import sys
import json
import numpy as np
from pathlib import Path

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Custom JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

from services.video_analyzer import VideoAnalyzer

def main():
    print("=" * 50)
    print("Video Quality Analysis Tool")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = VideoAnalyzer()
    
    # Path to videos
    videos_dir = os.path.join(os.path.dirname(__file__), 'reels')
    
    if not os.path.exists(videos_dir):
        print(f"Error: Video directory not found: {videos_dir}")
        return
    
    # Find all video files
    video_files = []
    for ext in ['.mp4', '.avi', '.mov', '.mkv']:
        video_files.extend(list(Path(videos_dir).glob(f"*{ext}")))
    
    if not video_files:
        print(f"No video files found in {videos_dir}")
        return
    
    print(f"Found {len(video_files)} video files to analyze")
    print("-" * 50)
    
    # Create output directory
    output_dir = os.path.join(videos_dir, "analysis_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    # Analyze each video
    successful = 0
    for video_path in video_files[:3]:  # Limit to 3 for testing
        video_name = os.path.basename(video_path)
        print(f"Analyzing: {video_name}")
        
        try:
            # Analyze single video
            report_path = analyzer.generate_quality_report(str(video_path), output_dir)
            
            if report_path:
                print(f"✅ Report generated: {os.path.basename(report_path)}")
                successful += 1
            else:
                print(f"❌ Analysis failed for {video_name}")
        except Exception as e:
            print(f"❌ Error analyzing {video_name}: {e}")
    
    print("-" * 50)
    print(f"Analysis complete: {successful} out of {min(len(video_files), 3)} videos analyzed")
    print(f"Reports saved to: {output_dir}")

if __name__ == "__main__":
    main()
