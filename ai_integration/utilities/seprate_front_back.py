from PIL import Image
from ..utilities.change_background import change_background_white

def seprate_front_back(img):
    width, height = img.size
    half_width = width // 2

    left_section = img.crop((0, 0, half_width, height))
    right_section = img.crop((half_width, 0, width, height))

    # Chnage the background to white
    left_section = change_background_white(left_section)
    right_section = change_background_white(right_section)

    # left_section.show()
    # right_section.show()
    return left_section, right_section



if __name__=="__main__":
    input_image = 'test_images/front_back.jpeg'
    #Parsing input image path
    img = Image.open(input_image)

    front, back = seprate_front_back(img)
