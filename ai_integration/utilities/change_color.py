from PIL import Image
import numpy as np
from collections import Counter
from rembg import remove
from sklearn.cluster import KMeans
from ..utilities.change_background import change_background_white
from ..utilities.color_processing import detect_major_color, blend_new_color
import copy

def change_colors(img, new_color):
    new_img = copy.deepcopy(img)

    #Identify major color of the object 
    detected_color = detect_major_color(new_img)

    #Changing the major color of object
    changed_color_img = blend_new_color(new_img, detected_color, new_color)

    #Changing backgrount to white
    changed_color_img = change_background_white(changed_color_img)

    # changed_color_img.show()
    return changed_color_img

