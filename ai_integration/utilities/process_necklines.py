# Import necessary modules and functions from utility modules
import random
from ..utilities.neckline_segment_processing import transparent_segment_neckline, round_neck_segment_neckline, v_neck_segment_neckline, crew_neck_segment_neckline, square_neck_segment_neckline
import copy
from ..utilities.get_predections_yolo import get_predictions_torso
from ..utilities.generate_dalle_inpainting import generate_inpainting_neck
from ..utilities.change_background import change_background_white

# Function to process and change the neckline of a given image
def process_neckline(img, neck_type, sub_neck):
    # Create a deep copy of the original image
    new_img = copy.deepcopy(img)

    # Initialize a flag to check if the neckline is high-neck
    is_high = False

    # Get predictions for torso using YOLO model
    pred_torso = get_predictions_torso(img)

    # Check if the desired neckline is high-neck and it is not the same as the sub-neck
    if neck_type == 'high-neck' and neck_type != sub_neck:
        is_high = True

        # Process different sub-neck types within high-neck
        if sub_neck == 'u-neck':
            mask_img = round_neck_segment_neckline(new_img, pred_torso, is_high)

        elif sub_neck == 'v-neck':
            mask_img = v_neck_segment_neckline(new_img, pred_torso, is_high)

        elif sub_neck == 'square-neck':
            mask_img = square_neck_segment_neckline(new_img, pred_torso, is_high)

        # Generate inpainting for the modified neckline
        prompt = f'Change the neckline of the dress to {neck_type}. do not add mannequin'
        inpainting_neck = generate_inpainting_neck(mask_img.convert('RGBA'), prompt)

        # Change the background of the inpainted image to white
        return change_background_white(inpainting_neck)

    # Process u-neck neckline if it is not the same as the sub-neck
    elif neck_type == 'u-neck' and neck_type != sub_neck:
        if sub_neck == 'v-neck':
            mask_img = v_neck_segment_neckline(new_img, pred_torso, is_high)

        elif sub_neck == 'square-neck':
            mask_img = square_neck_segment_neckline(new_img, pred_torso, is_high)

        # Generate inpainting for the modified neckline
        prompt = f'Change the neckline of the dress to {neck_type}. do not add mannequin'
        inpainting_neck = generate_inpainting_neck(mask_img.convert('RGBA'), prompt)

        # Change the background of the inpainted image to white
        return change_background_white(inpainting_neck)

    # Process v-neck neckline if it is not the same as the sub-neck
    elif neck_type == 'v-neck' and neck_type != sub_neck:
        if sub_neck == 'u-neck':
            mask_img = round_neck_segment_neckline(new_img, pred_torso, is_high)

        elif sub_neck == 'square-neck':
            mask_img = square_neck_segment_neckline(new_img, pred_torso, is_high)

        # Generate inpainting for the modified neckline
        prompt = f'Change the neckline of the dress to {neck_type}. do not add mannequin'
        inpainting_neck = generate_inpainting_neck(mask_img.convert('RGBA'), prompt)

        # Change the background of the inpainted image to white
        return change_background_white(inpainting_neck)

    # Process square-neck neckline if it is not the same as the sub-neck
    elif neck_type == 'square-neck' and neck_type != sub_neck:
        if sub_neck == 'u-neck':
            mask_img = round_neck_segment_neckline(new_img, pred_torso, is_high)

        elif sub_neck == 'v-neck':
            mask_img = v_neck_segment_neckline(new_img, pred_torso, is_high)

        # Generate inpainting for the modified neckline
        prompt = f'Change the neckline of the dress to {neck_type}. do not add mannequin'
        inpainting_neck = generate_inpainting_neck(mask_img.convert('RGBA'), prompt)

        # Change the background of the inpainted image to white
        return change_background_white(inpainting_neck)

    # Return None if the neckline type and sub-neck are the same or other cases
    else:
        return None
