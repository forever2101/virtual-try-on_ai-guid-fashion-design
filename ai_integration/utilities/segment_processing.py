from PIL import Image, ImageDraw

# Function to remove segments based on their points
def remove_segment(img, segment_data):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    points = [(x, y) for x,y in zip(x_values, y_values)]
    draw.polygon(points, fill='white')
    return img

# Function to make transparent segments based on their points
def transparent_segment(img, segment_data):
    draw = ImageDraw.Draw(img)
    points = [(point['x'], point['y']) for point in segment_data['points']]
    draw.polygon(points, fill=(0, 0, 0, 0))
    return img


def transparent_segment_hem(img, segment_data):
    draw = ImageDraw.Draw(img)
    points = [(point['x'], point['y']) for point in segment_data['points']]
    
    y_values = [point['y'] for point in segment_data['points']]
    min_y = min(y_values)
    threshold = min_y + 0.1 * (max(y_values) - min_y)  # 10% below the minimum y
    
    hem_points = [(x, y) for (x, y) in points if y >= threshold]  # Select points below threshold
    
    if len(hem_points) > 2:  # Need at least 3 points to create a polygon
        draw.polygon(hem_points, fill=(0, 0, 0, 0))
        
        # Find the x-coordinates where min and max y-values in hem_points exist
        x_coords = [point[0] for point in hem_points]
        x_min, x_max = min(x_coords), max(x_coords)
        
        # Calculate the y-coordinate for the bottom of the rectangle
        max_x_distance = max(hem_points, key=lambda x: x[0])[0] - min(hem_points, key=lambda x: x[0])[0]
        max_y_distance_points = [point for point in hem_points if point[0] == min(hem_points, key=lambda x: x[0])[0] or point[0] == max(hem_points, key=lambda x: x[0])[0]]
        y_min = min(max_y_distance_points, key=lambda x: x[1])[1]
        
        # Draw transparent rectangle based on calculated coordinates
        img_width, img_height = img.size
        draw.rectangle([(x_min, y_min), (x_max, img_height)], fill=(0, 0, 0, 0))
    
    return img

def transparent_segment_sleeves(img, segment_data):
    draw = ImageDraw.Draw(img)
    x_values = [point['x'] for point in segment_data['points']]
    y_values = [point['y'] for point in segment_data['points']]
    
    max_x = max(x_values)
    min_x = min(x_values)
    mid_y = sum(y_values) / len(y_values)
    y_range = max(y_values) - min(y_values)
    
    # Calculate first circle's x position 30% before the min x
    first_circle_x = min_x - 0.8 * (max_x - min_x)
    # Calculate first circle's y diameter based on y range
    first_circle_diameter = y_range
    
    # Draw first circle
    draw.ellipse([(first_circle_x, mid_y - first_circle_diameter + min_x / 2),
                  (first_circle_x + first_circle_diameter, mid_y + first_circle_diameter + min_x / 2)],
                 fill=(0, 0, 0, 0))
    
    
    # Calculate second circle's x position 30% after the max x
    second_circle_x = max_x + 0.8 * (max_x - min_x)
    # Calculate second circle's y diameter based on y range
    second_circle_diameter = y_range
    
    # Draw second circle
    draw.ellipse([(second_circle_x - second_circle_diameter, mid_y - second_circle_diameter + min_x / 2),
                  (second_circle_x, mid_y + second_circle_diameter + min_x / 2)],
                 fill=(0, 0, 0, 0))
    
    return img


# Function to extract segmented area from an image
def extract_segmented_area(img, segment_data):
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    min_x, min_y = min(x_values), min(y_values)
    max_x, max_y = max(x_values), max(y_values)
    width, height = max_x - min_x, max_y - min_y

    cropped_img = img.crop((min_x, min_y, min_x + width, min_y + height))
    mask = Image.new('L', cropped_img.size, 0)
    draw = ImageDraw.Draw(mask)

    # Calculate offset points
    offset_x_values = x_values - min_x
    offset_y_values = y_values - min_y
    offset_points = [{'x': x, 'y': y} for x, y in zip(offset_x_values, offset_y_values)]

    polygon_points = [(point['x'], point['y']) for point in offset_points]

    draw.polygon(polygon_points, outline=1, fill=1)
    segmented_img = Image.new('RGBA', cropped_img.size, (0, 0, 0, 0))

    for x in range(cropped_img.width):
        for y in range(cropped_img.height):
            if mask.getpixel((x, y)):
                pixel = cropped_img.getpixel((x, y))
                # Ensure the pixel value is a tuple (r, g, b, a)
                if isinstance(pixel, int):
                    pixel = (pixel, pixel, pixel)  # Convert grayscale to RGB
                elif len(pixel) == 3:
                    pixel = pixel + (255,)  # Add alpha channel if missing
                segmented_img.putpixel((x, y), pixel)

    return segmented_img

