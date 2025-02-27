import cv2
import numpy as np
from PIL import Image
import argparse
import os
import json


def get_dominant_color_range(image, tolerance=30):
    """Extracts the dominant color range from an image, using either a reference file or the top-left 10% region."""
    if image is None:
        raise ValueError("Error: Could not open or read the reference image.")
    
    height, width, _ = image.shape
    region = image[:height // 10, :width // 10]  # Extract the top-left 10% region
    
    # Convert to HSV for better color detection
    region_hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    
    # Get the average color in HSV
    avg_color = np.mean(region_hsv.reshape(-1, 3), axis=0)
    avg_hue = avg_color[0]  # Hue component
    
    # Define dynamic hue range based on the extracted dominant color
    lower_hue = max(avg_hue - tolerance, 0)
    upper_hue = min(avg_hue + tolerance, 179)
    
    lower_color = np.array([lower_hue, 50, 50], dtype=np.uint8)
    upper_color = np.array([upper_hue, 255, 255], dtype=np.uint8)
    
    return lower_color, upper_color

def remove_background_using_reference(reference_path, input_path, tolerance=30):
    # Load input image
    input_image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if input_image is None:
        raise ValueError(f"Error: Could not open or read the input image '{input_path}'.")
    
    if reference_path and os.path.exists(reference_path):
        ref_image = cv2.imread(reference_path)
        if ref_image is None:
            print(f"Warning: Could not open reference image '{reference_path}'. Falling back to top-left region of the input image.")
            lower_color, upper_color = get_dominant_color_range(input_image, tolerance)
        else:
            lower_color, upper_color = get_dominant_color_range(ref_image, tolerance)
    else:
        print("Warning: No reference image provided. Falling back to top-left region of the input image.")
        lower_color, upper_color = get_dominant_color_range(input_image, tolerance)
    
    # Convert input image to HSV
    input_hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    
    # Create mask to detect the dominant background color
    mask = cv2.inRange(input_hsv, lower_color, upper_color)
    
    # Convert input image to RGBA (ensure alpha channel is present)
    if input_image.shape[-1] == 3:
        input_rgba = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGBA)
    else:
        input_rgba = input_image.copy()
    
    # Ensure fully transparent pixels are white in RGB (avoids black edges in styling tool)
    input_rgba[mask == 255, :3] = [255, 255, 255]  # Set transparent areas to white
    input_rgba[:, :, 3] = 255 - mask  # Apply transparency to detected background
    
    # Convert to PIL Image
    pil_image = Image.fromarray(input_rgba)
    
    # Define output path with _transparent.png extension
    base_name, _ = os.path.splitext(input_path)
    output_path = f"{base_name}_transparent.png"
    
    # Save the final image
    pil_image.save(output_path)
    
    print(f"Processed image saved as: {output_path}")
    
    return output_path


def resize_image(input_path, size_label):
    sizes = {
        "S": 150,
        "M": 300,
        "L": 600,
        "XL": 1200,
        "XXL": 2400
    }
    if size_label not in sizes:
        raise ValueError("Invalid size label. Choose from S, M, L, XL, XXL")
    
    max_size = sizes[size_label]
    image = Image.open(input_path)
    width, height = image.size
    
    # Keep aspect ratio
    if width > height:
        new_width = max_size
        new_height = int((height / width) * max_size)
    else:
        new_height = max_size
        new_width = int((width / height) * max_size)
    
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    base_name, _ = os.path.splitext(input_path)
    output_path = f"{base_name}_resized.png"
    resized_image.save(output_path)
    
    print(f"Resized image saved as: {output_path}")
    return output_path

def process_image(input_path, brightness=255, edge_threshold1=100, edge_threshold2=200, contour_color=(0, 0, 0)):
    """Extract edges from an image and save as transparent PNG."""
    image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Error: Could not open or read the image '{input_path}'. Ensure it is a valid image file.")
    
    gray = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, edge_threshold1, edge_threshold2)
    edges = cv2.bitwise_not(edges)
    
    transparent_img = np.zeros((edges.shape[0], edges.shape[1], 4), dtype=np.uint8)
    transparent_img[:, :, 3] = 255 - edges  # Alpha channel, ensuring transparency for non-edges
    for i in range(3):
        transparent_img[:, :, i] = (edges * (contour_color[i] / 255)).astype(np.uint8)
    
    pil_image = Image.fromarray(transparent_img)
    base_name, _ = os.path.splitext(input_path)
    output_path = f"{base_name}_edge.png"
    pil_image.save(output_path)
    
    print(f"Processed image saved as: {output_path}")
    return output_path

def main(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    background_params = config.get("background")
    styling_params = config.get("styling")
    resize_params = config.get("resize")
    
    if background_params:
        reference_path = background_params.get("reference", None)
        output_path = remove_background_using_reference(reference_path, background_params["input"], background_params.get("tolerance", 30))
        if resize_params:
            output_path = resize_image(output_path, resize_params.get("size", "M"))
        if styling_params:
            color_tuple = tuple(map(int, styling_params.get("color", "0,0,0").split(',')))
            process_image(output_path, styling_params.get("brightness", 255), styling_params.get("threshold1", 100), styling_params.get("threshold2", 200), color_tuple)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image processing tool using JSON configuration.")
    parser.add_argument("config", type=str, help="Path to JSON configuration file")
    
    args = parser.parse_args()
    main(args.config)
