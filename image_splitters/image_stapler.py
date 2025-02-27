# this file will be use to stapple an image over another nb_hoch time
# input : file_name
#         nb_hoch : stapple height

# output : 
#       nb_hoch-1 new image with 2,3,....nb_hoch stapple

import os
from PIL import Image

def staple(filename, dirname, fileoutputname, nbhoch, remove_top, remove_bottom, remove_left, remove_right):
    img_path = os.path.join(dirname, filename)
    img = Image.open(img_path)

    w, h = img.size  
    box = (remove_left, remove_top, w - remove_right, h - remove_bottom)

    # Crop the initial image based on the specified dimensions
    cropped_img = img.crop(box)

    # Get the cropped width and height for subsequent pasting
    width, height = cropped_img.size

    # Create a blank image to hold the stacked images
    stacked_image = Image.new("RGBA", (width, height * nbhoch))

    # Paste the cropped image onto the blank image
    #stacked_image.paste(cropped_img, (0, 0))
    stacked_image.paste(cropped_img, (0,  height * (nbhoch-1)))
    stacked_image.save(os.path.join(dirname, f'{fileoutputname}1.png'))

    # Loop through and paste subsequent cropped images vertically
    for i in range(2, nbhoch + 1):
        #stacked_image.paste(cropped_img, (0, height * (i - 1)))
        stacked_image.paste(cropped_img, (0, height * (nbhoch- i)))

        # Save the stacked image at each level
        stacked_image.save(os.path.join(dirname, f'{fileoutputname}{i}.png'))

file_name = "frog-black-set_100_400.png"
fileoutput_name = "frog-staple-black_"
dir_name = "/home/nathalie/Downloads/set"
nb_hoch = 10
remove_top = 0
remove_bottom = 0
remove_left = 0
remove_right = 0
staple(file_name, dir_name, fileoutput_name, nb_hoch, remove_top, remove_bottom, remove_left, remove_right)
