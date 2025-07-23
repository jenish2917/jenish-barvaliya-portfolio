"""
Showcase Video Quality Analysis Tool for Daily News Reels
This script generates a comprehensive quality report for news reel videos
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from services.video_analyzer import VideoAnalyzer

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                   📊 VIDEO QUALITY ANALYSIS SHOWCASE 🎬                      ║
    ║                                                                              ║
    ║                  Analyze News Reels for Quality and Issues                   ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize analyzer
    analyzer = VideoAnalyzer()
    
    # Path to videos
    videos_dir = os.path.join(os.path.dirname(__file__), 'reels')
    output_dir = os.path.join(videos_dir, "showcase_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all video files
    video_files = []
    for ext in ['.mp4', '.avi', '.mov', '.mkv']:
        video_files.extend(list(Path(videos_dir).glob(f"*{ext}")))
    
    if not video_files:
        print(f"❌ No video files found in {videos_dir}")
        return
    
    print(f"📊 Found {len(video_files)} video files to analyze")
    print("=" * 60)
    
    # Batch analyze videos
    results = analyzer.batch_analyze_videos(videos_dir, output_dir)
    
    if not results:
        print("❌ No videos could be analyzed")
        return
    
    # Generate HTML report
    html_report = generate_html_report(results, output_dir)
    
    print("\n✅ Analysis complete!")
    print(f"📊 Analyzed {len(results)} videos")
    print(f"📄 Full report: {html_report}")
    
    # Show summary
    print("\n📊 QUALITY SUMMARY:")
    print("=" * 60)
    
    # Calculate averages
    avg_overall = sum(v.overall_quality_score for v in results.values()) / len(results)
    avg_video = sum(v.overall_video_score for v in results.values()) / len(results)
    avg_audio = sum(v.overall_audio_score for v in results.values()) / len(results)
    
    print(f"🎥 Average Video Quality: {avg_video:.1f}%")
    print(f"🔊 Average Audio Quality: {avg_audio:.1f}%")
    print(f"✨ Overall Quality Score: {avg_overall:.1f}%")
    
    # Show top issues
    all_recommendations = []
    for metrics in results.values():
        all_recommendations.extend(metrics.recommendations)
    
    # Count recommendation frequency
    rec_count = {}
    for rec in all_recommendations:
        rec_count[rec] = rec_count.get(rec, 0) + 1
    
    # Sort by frequency
    top_issues = sorted(rec_count.items(), key=lambda x: x[1], reverse=True)
    
    print("\n🔍 TOP ISSUES DETECTED:")
    print("=" * 60)
    for issue, count in top_issues[:5]:
        percentage = (count / len(results)) * 100
        print(f"• {issue} ({percentage:.0f}% of videos)")

def generate_html_report(results, output_dir):
    """Generate an HTML report for the analyzed videos"""
    report_path = os.path.join(output_dir, f"video_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    
    # Start HTML content
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>News Reels Quality Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; }}
            h2 {{ color: #3498db; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-top: 30px; }}
            .video-card {{ background: white; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 20px; overflow: hidden; }}
            .video-header {{ padding: 10px 15px; background: #f8f9fa; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; }}
            .video-content {{ padding: 15px; }}
            .scores {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px; }}
            .score-card {{ padding: 10px; border-radius: 5px; flex: 1; min-width: 120px; text-align: center; }}
            .high {{ background: #d4edda; color: #155724; }}
            .medium {{ background: #fff3cd; color: #856404; }}
            .low {{ background: #f8d7da; color: #721c24; }}
            .recommendations {{ background: #e2e3e5; padding: 10px; border-radius: 5px; margin-top: 15px; }}
            .recommendations ul {{ margin: 5px 0; padding-left: 25px; }}
            .summary {{ background: #cce5ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .charts {{ display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px; }}
            .chart {{ flex: 1; min-width: 300px; height: 250px; border: 1px solid #ddd; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>News Reels Video Quality Analysis</h1>
            <div class="summary">
                <h2>Analysis Summary</h2>
                <p><strong>Total Videos Analyzed:</strong> {total_videos}</p>
                <p><strong>Average Overall Quality:</strong> {avg_quality:.1f}%</p>
                <p><strong>Analysis Date:</strong> {date}</p>
            </div>
            
            <h2>Video Details</h2>
    """
    
    # Fill in summary values
    html = html.format(
        total_videos=len(results),
        avg_quality=sum(v.overall_quality_score for v in results.values()) / len(results) if results else 0,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Add each video
    for video_path, metrics in results.items():
        video_name = os.path.basename(video_path)
        
        # Determine score classes
        overall_class = "high" if metrics.overall_quality_score >= 75 else "medium" if metrics.overall_quality_score >= 50 else "low"
        video_class = "high" if metrics.overall_video_score >= 75 else "medium" if metrics.overall_video_score >= 50 else "low"
        audio_class = "high" if metrics.overall_audio_score >= 75 else "medium" if metrics.overall_audio_score >= 50 else "low"
        
        html += f"""
            <div class="video-card">
                <div class="video-header">
                    <h3>{video_name}</h3>
                    <span>Duration: {metrics.duration:.1f}s</span>
                </div>
                <div class="video-content">
                    <div class="scores">
                        <div class="score-card {overall_class}">
                            <h4>Overall</h4>
                            <div style="font-size: 24px; font-weight: bold;">{metrics.overall_quality_score:.1f}%</div>
                        </div>
                        <div class="score-card {video_class}">
                            <h4>Video Quality</h4>
                            <div style="font-size: 24px; font-weight: bold;">{metrics.overall_video_score:.1f}%</div>
                        </div>
                        <div class="score-card {audio_class}">
                            <h4>Audio Quality</h4>
                            <div style="font-size: 24px; font-weight: bold;">{metrics.overall_audio_score:.1f}%</div>
                        </div>
                    </div>
                    
                    <p><strong>Resolution:</strong> {metrics.resolution[0]}x{metrics.resolution[1]} | <strong>FPS:</strong> {metrics.fps:.1f} | <strong>Bitrate:</strong> {metrics.bitrate:.2f} Mbps</p>
                    
                    <h4>Technical Metrics</h4>
                    <ul>
                        <li>Clarity: {metrics.clarity_score:.1f}%</li>
                        <li>Brightness: {metrics.brightness_score:.1f}%</li>
                        <li>Contrast: {metrics.contrast_score:.1f}%</li>
                        <li>Avatar Detection: {metrics.avatar_detection_score:.1f}%</li>
                        <li>Speech Quality: {metrics.speech_quality_score:.1f}%</li>
                    </ul>
                    
                    <div class="recommendations">
                        <h4>Recommendations:</h4>
                        <ul>
        """
        
        for rec in metrics.recommendations:
            html += f"<li>{rec}</li>"
        
        html += """
                        </ul>
                    </div>
                </div>
            </div>
        """
    
    # Close HTML
    html += """
        </div>
    </body>
    </html>
    """
    
    # Write HTML to file
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return report_path

if __name__ == "__main__":
    main()
