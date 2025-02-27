from PIL import Image
import os

def combine_images(input_dir, output_dir, img1_name, img2_name, output_name):
    # Open the two images
    img1_path = os.path.join(input_dir, img1_name)
    img2_path = os.path.join(input_dir, img2_name)

    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Get the dimensions of the images
    img1_width, img1_height = img1.size
    img2_width, img2_height = img2.size

    # Create a new image with width = sum of both widths and max height
    new_img_width = img1_width + img2_width
    new_img_height = max(img1_height, img2_height)

    # Create a blank white canvas for the new image
    new_img = Image.new("RGB", (new_img_width, new_img_height), color=(255, 255, 255))

    # Paste the first image at the left
    new_img.paste(img1, (0, 0))

    # Paste the second image at the right
    new_img.paste(img2, (img1_width, 0))

    # Save the new image as JPEG
    output_path = os.path.join(output_dir, output_name)
    new_img.save(output_path, "JPEG")

    print(f"New image saved as {output_path}")

# Example usage:
input_directory = "/home/nathalie/Downloads/tmp/"  # Replace with actual input directory path
output_directory = "/home/nathalie/Downloads/tmp/"  # Replace with actual output directory path
img1_filename = "idnath1.png"
img2_filename = "idnath2.png"
output_filename = "combined_image.jpg"

combine_images(input_directory, output_directory, img1_filename, img2_filename, output_filename)
