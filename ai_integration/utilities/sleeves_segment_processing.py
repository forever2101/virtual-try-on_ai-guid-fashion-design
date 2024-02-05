from PIL import Image, ImageDraw, ImageOps

# Function to blend sleeves segment onto the original image
def blend_segment_sleeves_from_torso(img, segment_img, segment_data_org, segment_data_ref, direction, org_torso_seg, ref_torso_seg):

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

    # Find the x value at the minimum y for the original and reference
    org_index_min_y = org_y_values.index(org_min_y)
    ref_index_min_y = ref_y_values.index(ref_min_y)
    org_value_x_miny = org_x_values[org_index_min_y]
    ref_value_x_miny = ref_x_values[ref_index_min_y]


    org_index_min_x = org_x_values.index(org_min_x)
    org_value_y_minx = org_y_values[org_index_min_x]

    org_index_max_x = org_x_values.index(org_min_x)
    org_value_y_maxx = org_y_values[org_index_max_x]


    # Calculate percentage change in width and height
    percent_change_width = (org_torso_seg.width - ref_torso_seg.width) / ref_torso_seg.width
    percent_change_height = (org_torso_seg.height - ref_torso_seg.height) / ref_torso_seg.height

    # Calculate new width and height based on percentage change
    new_seg_width = round(segment_img.width * (1 + percent_change_width))
    new_seg_height = round(segment_img.height * (1 + percent_change_height))

    resized_seg = segment_img.resize((new_seg_width, new_seg_height), Image.LANCZOS)

    # Convert images to RGBA mode if not already in that mode
    img = img.convert("RGBA")
    segment_img = resized_seg.convert("RGBA")
    # x_shift = int(0.9*(ref_max_x-ref_min_x))

    # Calculate the shift required for blending the segment
    if direction == 'left':
        img.paste(segment_img, (int(org_min_x - int((segment_img.width))), int(org_value_y_minx)), segment_img)
    if direction == 'right':
        # x_shift = int((org_value_x_miny - org_min_x) - (ref_value_x_miny - ref_min_x))
        img.paste(segment_img, (int(org_max_x), int(org_value_y_maxx)), segment_img)
    return img

# Function to blend sleeves segment onto the original image
def blend_segment_sleeves(img, segment_img, segment_data_org, segment_data_ref, direction, org_torso_seg, ref_torso_seg):

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

    # Find the x value at the minimum y for the original and reference
    org_index_min_y = org_y_values.index(org_min_y)
    ref_index_min_y = ref_y_values.index(ref_min_y)
    org_value_x_miny = org_x_values[org_index_min_y]
    ref_value_x_miny = ref_x_values[ref_index_min_y]


    # resized_seg = segment_img.resize((new_seg_width, new_seg_height), Image.Resampling.LANCZOS)
    # Calculate percentage change in width and height
    percent_change_width = (org_torso_seg.width - ref_torso_seg.width) / ref_torso_seg.width
    percent_change_height = (org_torso_seg.height - ref_torso_seg.height) / ref_torso_seg.height

    # Calculate new width and height based on percentage change
    new_seg_width = round(segment_img.width * (1 + percent_change_width))
    new_seg_height = round(segment_img.height * (1 + percent_change_height))

    resized_seg = segment_img.resize((new_seg_width, new_seg_height), Image.LANCZOS)


    # Convert images to RGBA mode if not already in that mode
    img = img.convert("RGBA")
    segment_img = resized_seg.convert("RGBA")

    # Calculate the shift required for blending the segment
    if direction == 'left':
        x_shift = int((ref_value_x_miny * (1 + percent_change_width) - ref_min_x * (1 + percent_change_width)) - (org_value_x_miny - org_min_x))
        img.paste(segment_img, (int(org_min_x - x_shift), int(org_min_y)), segment_img)
    if direction == 'right':
        x_shift = int((org_value_x_miny - org_min_x) - (ref_value_x_miny * (1 + percent_change_width) - ref_min_x * (1 + percent_change_width)))
        img.paste(segment_img, (int(org_min_x + x_shift), int(org_min_y)), segment_img)
    return img




