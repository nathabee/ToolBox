# this file will be use to stapple an image over another nb_hoch time
# input : file_name
#         nb_hoch : stapple height

# output : 
#       nb_hoch-1 new image with 2,3,....nb_hoch stapple

import os
from PIL import Image

def staplelist(filenamelist, dirname, fileoutputname, nbhoch, remove_top, remove_bottom, remove_left, remove_right):
    img_path = os.path.join(dirname, filenamelist[0])
    img = Image.open(img_path)

    w, h = img.size  
    box = (remove_left, remove_top, w - remove_right, h - remove_bottom)

    # Crop the initial image based on the specified dimensions
    cropped_img = img.crop(box)

    # Get the cropped width and height for subsequent pasting
    width, height = cropped_img.size

    # Create a blank image to hold the stacked images
    stacked_image = Image.new("RGBA", (width, height * nbhoch))
    

    i = 1

    for filename in filenamelist :
        if i == nbhoch + 1 :
            return
        
        img_path = os.path.join(dirname, filename )
        img = Image.open(img_path)
        cropped_img = img.crop(box)
 

        # L paste subsequent cropped images vertically
        stacked_image.paste(cropped_img, (0, height * (nbhoch- i)))

        # Save the stacked image at each level
        stacked_image.save(os.path.join(dirname, f'{fileoutputname}{i}.png'))
        
        i += 1



filenamelist = [
"frog-black-set_400_300.png",
"frog-black-set_300_300.png",
"frog-black-set_0_200.png",
"frog-black-set_0_400.png",
"frog-black-set_100_200.png",
"frog-black-set_100_300.png",
"frog-black-set_200_100.png",
"frog-black-set_200_300.png",
"frog-black-set_300_100.png",
"frog-black-set_400_100.png" ]

fileoutput_name = "frog-staple-black_"
dir_name = "/home/nathalie/Downloads/set"
nb_hoch = 10
remove_top = 0
remove_bottom = 0
remove_left = 0
remove_right = 0
staplelist(filenamelist, dir_name, fileoutput_name, nb_hoch, remove_top, remove_bottom, remove_left, remove_right)
