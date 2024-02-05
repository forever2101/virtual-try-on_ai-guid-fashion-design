from rembg import remove

def change_background_white(img):
    # Remove the image background using the rembg library
    return remove(img, bgcolor=(255, 255, 255, 255))

def change_background_transparent(img):
    # Remove the image background using the rembg library
    return remove(img)