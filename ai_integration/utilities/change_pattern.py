# Import necessary libraries and modules
from PIL import Image
from ..utilities.change_background import change_background_white, change_background_transparent
from ..utilities.get_predections_yolo import get_predictions_hem, get_predictions_sleeves, get_predictions_torso
from ..utilities.color_processing import detect_major_color, blend_pattern_segments
from io import BytesIO
from django.core.files.base import ContentFile

# Function to convert a Pillow image to a Django ContentFile
def convert_pillow_image_to_django_file(pillow_image, image_format='PNG', image_name='image.png'):
    # Convert Pillow image to BytesIO object
    image_io = BytesIO()
    pillow_image.save(image_io, format=image_format)
    image_io.seek(0)
    # Create Django ContentFile from BytesIO object
    image_file = ContentFile(image_io.getvalue(), name=image_name)
    return image_file

# Function to generate a pattern across the entire image
def generate_wholepattern(img, pattern):
    img = Image.new("RGBA", (img.width, img.height), color=(0, 0, 0, 0))
    i, j = 0, 0
    while j < img.height:
        i = 0
        while i < img.width:
            img.paste(pattern, (i, j))
            i += pattern.width
            pattern = pattern.transpose(Image.FLIP_LEFT_RIGHT)
        pattern = pattern.transpose(Image.FLIP_TOP_BOTTOM)
        j += pattern.height
    return img

# Function to change the pattern on the main image with specified opacity
def change_pattern(main_img, pattern, opacity=1.0):
    # Get predictions for different segments in the main image
    pred_torso = get_predictions_torso(main_img)
    pred_skirt = get_predictions_hem(main_img)
    pred_left_sleeve, pred_right_sleeve = get_predictions_sleeves(main_img)

    segments = []
    # Append non-empty predictions to the segments list
    if pred_torso != None:
        segments.append(pred_torso)
    if pred_skirt != None:
        segments.append(pred_skirt)
    if pred_left_sleeve != None:
        segments.append(pred_left_sleeve)
    if pred_right_sleeve != None:
        segments.append(pred_right_sleeve)

    if len(segments) > 0:
        # Detect the major color of the main image
        detected_color = detect_major_color(main_img)

        # Generate a pattern across the entire main image
        pattern = generate_wholepattern(main_img, pattern)

        # Create a new image with a white background for pattern opacity
        white_background = Image.new('RGBA', pattern.size, (255, 255, 255, 255))

        # Blend the original image with the white background using the specified opacity
        opac_pattern = Image.blend(white_background, pattern, opacity)

        # Blend the pattern with the main image based on detected color and segments
        blended_pattern = blend_pattern_segments(main_img, detected_color, opac_pattern, segments)

        # Change the background color of the blended pattern to white
        blended_pattern = change_background_white(blended_pattern)

        # Convert the blended pattern to a Django ContentFile
        return convert_pillow_image_to_django_file(blended_pattern, 'PNG', 'fabric_image.png')
    else:
        # If no segments are detected, make the main image transparent
        main_img = change_background_transparent(main_img)
        # Convert the transparent main image to a Django ContentFile
        return convert_pillow_image_to_django_file(main_img, 'PNG', 'fabric_image.png')
