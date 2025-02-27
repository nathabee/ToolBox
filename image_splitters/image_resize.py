import os
from PIL import Image

def compress_image(input_dir, output_dir, filename, target_size):
    # Ensure target size is in bytes
    if target_size.lower().endswith('m'):
        target_size_bytes = int(target_size[:-1]) * 1024 * 1024
    elif target_size.lower().endswith('k'):
        target_size_bytes = int(target_size[:-1]) * 1024
    else:
        raise ValueError("Target size must end with 'M' or 'K' for megabytes or kilobytes, respectively.")

    # Construct the full input path
    input_path = os.path.join(input_dir, filename)
    
    # Open the image
    img = Image.open(input_path)
    
    # Reduce the image quality to meet the target size
    quality = 95  # Start with high quality
    while True:
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_{target_size}.jpeg")
        img.save(output_path, format='JPEG', quality=quality)
        
        # Check the file size
        if os.path.getsize(output_path) <= target_size_bytes:
            break
        
        # Reduce the quality
        quality -= 5
        if quality < 10:  # Prevent quality from going too low
            raise ValueError("Cannot reduce image to target size without dropping quality below acceptable levels.")
    
    print(f"Image saved to {output_path}")

# Example usage
# input_directory = '/home/nathalie/coding/project/site/naturgarten/assets'
input_directory = '/home/nathalie/Downloads/'
output_directory = '/home/nathalie/Downloads/'
#filename = 'Fruehling.jpg'
filename = 'wasserpesternte.jpg'
# 
target_size = '500K'  # Target size in Kilobytes



#ackerhummel.jpg  fliege.jpg        marienkaefer.jpg  teich.jpg     winghase.png
#beebot.ico       frog              mp3               terassen.jpg
#bee.png          gartenhummel.jpg  quitten.jpg       video
#erdhummel.jpg    kiwipergola.jpg   rittersporn.jpg   wanzen.jpg


compress_image(input_directory, output_directory, filename, target_size)
