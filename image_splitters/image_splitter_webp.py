from PIL import Image


def split_image(image_path, breite_length, breite_max_length, height_length, height_max_length):
    filename=f"{image_path}.webp"   #without webp extension
    img = Image.open(filename)
    img_width, img_height = img.size

    # Convert breite and height ranges to pixel values based on the max lengths
    breite_splits = [(int(b[0] / breite_max_length * img_width), int(b[1] / breite_max_length * img_width)) for b in breite_length]
    height_splits = [(int(h[0] / height_max_length * img_height), int(h[1] / height_max_length * img_height)) for h in height_length]

    # Split and save each zone
    count = 0
    for h_start, h_end in height_splits:
        for b_start, b_end in breite_splits:
            # Crop the sub-image
            sub_img = img.crop((b_start, h_start, b_end, h_end))
            sub_img.save(f"{image_path}_{count}.png")
            count += 1

# Example usage
#breite_length = [(1, 7.7), (8, 15), (15, 22)]
#breite_max_length = 23
#height_length = [(0.5, 6), (8, 13), (15, 20.5)]
#height_max_length = 23


breite_length = [(1, 7.7), (8, 15), (15, 22)]
breite_max_length = 23
height_length = [(0.5, 6), (8, 13), (15, 20.5)]
height_max_length = 23

name="/home/nathalie/Downloads/set/logo_eval3"   #without webp extension
split_image(name, breite_length, breite_max_length, height_length, height_max_length)
