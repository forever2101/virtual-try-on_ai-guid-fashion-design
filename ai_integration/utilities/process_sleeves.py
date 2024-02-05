# Import necessary modules and functions from utility modules
import copy
import random
from ..utilities.get_predections_yolo import get_predictions_torso
from ..utilities.swap_sleeve import swap_sleeve, swap_sleeve_from_sleeveless
from ..utilities.generate_dalle3_vairants import gen_dalle_vairant_sleeve
from ..utilities.sleeves_segment_processing import to_sleeveless
from ..utilities.get_predections_yolo import get_predictions_sleeves
from ..utilities.generate_dalle_inpainting import generate_inpainting_neck
from ..utilities.change_background import change_background_white

# Function to process and swap the sleeves of a given image
def process_sleeve(img, sleeve_type, sub_type):
    # Create a deep copy of the original image and convert it to RGBA mode
    new_img = copy.deepcopy(img).convert('RGBA')

    # Check if the desired sleeve type is sleeveless and not the same as the sub-type
    if sleeve_type == 'sleeveless' and sleeve_type != sub_type:
        # Get torso predictions from the original image
        pred_torso = get_predictions_torso(img)

        # Generate a sleeve variant for the specified sub-type
        generated_var = gen_dalle_vairant_sleeve(new_img, sub_type)

        # Swap the sleeves from sleeveless to the generated variant
        swapped_sleeves = swap_sleeve_from_sleeveless(new_img, generated_var)
        return swapped_sleeves

    # Check if the desired sleeve type is cap-length and not the same as the sub-type
    elif sleeve_type == 'cap-length' and sleeve_type != sub_type:
        # Check if the sub-type is sleeveless
        if sub_type == 'sleeveless':
            # Get predictions for left and right sleeves
            left_sleeve, right_sleeve = get_predictions_sleeves(new_img)

            # Convert the dress to sleeveless using the detected sleeves
            mask = to_sleeveless(new_img, left_sleeve, right_sleeve)

            # Generate an inpainting for the sleeveless transformation
            prompt = f'Change this dress sleeve to sleeveless.'
            mask = mask.convert('RGBA')
            inpainting = generate_inpainting_neck(mask, prompt)

            # Change the background to white and return the result
            return change_background_white(inpainting)
        else:
            # Generate a sleeve variant for the specified sub-type
            generated_var = gen_dalle_vairant_sleeve(new_img, sub_type)

            # Swap the sleeves using the generated variant
            if generated_var is not None:
                swapped_sleeves = swap_sleeve(new_img, generated_var)
                return swapped_sleeves

    # Check if the desired sleeve type is elbow-length and not the same as the sub-type
    elif (sleeve_type == 'elbow-length' or sleeve_type == 'elbow-length1') and sleeve_type != sub_type:
        # Check if the sub-type is sleeveless
        if sub_type == 'sleeveless':
            # Get predictions for left and right sleeves
            left_sleeve, right_sleeve = get_predictions_sleeves(new_img)

            # Convert the dress to sleeveless using the detected sleeves
            mask = to_sleeveless(new_img, left_sleeve, right_sleeve)

            # Generate an inpainting for the sleeveless transformation
            prompt = f'Change this dress sleeve to sleeveless.'
            mask = mask.convert('RGBA')
            inpainting = generate_inpainting_neck(mask, prompt)

            # Change the background to white and return the result
            return change_background_white(inpainting)
        else:
            # Generate a sleeve variant for the specified sub-type
            generated_var = gen_dalle_vairant_sleeve(new_img, sub_type)

            # Swap the sleeves using the generated variant
            if generated_var is not None:
                swapped_sleeves = swap_sleeve(new_img, generated_var)
                return swapped_sleeves

    # Check if the desired sleeve type is full-length and not the same as the sub-type
    elif sleeve_type == 'full-length' and sleeve_type != sub_type:
        # Check if the sub-type is sleeveless
        if sub_type == 'sleeveless':
            # Get predictions for left and right sleeves
            left_sleeve, right_sleeve = get_predictions_sleeves(new_img)

            # Convert the dress to sleeveless using the detected sleeves
            mask = to_sleeveless(new_img, left_sleeve, right_sleeve)

            # Generate an inpainting for the sleeveless transformation
            prompt = f'Change this dress sleeve to sleeveless.'
            mask = mask.convert('RGBA')
            inpainting = generate_inpainting_neck(mask, prompt)

            # Change the background to white and return the result
            return change_background_white(inpainting)
        else:
            # Generate a sleeve variant for the specified sub-type
            generated_var = gen_dalle_vairant_sleeve(new_img, sub_type)

            # Swap the sleeves using the generated variant
            if generated_var is not None:
                swapped_sleeves = swap_sleeve(new_img, generated_var)
                return swapped_sleeves

    # Return None if the sleeve type and sub-type are the same or other cases
    else:
        return None