#old code foe generating sleeves
def to_sleeveless(img, segment_data_left, segment_data_right):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy_left = segment_data_left.xy[0]

    # Separate X and Y values into 1D arrays
    x_values_left = xy_left[:, 0]
    y_values_left = xy_left[:, 1]
    
    min_y_left = min(y_values_left)
    max_y_left = max(y_values_left)
    mid_y_left = (min_y_left + max_y_left) / 2
    
    min_x_left = min(x_values_left)
    max_x_left = max(x_values_left)
    mid_x_left = (min_x_left + max_x_left) / 2

    # Find the index of the minimum x value in x_values_left
    min_x_index_left = x_values_left.tolist().index(min_x_left)

    # Retrieve the corresponding y value
    y_at_min_x_left = y_values_left[min_x_index_left]

    # Find the index of the minimum x value in x_values_left
    max_x_index_left = x_values_left.tolist().index(max_x_left)

    # Retrieve the corresponding y value
    y_at_max_x_left = y_values_left[max_x_index_left]

    # Find the index of the minimum y value in y_values_left
    min_y_index_left = y_values_left.tolist().index(min_y_left)

    # Retrieve the corresponding x value
    x_at_min_y_left = x_values_left[min_y_index_left]


    # Reshape the array to a 2D array
    xy_right = segment_data_right.xy[0]

    # Separate X and Y values into 1D arrays
    x_values_right = xy_right[:, 0]
    y_values_right = xy_right[:, 1]
    
    min_y_right = min(y_values_right)
    max_y_right = max(y_values_right)
    mid_y_right = (min_y_right + max_y_right) / 2
    
    min_x_right = min(x_values_right)
    max_x_right = max(x_values_right)
    mid_x_right = (min_x_right + max_x_right) / 2


    # Find the index of the minimum x value in x_values_left
    min_x_index_right = x_values_right.tolist().index(min_x_right)

    # Retrieve the corresponding y value
    y_at_min_x_right = y_values_right[min_x_index_right]

    # Find the index of the minimum x value in x_values_left
    min_x_index_right = x_values_right.tolist().index(min_x_right)

    # Retrieve the corresponding y value
    y_at_min_x_right = y_values_left[min_x_index_right]

    # Find the index of the minimum y value in y_values_left
    min_y_index_right = y_values_right.tolist().index(min_y_right)

    # Retrieve the corresponding x value
    x_at_min_y_right = x_values_left[min_y_index_right]


    left_sleeve = [(x, y) for x, y in zip(x_values_left,y_values_left)] 
    right_sleeve = [(x, y) for x, y in zip(x_values_right,y_values_right)]  

    draw.polygon(left_sleeve, fill='white')
    draw.polygon(right_sleeve, fill='white')

    diff = max_x_left-x_at_min_y_left

    rect_coords = [(x_at_min_y_left, min_y_left), (max_x_left, y_at_max_x_left)]
    # rect_coords = [(min_x_right, min_y_right), (x_at_min_y_right, y_at_min_x_right)]
    rect_coords_2 = [(min_x_right, min_y_left), (min_x_right+diff, y_at_max_x_left)]

    # Draw the rectangle after the polygon
    draw.rectangle(rect_coords, fill=(0, 0, 0, 0))  
    draw.rectangle(rect_coords_2, fill=(0, 0, 0, 0))    
    
    return img

