# Import necessary modules from the Python Imaging Library (PIL)
from PIL import Image, ImageDraw
import math
import copy

# Function to blend a segmented image onto the original image with adjustments
def blend_segment_skirt(img, segment_img, segment_data_org, segment_data_ref, ratio):
    # Extract X and Y coordinates of the original segment
    org_xy = segment_data_org.xy[0]
    
    # Separate X and Y values into 1D arrays
    org_x_values = list(org_xy[:, 0])
    org_y_values = list(org_xy[:, 1])
    org_min_x, org_min_y = min(org_x_values), min(org_y_values)
    org_max_x, org_max_y = max(org_x_values), max(org_y_values)
    org_mid_x = (org_min_x + org_max_x) / 2
    org_mid_y = (org_min_y + org_max_y) / 2

    # Extract X and Y coordinates of the reference segment
    ref_xy = segment_data_ref.xy[0]
    
    # Separate X and Y values into 1D arrays
    ref_x_values = list(ref_xy[:, 0])
    ref_y_values = list(ref_xy[:, 1])
    ref_min_x, ref_min_y = min(ref_x_values), min(ref_y_values)
    ref_max_x, ref_max_y = max(ref_x_values), max(ref_y_values)
    ref_mid_x = (ref_min_x + ref_max_x) / 2
    ref_mid_y = (ref_min_y + ref_max_y) / 2

    # Calculate the distance between x min and x mid for both original and reference segments
    org_min_mid_x = (org_mid_x - org_min_x)
    ref_min_mid_x = (ref_mid_x - ref_min_x)

    # Resize the reference segment based on the specified ratio
    orignial_seg_height = abs(org_max_y - org_min_y)
    new_seg_height = int(ratio * orignial_seg_height)
    
    # Calculate the waist points for both original and reference segments
    org_waist_points = [x for x, y in zip(org_x_values, org_y_values) if y < (org_min_y + 0.15 * (org_max_y - org_min_y))]
    org_waist_x_max, org_waist_x_min = max(org_waist_points), min(org_waist_points)
    org_max_min_diff = org_waist_x_max - org_waist_x_min
    
    ref_waist_points = [x for x, y in zip(ref_x_values, ref_y_values) if y < (ref_min_y + 0.15 * (ref_max_y - ref_min_y))]
    ref_waist_x_max, ref_waist_x_min = max(ref_waist_points), min(ref_waist_points)
    ref_max_min_diff = ref_waist_x_max - ref_waist_x_min

    diff_org_ref_waist = org_max_min_diff - ref_max_min_diff

    # Adjust the width of the reference segment based on the difference in waist width
    if diff_org_ref_waist > 0:
        new_seg_width = int(segment_img.width + abs(diff_org_ref_waist))
    else:
        new_seg_width = int(segment_img.width - abs(diff_org_ref_waist))

    # Convert images to RGBA mode if not already in that mode
    img = img.convert("RGBA")
    segment_img = segment_img.convert("RGBA")

    # Resize the segment image
    resized_seg = segment_img.resize((new_seg_width, new_seg_height), Image.Resampling.LANCZOS)

    # Padding to prevent image cutoff
    padding = 0

    # Adjust dimensions and create a new padded image if necessary
    if (org_min_y + new_seg_height > img.width):
        padding = int((org_min_y + new_seg_height) - img.width + 0.1 * (org_min_y + new_seg_height))
        new_width = img.width + padding
        new_height = img.height + padding
        padded_image = Image.new('RGBA', (new_width, new_height), 'white')
        padded_image.paste(img, (padding // 2, 0))
        img = padded_image

    # Paste the resized segment onto the image using calculated shifts
    img.paste(resized_seg, (int((padding // 2 + org_min_x + (org_max_x - org_min_x) // 2) - new_seg_width // 2), int(org_min_y)), resized_seg)

    return img


# Function to convert an image to a polygon mask
def seg_to_polygon(img, top_percent, bottom_rect_percent):
    width, height = img.size

    # Create a blank mask image
    mask = Image.new("RGBA", img.size, (0, 0, 0, 0))

    # Define coordinates for creating a polygon mask
    top_x = (width / 2) - (top_percent * width) / 2
    bottom_y = height - bottom_rect_percent * height
    draw_mask = ImageDraw.Draw(mask)
    polygon_points = [(top_x, 0), (0, bottom_y), (0, height - 1), (width - 1, height - 1), (width - 1, bottom_y), (width - top_x, 0)]
    draw_mask.polygon(polygon_points, fill='white')

    # Replace white pixels in the mask with corresponding pixels from the image
    for x in range(width):
        for y in range(height):
            if mask.getpixel((x, y))[:3] == (255, 255, 255):
                mask.putpixel((x, y), img.getpixel((x, y)))

    return mask
