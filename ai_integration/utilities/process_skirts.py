# Import necessary modules and functions from utility modules
import random 
import copy 
from ..utilities.generate_dalle3_vairants import gen_dalle_vairant_skirt
from ..utilities.swap_skirt import swap_skirt

# Function to process and swap the skirt of a given image
def process_skirt(img, skirt_length, sub_type):
    # Create a deep copy of the original image
    new_img = copy.deepcopy(img)

    # Check if the desired skirt length is full-length and not the same as the sub-type
    if skirt_length == 'full-length' and skirt_length != sub_type:
        # Process different sub-types within full-length skirt
        if sub_type == 'knee-length':
            ratio = 0.55
            org_img2_skirt_variant = gen_dalle_vairant_skirt(new_img, skirt_length)

            # Check if the generated skirt variant is not None
            if org_img2_skirt_variant is not None:
                # Swap the original skirt with the generated variant using the specified ratio
                swapped_skirt = swap_skirt(new_img, org_img2_skirt_variant, ratio)
                return swapped_skirt

        elif sub_type == 'mini-length':
            ratio = 0.4
            org_img2_skirt_variant = gen_dalle_vairant_skirt(new_img, skirt_length)

            # Check if the generated skirt variant is not None
            if org_img2_skirt_variant is not None:
                # Swap the original skirt with the generated variant using the specified ratio
                swapped_skirt = swap_skirt(new_img, org_img2_skirt_variant, ratio)
                return swapped_skirt

    # Check if the desired skirt length is mini-length and not the same as the sub-type
    elif skirt_length == 'mini-length' and skirt_length != sub_type:
        # Process different sub-types within mini-length skirt
        if sub_type == 'knee-length':
            ratio = 1.25
            org_img2_skirt_variant = gen_dalle_vairant_skirt(new_img, skirt_length)

            # Check if the generated skirt variant is not None
            if org_img2_skirt_variant is not None:
                # Swap the original skirt with the generated variant using the specified ratio
                swapped_skirt = swap_skirt(new_img, org_img2_skirt_variant, ratio)
                return swapped_skirt

        elif sub_type == 'full-length':
            ratio = 2.5
            org_img2_skirt_variant = gen_dalle_vairant_skirt(new_img, skirt_length)

            # Check if the generated skirt variant is not None
            if org_img2_skirt_variant is not None:
                # Swap the original skirt with the generated variant using the specified ratio
                swapped_skirt = swap_skirt(new_img, org_img2_skirt_variant, ratio)
                return swapped_skirt

    # Check if the desired skirt length is knee-length and not the same as the sub-type
    elif skirt_length == 'knee-length' and skirt_length != sub_type:
        # Process different sub-types within knee-length skirt
        if sub_type == 'full-length':
            ratio = 2
            org_img2_skirt_variant = gen_dalle_vairant_skirt(new_img, skirt_length)

            # Check if the generated skirt variant is not None
            if org_img2_skirt_variant is not None:
                # Swap the original skirt with the generated variant using the specified ratio
                swapped_skirt = swap_skirt(new_img, org_img2_skirt_variant, ratio)
                return swapped_skirt

        elif sub_type == 'mini-length':
            ratio = 0.75
            org_img2_skirt_variant = gen_dalle_vairant_skirt(new_img, skirt_length)

            # Check if the generated skirt variant is not None
            if org_img2_skirt_variant is not None:
                # Swap the original skirt with the generated variant using the specified ratio
                swapped_skirt = swap_skirt(new_img, org_img2_skirt_variant, ratio)
                return swapped_skirt

    # Return None if the skirt length and sub-type are the same or other cases
    else:
        return None
