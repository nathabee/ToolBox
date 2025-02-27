#pip install opencv-python pillow numpy


import cv2
import numpy as np
from PIL import Image, ImageEnhance

# def enhance_contrast(input_path, output_path, contrast_factor=1.5, brightness_offset=30):
def enhance_contrast(input_path, output_path, contrast_factor=1.2, brightness_offset=20):
    # Load the image using OpenCV
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    
    # Convert to grayscale for better contrast adjustment
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast by applying a scaling factor
    adjusted = cv2.convertScaleAbs(gray, alpha=contrast_factor, beta=brightness_offset)
    
    # Thresholding to make the lighter grays turn white
    _, thresh = cv2.threshold(adjusted, 200, 255, cv2.THRESH_BINARY)
    
    # Convert back to color (optional, depending on your needs)
    cleaned_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    
    # Save the result
    cv2.imwrite(output_path, cleaned_image)
    
    print(f"Enhanced image saved as: {output_path}")

# Usage 
input_path = '/home/nathalie/Downloads/tmp/image_split_0.png'  # Your input file path
output_path = '/home/nathalie/Downloads/tmp/cleaned_scan.jpg'  # Where to save the output
enhance_contrast(input_path, output_path)