def full_to_sleeveless(img, segment_data_left, segment_data_right):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy_left = segment_data_left.xy[0]

    # Separate X and Y values into 1D arrays
    x_values_left = xy_left[:, 0]
    y_values_left = xy_left[:, 1]
    
    min_y_left = min(y_values_left)
    max_y_left = max(y_values_left)
    mid_y_left = (min_y_left + max_y_left) / 2
    
    min_x_left = min(x_values_left)
    max_x_left = max(x_values_left)
    mid_x_left = (min_x_left + max_x_left) / 2

    # Find the index of the minimum x value in x_values_left
    min_x_index_left = x_values_left.tolist().index(min_x_left)

    # Retrieve the corresponding y value
    y_at_min_x_left = y_values_left[min_x_index_left]

    # Find the index of the minimum x value in x_values_left
    max_x_index_left = x_values_left.tolist().index(max_x_left)

    # Retrieve the corresponding y value
    y_at_max_x_left = y_values_left[max_x_index_left]

    # Find the index of the minimum y value in y_values_left
    min_y_index_left = y_values_left.tolist().index(min_y_left)

    # Retrieve the corresponding x value
    x_at_min_y_left = x_values_left[min_y_index_left]





    # Reshape the array to a 2D array
    xy_right = segment_data_right.xy[0]

    # Separate X and Y values into 1D arrays
    x_values_right = xy_right[:, 0]
    y_values_right = xy_right[:, 1]
    
    min_y_right = min(y_values_right)
    max_y_right = max(y_values_right)
    mid_y_right = (min_y_right + max_y_right) / 2
    
    min_x_right = min(x_values_right)
    max_x_right = max(x_values_right)
    mid_x_right = (min_x_right + max_x_right) / 2


    # Find the index of the minimum x value in x_values_left
    min_x_index_right = x_values_right.tolist().index(min_x_right)

    # Retrieve the corresponding y value
    y_at_min_x_right = y_values_right[min_x_index_right]

    # Find the index of the minimum x value in x_values_left
    min_x_index_right = x_values_right.tolist().index(min_x_right)

    # Retrieve the corresponding y value
    y_at_min_x_right = y_values_left[min_x_index_right]

    # Find the index of the minimum y value in y_values_left
    min_y_index_right = y_values_right.tolist().index(min_y_right)

    # Retrieve the corresponding x value
    x_at_min_y_right = x_values_left[min_y_index_right]


    left_sleeve = [(x, y) for x, y in zip(x_values_left,y_values_left)] 
    right_sleeve = [(x, y) for x, y in zip(x_values_right,y_values_right)]  

    draw.polygon(left_sleeve, fill='white')
    draw.polygon(right_sleeve, fill='white')

    diff = max_x_left-x_at_min_y_left

    rect_coords = [(x_at_min_y_left, min_y_left), (max_x_left, y_at_max_x_left)]
    # rect_coords = [(min_x_right, min_y_right), (x_at_min_y_right, y_at_min_x_right)]
    rect_coords_2 = [(min_x_right, min_y_left), (min_x_right+diff, y_at_max_x_left)]

    # Draw the rectangle after the polygon
    draw.rectangle(rect_coords, fill=(0, 0, 0, 0))  
    draw.rectangle(rect_coords_2, fill=(0, 0, 0, 0))    
    
    return img


