import os
from PIL import Image
from itertools import product

 

def tile(filename, dir_in, dir_out, nb_w, nb_h):
#def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    wd =  w // nb_w 
    hd =  h // nb_h 
    
    grid = product(range(0, h-h%hd, hd), range(0, w-w%wd, wd))
    for i, j in grid:
        box = (j, i, j+hd, i+wd)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)


file_name="frog-set3.png"
dir_name="/home/nathalie/Downloads/set"
nb_breit=4
nb_hoch=4
tile(file_name,dir_name,dir_name,nb_breit,nb_hoch)