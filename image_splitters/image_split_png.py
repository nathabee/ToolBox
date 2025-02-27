from PIL import Image
import os

def split_image(image_path, breite_length, breite_max_length, height_length, height_max_length):
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Convert breite and height ranges to pixel values based on the max lengths
    breite_splits = [(int(b[0] / breite_max_length * img_width), int(b[1] / breite_max_length * img_width)) for b in breite_length]
    height_splits = [(int(h[0] / height_max_length * img_height), int(h[1] / height_max_length * img_height)) for h in height_length]

    # Split and save each zone
    count = 0
    base_filename = os.path.splitext(image_path)[0]  # Remove extension from filename
    for h_start, h_end in height_splits:
        for b_start, b_end in breite_splits:
            # Crop the sub-image
            sub_img = img.crop((b_start, h_start, b_end, h_end))
            sub_img.save(f"{base_filename}_split_{count}.jpg")
            print(f"Saved: {base_filename}_split_{count}.jpg")
            count += 1

# Example usage
if __name__ == "__main__":
    image_path = "/home/nathalie/Downloads/tmp/papier1.jpg"  # Path to the PNG file

    # Define the splitting dimensions
    #breite_length = [(6, 23.7)]
    #breite_max_length = 30
    #height_length = [(0,11)]
    #height_max_length = 17.2
    breite_length = [(0, 28)]
    breite_max_length = 28
    height_length = [(0,12)]
    height_max_length = 20.5
    #breite_length = [(7, 30)]
    #breite_max_length = 37
    #height_length = [(2,8.7)]
    #height_max_length = 21.2

    split_image(image_path, breite_length, breite_max_length, height_length, height_max_length)
