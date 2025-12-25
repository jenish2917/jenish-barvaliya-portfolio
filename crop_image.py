import os
from PIL import Image, ImageFilter, ImageEnhance
import sys

def create_professional_headshot(input_path, output_path):
    """
    Create a professional headshot crop from a full body/portrait image
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        width, height = img.size
        
        # Create a square crop focused on the upper portion (where face typically is)
        # For a professional headshot, we want roughly the top 60% of the image
        crop_size = min(width, height)
        
        # Calculate crop box for a professional headshot
        # Focus on upper portion where the face would be
        left = (width - crop_size) // 2
        top = int(height * 0.1)  # Start from 10% down from top
        right = left + crop_size
        bottom = top + crop_size
        
        # Ensure we don't go beyond image boundaries
        if bottom > height:
            bottom = height
            top = bottom - crop_size
        
        # Crop the image
        cropped = img.crop((left, top, right, bottom))
        
        # Resize to a standard profile picture size (400x400)
        cropped = cropped.resize((400, 400), Image.Resampling.LANCZOS)
        
        # Enhance the image for better appearance
        # Slightly increase brightness and contrast
        enhancer = ImageEnhance.Brightness(cropped)
        cropped = enhancer.enhance(1.1)
        
        enhancer = ImageEnhance.Contrast(cropped)
        cropped = enhancer.enhance(1.05)
        
        enhancer = ImageEnhance.Color(cropped)
        cropped = enhancer.enhance(1.1)
        
        # Apply subtle sharpening
        cropped = cropped.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
        
        # Save the processed image
        cropped.save(output_path, 'JPEG', quality=95, optimize=True)
        print(f"Professional headshot created: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

if __name__ == "__main__":
    input_image = r"d:\jenish barvaliya - portfolio\backend\media\profile\profile.jpg"
    output_image = r"d:\jenish barvaliya - portfolio\backend\media\profile\profile_headshot.jpg"
    
    if os.path.exists(input_image):
        success = create_professional_headshot(input_image, output_image)
        if success:
            print("✅ Professional headshot created successfully!")
        else:
            print("❌ Failed to create professional headshot")
    else:
        print(f"❌ Input image not found: {input_image}")
