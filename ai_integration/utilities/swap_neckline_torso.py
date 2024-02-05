from PIL import Image
from ..utilities.get_predections_yolo import get_predictions_torso
from ..utilities.rgba_to_rgb import rgba_to_rgb
from ..utilities.segment_processing import remove_segment, extract_segmented_area, blend_segment_mid, resize_segment
from ..utilities.change_background import change_background_white


# Function to swap neckline and torso between the original and reference images
def swap_neckline_torse(org_img, ref_img):
    # Convert original and reference images to RGB
    # rgba_to_rgb(org_img_path)
    # org_img = Image.open(org_img_path)
    # org_neckline = get_predictions_neckline(org_img_path)
    org_torso = get_predictions_torso(org_img)
    # print(org_torso)

    # rgba_to_rgb(ref_img_path)
    # ref_img = Image.open(ref_img_path)
    # ref_neckline = get_predictions_neckline(ref_img_path)
    ref_torso = get_predictions_torso(ref_img)

    # Remove segments from the original image based on detected neckline  and torso
    torso_org = extract_segmented_area(org_img, org_torso)
    # neckline_org = extract_segmented_area(org_img, org_neckline)
    # org_img = remove_segment(org_img, org_neckline)
    org_img = remove_segment(org_img, org_torso)

    # Extract segmented areas for neckline and torso from the reference image
    # neckline_ref = extract_segmented_area(ref_img, ref_neckline)
    torso_ref = extract_segmented_area(ref_img, ref_torso)

    # Resizing segmented areas for neckline and torso from the reference image
    # neckline_ref, ref_neckline = resize_segment(neckline_ref, ref_neckline, neckline_org, org_neckline)
    # torso_ref, ref_torso = resize_segment(torso_ref, ref_torso, torso_org, org_torso)

    # Blend the neckline and torso onto the original image
    # org_img = blend_segment_mid(org_img, neckline_ref, org_neckline, ref_neckline)
    org_img = blend_segment_mid(org_img, torso_ref, org_torso, ref_torso)

    # Remove the image background using the rembg library
    org_img = change_background_white(org_img)

    # Display the modified image
    # org_img.show()

    return org_img

# Main function to initiate swapping sleeves
if __name__ == "__main__":
    org_img_path = "./test_images/org.jpeg"
    ref_img_path = "./test_images/ref.jpeg"
    swap_neckline_torse(org_img_path, ref_img_path)