def resize_segment(segment_img_new, segment_data_new, original_img, segment_data_org):
    # Extract x and y values for segments
    org_x_values = [point['x'] for point in segment_data_org['points']]
    org_y_values = [point['y'] for point in segment_data_org['points']]
    org_min_x, org_min_y = min(org_x_values), min(org_y_values)
    org_max_x, org_max_y = max(org_x_values), max(org_y_values)

    org_width, org_height = original_img.size

    # Calculate scaling factors for x and y axes
    scale_x = org_width / (org_max_x - org_min_x)
    scale_y = org_height / (org_max_y - org_min_y)

    # Resize the segment image based on original image dimensions
    resized_segment_img_new = segment_img_new.resize(original_img.size)

    # Resize the segment points based on original image dimensions
    resized_segment_points_new = []
    for point in segment_data_new['points']:
        scaled_x = (point['x'] - org_min_x) * scale_x
        scaled_y = (point['y'] - org_min_y) * scale_y
        resized_segment_points_new.append({'x': scaled_x, 'y': scaled_y})

    return resized_segment_img_new, {'points': resized_segment_points_new}


# Function to blend segment onto the original image
def blend_segment_mid(img, segment_img, segment_data_org, segment_data_ref):

    org_xy = segment_data_org.xy[0]

    # Separate X and Y values into 1D arrays
    org_x_values = list(org_xy[:, 0])
    org_y_values = list(org_xy[:, 1])
    org_min_x, org_min_y = min(org_x_values), min(org_y_values)
    org_max_x, org_max_y = max(org_x_values), max(org_y_values)
    org_mid_x = (org_min_x+org_max_x)/2
    org_mid_y = (org_min_y+org_max_y)/2


    ref_xy = segment_data_ref.xy[0]

    # Separate X and Y values into 1D arrays
    ref_x_values = list(ref_xy[:, 0])
    ref_y_values = list(ref_xy[:, 1])
    ref_min_x, ref_min_y = min(ref_x_values), min(ref_y_values)
    ref_max_x, ref_max_y = max(ref_x_values), max(ref_y_values)
    ref_mid_x = (ref_min_x+ref_max_x)/2
    ref_mid_y = (ref_min_y+ref_max_y)/2

    #Calculate distance between x min and x mid
    org_min_mid_x = (org_mid_x - org_min_x)
    ref_min_mid_x = (ref_mid_x - ref_min_x)

    # Calculate the translation needed to align midpoints
    x_shift = abs(ref_min_mid_x-org_min_mid_x)
    # y_shift = ref_mid_y - org_mid_y

    # Convert images to RGBA mode if not already in that mode
    img = img.convert("RGBA")
    segment_img = segment_img.convert("RGBA")

    # Paste segment_img onto img using the calculated shifts
    img.paste(segment_img, (int(org_min_x), int(org_min_y)), segment_img)

    return img

# Function to blend segment onto the original image
def blend_segment_skirt(img, segment_img, segment_data_org, segment_data_ref):
    org_xy = segment_data_org.xy[0]

    # Separate X and Y values into 1D arrays
    org_x_values = list(org_xy[:, 0])
    org_y_values = list(org_xy[:, 1])
    org_min_x, org_min_y = min(org_x_values), min(org_y_values)
    org_max_x, org_max_y = max(org_x_values), max(org_y_values)
    org_mid_x = (org_min_x+org_max_x)/2
    org_mid_y = (org_min_y+org_max_y)/2


    ref_xy = segment_data_ref.xy[0]

    # Separate X and Y values into 1D arrays
    ref_x_values = list(ref_xy[:, 0])
    ref_y_values = list(ref_xy[:, 1])
    ref_min_x, ref_min_y = min(ref_x_values), min(ref_y_values)
    ref_max_x, ref_max_y = max(ref_x_values), max(ref_y_values)
    ref_mid_x = (ref_min_x+ref_max_x)/2
    ref_mid_y = (ref_min_y+ref_max_y)/2


    #Calculate distance between x min and x mid
    org_min_mid_x = (org_mid_x - org_min_x)
    ref_min_mid_x = (ref_mid_x - ref_min_x)

    # Calculate the translation needed to align midpoints
    x_shift = abs(ref_min_mid_x-org_min_mid_x)
    # y_shift = ref_mid_y - org_mid_y

    # Convert images to RGBA mode if not already in that mode
    img = img.convert("RGBA")
    segment_img = segment_img.convert("RGBA")

    # Paste segment_img onto img using the calculated shifts
    img.paste(segment_img, (int(org_min_x + x_shift), int(org_min_y)), segment_img)

    return img