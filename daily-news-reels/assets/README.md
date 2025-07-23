# Assets Folder

This folder contains media assets used in video generation:

## Files

- `default_bg.jpg` - Default background image for video reels (1080x1920, 9:16 aspect ratio)
- `background_music.mp3` - Optional background music for video reels (not implemented yet)

## Custom Assets

You can add your own:

1. **Background Images**: Place `.jpg` or `.png` files here
   - Recommended size: 1080x1920 pixels (9:16 aspect ratio)
   - Use high-quality images for best results

2. **Background Music**: Place `.mp3` files here  
   - Keep volume low for voice clarity
   - Recommended length: 60+ seconds for looping

## Usage

The video generator will:
1. First try to use the news article's image (if available)
2. Fall back to `default_bg.jpg` if no article image
3. Create a solid color background as final fallback

Custom backgrounds can be specified programmatically in the video generator.
