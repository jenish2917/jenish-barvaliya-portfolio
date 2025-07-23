# 📰 AI News-to-Reels Generator

Automatically convert today's news articles into engaging 30-60 second vertical video reels using AI. Perfect for creating content for Instagram Reels, YouTube Shorts, and TikTok.

## 🎯 Features

- **Smart News Fetching**: Gets today's headlines from multiple countries using NewsAPI
- **AI Summarization**: Uses Ollama with Qwen model for intelligent article summarization
- **Script Generation**: Creates engaging news anchor scripts optimized for short-form video
- **AI Voiceover**: Generates natural-sounding voiceovers using Google TTS
- **Video Creation**: Produces vertical 9:16 videos with text overlays and backgrounds
- **Batch Processing**: Handles multiple articles automatically
- **Multi-Country Support**: Fetch news from US, India, UK, and more

## 🏗️ Project Structure

```
daily-news-reels/
├── main.py                    # Main pipeline orchestrator
├── news_fetcher.py            # NewsAPI integration
├── summarizer.py              # Ollama/Qwen AI summarization
├── script_generator.py        # News script generation
├── tts_generator.py           # Text-to-speech voiceover
├── video_generator.py         # Video reel creation
├── config.env                 # Configuration file
├── requirements.txt           # Python dependencies
├── assets/                    # Background images and music
│   ├── default_bg.jpg
│   └── background_music.mp3
├── reels/                     # Output folder
│   └── YYYY-MM-DD/
│       ├── audio/            # Generated voiceovers
│       ├── videos/           # Final video reels
│       └── report.txt        # Pipeline summary
└── README.md
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **NewsAPI account** (free at https://newsapi.org/)

### Installation

1. **Clone or download this project**
   ```powershell
   cd d:\reel\daily-news-reels
   ```

2. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```powershell
   # Download from https://ollama.com/
   # After installation:
   ollama serve
   ollama pull qwen:latest
   ```

4. **Configure API keys**
   - Edit `config.env`
   - Replace `your_newsapi_key_here` with your actual NewsAPI key

### Running the Pipeline

```powershell
python main.py
```

## ⚙️ Configuration

Edit `config.env` to customize:

```env
# NewsAPI Configuration
NEWS_API_KEY=your_actual_newsapi_key_here

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen:latest

# Video Configuration
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
BACKGROUND_COLOR=(30, 30, 30)
```

### Customizing the Pipeline

Edit `main.py` to change:

```python
# Countries to fetch news from
countries = ['us', 'in', 'gb', 'ca', 'au']

# News categories
categories = ['general', 'technology', 'business', 'health']

# Specific topics to search for
topics = ['AI', 'technology', 'climate change']

# Number of articles per country
articles_per_country = 5
```

## 📋 Step-by-Step Process

1. **News Fetching** (`news_fetcher.py`)
   - Fetches today's top headlines from specified countries
   - Supports multiple categories and custom topics
   - Filters out articles without content

2. **AI Summarization** (`summarizer.py`)
   - Uses Ollama with Qwen model for intelligent summarization
   - Creates concise 3-5 sentence summaries
   - Optimized for video content

3. **Script Generation** (`script_generator.py`)
   - Converts summaries into natural news anchor scripts
   - Adds engaging hooks and call-to-actions
   - Optimized for 30-60 second videos

4. **Voiceover Creation** (`tts_generator.py`)
   - Generates natural-sounding speech using Google TTS
   - Supports multiple accents and languages
   - Optimizes text for better pronunciation

5. **Video Production** (`video_generator.py`)
   - Creates vertical 9:16 aspect ratio videos
   - Adds text overlays, backgrounds, and effects
   - Supports custom backgrounds from news images

## 🎬 Output

The pipeline generates:

- **Audio files**: High-quality MP3 voiceovers
- **Video files**: Vertical MP4 reels ready for social media
- **Report**: Summary of pipeline execution with statistics

Example output structure:
```
reels/2025-07-01/
├── audio/
│   ├── 001_AI_Technology_Breakthrough.mp3
│   ├── 002_Global_Climate_Summit.mp3
│   └── ...
├── videos/
│   ├── 001_AI_Technology_Breakthrough.mp4
│   ├── 002_Global_Climate_Summit.mp4
│   └── ...
└── report.txt
```

## 🔧 Troubleshooting

### Common Issues

1. **"NewsAPI key not configured"**
   - Get a free API key from https://newsapi.org/
   - Update `config.env` with your key

2. **"Ollama not running"**
   ```powershell
   ollama serve
   ollama pull qwen:latest
   ```

3. **"No articles found"**
   - Check your internet connection
   - Verify NewsAPI key is valid
   - Try different countries or categories

4. **Import errors**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Video generation fails**
   - Ensure MoviePy dependencies are installed
   - Check available disk space
   - Verify audio files were generated

### Testing Individual Components

Test each module independently:

```powershell
# Test news fetching
python news_fetcher.py

# Test AI summarization
python summarizer.py

# Test script generation
python script_generator.py

# Test voiceover generation
python tts_generator.py

# Test video creation
python video_generator.py
```

## 🎨 Customization Ideas

### Advanced Features
- **Multiple Languages**: Add translation support
- **Custom Backgrounds**: Use branded backgrounds or animations
- **Music Integration**: Add background music to videos
- **Hashtag Generation**: Auto-generate relevant hashtags
- **Social Media Upload**: Integrate with YouTube/Instagram APIs

### Scheduling
Run automatically using Windows Task Scheduler:
```powershell
# Create daily task
schtasks /create /tn "NewsReels" /tr "python d:\reel\daily-news-reels\main.py" /sc daily /st 08:00
```

## 📦 Dependencies

- **requests**: HTTP requests for APIs
- **gtts**: Google Text-to-Speech
- **moviepy**: Video processing
- **Pillow**: Image processing
- **ollama**: AI model integration
- **beautifulsoup4**: Web scraping utilities
- **python-dotenv**: Environment configuration

## 🤝 Contributing

Feel free to enhance this project:
- Add new TTS providers (ElevenLabs, Azure Speech)
- Implement custom video templates
- Add more news sources beyond NewsAPI
- Create web interface for easier configuration

## 📄 License

This project is for educational and personal use. Please respect:
- NewsAPI terms of service
- Content licensing for commercial use
- Third-party service rate limits

## 🎯 Target Audience

Perfect for:
- Content creators seeking automated news content
- Social media managers
- News enthusiasts wanting personalized summaries
- Developers learning AI pipeline integration

---

**Get started today and transform how you consume and share news!** 🚀
