# Import necessary modules and functions
from PIL import Image
from ..utilities.get_predections_yolo import get_predictions_sleeves, get_predictions_torso
from ..utilities.rgba_to_rgb import rgba_to_rgb
from ..utilities.segment_processing import remove_segment, extract_segmented_area
from ..utilities.sleeves_segment_processing import blend_segment_sleeves, blend_segment_sleeves_from_torso
from ..utilities.change_background import change_background_white
from ..utilities.color_processing import detect_major_color_segment, blend_new_color
import copy

# Function to check and swap sleeves if necessary
def check_sleeve(left, right):
    # Extract X and Y coordinates of the left sleeve
    left_xy = left.xy[0]

    # Separate X and Y values into 1D arrays
    left_x_values = list(left_xy[:, 0])
    left_y_values = list(left_xy[:, 1])

    # Find min and max y values
    miny = min(left_y_values)
    maxy = max(left_y_values)

    # Find min and max x values
    minx = min(left_x_values)
    maxx = max(left_x_values)

    # Calculate X value at the minimum Y value
    x_at_miny = left_x_values[left_y_values.index(miny)]

    # Check if the sleeve is on the left side based on its position
    if x_at_miny < (maxx + minx) / 2:
        return left, right
    else:
        return right, left

# Function to swap sleeves between the original and reference images
def swap_sleeve(org_img, ref_img):
    # Convert original and reference images to RGB
    org_torso = get_predictions_torso(org_img)
    ref_torso = get_predictions_torso(ref_img)
    org_left, org_right = get_predictions_sleeves(org_img)

    # Extract sleeves from the reference image
    ref_left, ref_right = get_predictions_sleeves(ref_img)

    # Remove segments from the original image based on detected sleeves
    org_img = remove_segment(org_img, org_right)
    org_img = remove_segment(org_img, org_left)

    # Extract torso segment for color processing
    org_torso_color = extract_segmented_area(org_img, org_torso)
    new_color = detect_major_color_segment(org_torso_color)

    # Extract torso segments
    org_torso_seg = extract_segmented_area(org_img, org_torso)
    ref_torso_seg = extract_segmented_area(ref_img, ref_torso)

    # Extract segmented areas for left and right sleeves from the reference image
    left_sleeve_ref = extract_segmented_area(ref_img, ref_left)
    right_sleeve_ref = extract_segmented_area(ref_img, ref_right)

    # Change the color of the reference left sleeve
    left_domin_color = detect_major_color_segment(left_sleeve_ref)
    left_sleeve_ref = blend_new_color(left_sleeve_ref, left_domin_color, new_color)

    # Create a mirrored copy of the left sleeve to represent the right sleeve
    left_sleeve_copy = copy.deepcopy(left_sleeve_ref)
    right_sleeve_ref = left_sleeve_copy.transpose(Image.FLIP_LEFT_RIGHT)

    # Blend the left and right sleeves onto the original image
    org_img = blend_segment_sleeves(org_img, left_sleeve_ref, org_left, ref_left, 'left', org_torso_seg, ref_torso_seg)
    org_img = blend_segment_sleeves(org_img, right_sleeve_ref, org_right, ref_right, 'right', org_torso_seg, ref_torso_seg)

    # Remove the image background 
    org_img = change_background_white(org_img)

    # Return the modified image
    return org_img

# Function to swap sleeves between the original and reference images
def swap_sleeve_from_sleeveless(org_img, ref_img):
    # Convert original and reference images to RGB
    org_torso = get_predictions_torso(org_img)
    ref_torso = get_predictions_torso(ref_img)
    
    # Extract sleeves from the reference image
    ref_left, ref_right = get_predictions_sleeves(ref_img)

    # Extract torso segment for color processing
    org_torso_color = extract_segmented_area(org_img, org_torso)
    new_color = detect_major_color_segment(org_torso_color)

    # Extract torso segments
    org_torso_seg = extract_segmented_area(org_img, org_torso)
    ref_torso_seg = extract_segmented_area(ref_img, ref_torso)

    # Extract segmented areas for left and right sleeves from the reference image
    left_sleeve_ref = extract_segmented_area(ref_img, ref_left)
    right_sleeve_ref = extract_segmented_area(ref_img, ref_right)

    # Change the color of the reference left sleeve
    left_domin_color = detect_major_color_segment(left_sleeve_ref)
    left_sleeve_ref = blend_new_color(left_sleeve_ref, left_domin_color, new_color)

    # Create a mirrored copy of the left sleeve to represent the right sleeve
    left_sleeve_copy = copy.deepcopy(left_sleeve_ref)
    right_sleeve_ref = left_sleeve_copy.transpose(Image.FLIP_LEFT_RIGHT)

    # Blend the left and right sleeves onto the original image
    org_img = blend_segment_sleeves_from_torso(org_img, left_sleeve_ref, org_torso, ref_left, 'left', org_torso_seg, ref_torso_seg)
    org_img = blend_segment_sleeves_from_torso(org_img, right_sleeve_ref, org_torso, ref_right, 'right', org_torso_seg, ref_torso_seg)

    # Remove the image background 
    org_img = change_background_white(org_img)

    # Return the modified image
    return org_img
