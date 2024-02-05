from PIL import Image
from ..utilities.get_predections_yolo import get_predictions_hem, get_predictions_torso
from ..utilities.rgba_to_rgb import rgba_to_rgb
from ..utilities.segment_processing import remove_segment, extract_segmented_area
from ..utilities.hem_segment_procesing import blend_segment_skirt
from ..utilities.change_background import change_background_white
from ..utilities.color_processing import detect_major_color_segment, blend_new_color

# Function to swap skirts between the original and reference images
def swap_skirt(org_img, ref_img, ratio):
    # Convert original and reference images to RGB
    # rgba_to_rgb(org_img_path)
    # org_img = Image.open(org_img_path)
    org_skirt = get_predictions_hem(org_img)
    org_torso = get_predictions_torso(org_img)

    # rgba_to_rgb(ref_img_path)
    # ref_img = Image.open(ref_img_path)
    ref_skirt = get_predictions_hem(ref_img)

    #extract org segment for color
    org_torso_color = extract_segmented_area(org_img, org_torso)
    new_color = detect_major_color_segment(org_torso_color)

    # Remove segments from the original image based on detected skirt
    org_img = remove_segment(org_img, org_skirt)

    # Extract segmented areas for skirt from the reference image
    skirt_ref = extract_segmented_area(ref_img, ref_skirt)

    skirt_domin_color = detect_major_color_segment(skirt_ref)
    skirt_ref = blend_new_color(skirt_ref, skirt_domin_color, new_color)

    # Blend the skirt onto the original image
    org_img = blend_segment_skirt(org_img, skirt_ref, org_skirt, ref_skirt, ratio)

    # Remove the image background using the rembg library
    org_img = change_background_white(org_img)

    # Display the modified image
    # org_img.show()

    return org_img

# Main function to initiate swapping sleeves
if __name__ == "__main__":
    org_img_path = "./test_images/org.jpeg"
    ref_img_path = "./test_images/ref.jpeg"
    swap_skirt(org_img_path, ref_img_path)