def full_to_cap(img, segment_data_left, segment_data_right):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy_left = segment_data_left.xy[0]

    # Separate X and Y values into 1D arrays
    x_values_left = xy_left[:, 0]
    y_values_left = xy_left[:, 1]
    
    min_y_left = min(y_values_left)
    max_y_left = max(y_values_left)
    mid_y_left = (min_y_left + max_y_left) / 2
    
    min_x_left = min(x_values_left)
    max_x_left = max(x_values_left)
    mid_x_left = (min_x_left + max_x_left) / 2

    # Find the index of the minimum x value in x_values_left
    min_x_index_left = x_values_left.tolist().index(min_x_left)

    # Retrieve the corresponding y value
    y_at_min_x_left = y_values_left[min_x_index_left]

    # Find the index of the minimum x value in x_values_left
    max_x_index_left = x_values_left.tolist().index(max_x_left)

    # Retrieve the corresponding y value
    y_at_max_x_left = y_values_left[max_x_index_left]

    # Find the index of the minimum y value in y_values_left
    min_y_index_left = y_values_left.tolist().index(min_y_left)

    # Retrieve the corresponding x value
    x_at_min_y_left = x_values_left[min_y_index_left]


    # Reshape the array to a 2D array
    xy_right = segment_data_right.xy[0]

    # Separate X and Y values into 1D arrays
    x_values_right = xy_right[:, 0]
    y_values_right = xy_right[:, 1]
    
    min_y_right = min(y_values_right)
    max_y_right = max(y_values_right)
    mid_y_right = (min_y_right + max_y_right) / 2
    
    min_x_right = min(x_values_right)
    max_x_right = max(x_values_right)
    mid_x_right = (min_x_right + max_x_right) / 2


    # Find the index of the minimum x value in x_values_left
    min_x_index_right = x_values_right.tolist().index(min_x_right)

    # Retrieve the corresponding y value
    y_at_min_x_right = y_values_right[min_x_index_right]

    # Find the index of the minimum x value in x_values_left
    min_x_index_right = x_values_right.tolist().index(min_x_right)

    # Retrieve the corresponding y value
    y_at_min_x_right = y_values_left[min_x_index_right]

    # Find the index of the minimum y value in y_values_left
    min_y_index_right = y_values_right.tolist().index(min_y_right)

    # Retrieve the corresponding x value
    x_at_min_y_right = x_values_left[min_y_index_right]


    left_sleeve = [(x, y) for x, y in zip(x_values_left,y_values_left)] 
    right_sleeve = [(x, y) for x, y in zip(x_values_right,y_values_right)]  

    draw.polygon(left_sleeve, fill='white')
    draw.polygon(right_sleeve, fill='white')

    diff = max_x_left-x_at_min_y_left

    rect_coords = [(min_x_left, min_y_left), (max_x_left, y_at_max_x_left)]
    # rect_coords = [(min_x_right, min_y_right), (x_at_min_y_right, y_at_min_x_right)]
    rect_coords_2 = [(min_x_right, min_y_left), (max_x_right, y_at_max_x_left)]

    # Draw the rectangle after the polygon
    draw.rectangle(rect_coords, fill=(0, 0, 0, 0))  
    draw.rectangle(rect_coords_2, fill=(0, 0, 0, 0))    
    
    return img


def full_to_elbow(img, segment_data_left, segment_data_right, ratio_change):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data_left.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    min_y = min(y_values)
    upper_threshold = min_y + (0.7*ratio_change) * (max(y_values) - min_y)  # 10% below the minimum y
    lower_threshold = min_y + ratio_change * (max(y_values) - min_y)  # based on ratio

    white_points = [(x, y) for x, y in zip(x_values,y_values) if y >= (lower_threshold - 0.05*lower_threshold)]  # Select points below threshold
    draw.polygon(white_points, fill='white')

    # hem_points = [(x, y) for x, y in zip(x_values,y_values) if y >= upper_threshold and y<= lower_threshold]  # Select points below threshold
    hem_points = [(x, y) for x, y in zip(x_values,y_values) if y<= lower_threshold]  # Select points below threshold

    draw.polygon(hem_points, fill=(0, 0, 0, 0))


    xy = segment_data_right.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    min_y = min(y_values)
    upper_threshold = min_y + (0.7*ratio_change) * (max(y_values) - min_y)  # 10% below the minimum y
    lower_threshold = min_y + ratio_change * (max(y_values) - min_y)  # based on ratio

    white_points = [(x, y) for x, y in zip(x_values,y_values) if y >= (lower_threshold - 0.05*lower_threshold)]  # Select points below threshold
    draw.polygon(white_points, fill='white')

    hem_points = [(x, y) for x, y in zip(x_values,y_values) if y<= lower_threshold]  # Select points below threshold
    draw.polygon(hem_points, fill=(0, 0, 0, 0))

    
    return img