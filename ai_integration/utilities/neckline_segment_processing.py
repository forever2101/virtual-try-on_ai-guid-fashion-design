from PIL import Image, ImageDraw


def transparent_segment_neckline(img, segment_data, is_high):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    
    min_y = min(y_values)
    max_y = max(y_values)
    mid_y = (min_y + max_y) / 2
    
    min_x = min(x_values)
    max_x = max(x_values)
    mid_x = (min_x + max_x) / 2
    
    # Calculate radius as 95% of the distance between mid_x and min_x
    radius = 0.95 * abs(mid_x - min_x)
    
    # Ensure the midpoint of the ellipse aligns with min_y
    y_position = min_y
    
    # Ensure the ellipse doesn't go beyond mid_y
    y_upper_bound = min_y + 1.2 * radius
    y_lower_bound = min_y - radius
    
    # Draw ellipse within the y-coordinate boundaries
    draw.ellipse([(mid_x - radius, y_lower_bound), (mid_x + radius, y_upper_bound)], fill=(0, 0, 0, 0))
    
    return img


def round_neck_segment_neckline(img, segment_data, is_high):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    
    min_y = min(y_values)
    max_y = max(y_values)
    mid_y = (min_y + max_y) / 2
    
    min_x = min(x_values)
    max_x = max(x_values)
    mid_x = (min_x + max_x) / 2
    
    
    # Ensure the midpoint of the first ellipse aligns with min_y
    if is_high:
        radius = 0.6 * abs(mid_x - min_x)
        y_position = 1.1 * min_y
    else:
        radius = 0.8 * abs(mid_x - min_x)
        y_position = min_y
    
    # Draw first white ellipse at (mid_x, y_position) with calculated radius
    draw.ellipse([(mid_x - radius, y_position - radius), (mid_x + radius, y_position + radius)], fill='white')
    
    # Calculate the y position 30% above the first ellipse (aligning midpoint with min_y)
    y_position_2 = min_y + 0.3 * abs(min_y - mid_y)
    
    # Draw second white semi-ellipse with midpoint aligned to min_y
    draw.ellipse([(mid_x - radius, y_position_2 - radius), (mid_x + radius, y_position_2 + radius)], fill=(0, 0, 0, 0))

    # Calculate the y position 30% below min_y and mid_y
    y_position_3 = min_y - 0.1 * abs(min_y - mid_y)
    
    # Draw third white semi-ellipse 30% below min_y and mid_y
    draw.ellipse([(mid_x - radius, y_position_3 - radius), (mid_x + radius, y_position_3 + radius)], fill='white')
    
    return img



def crew_neck_segment_neckline(img, segment_data, is_high):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    
    min_y = min(y_values)
    max_y = max(y_values)
    mid_y = (min_y + max_y) / 2
    
    min_x = min(x_values)
    max_x = max(x_values)
    mid_x = (min_x + max_x) / 2
    

    if is_high:
        # Calculate radius as 95% of the distance between mid_x and min_x
        radius = 0.6 * abs(mid_x - min_x)
        
        # Calculate the y position 10% below the midpoint y and minimum y
        y_position = 1.3 * min_y #1.1 * min_y + 0.1 * mid_y
    else:
        # Calculate radius as 95% of the distance between mid_x and min_x
        radius = 0.80 * abs(mid_x - min_x)
        
        # Calculate the y position 10% below the midpoint y and minimum y
        y_position = min_y #1.1 * min_y + 0.1 * mid_y
        
    # Draw first white ellipse at (mid_x, y_position) with calculated radius
    draw.ellipse([(mid_x - radius, y_position - radius), (mid_x + radius, y_position + radius)], fill='white')
    
    # Calculate the y position 10% below the first white ellipse
    y_position_2 = 0.8*y_position #+ 0.1 * abs(y_position - min_y)
    
    # Draw second white semi-ellipse 10% below the first white ellipse
    # draw.chord([(mid_x - radius, y_position_2 - radius), (mid_x + radius, y_position_2 + radius)], outline=None, start=360, end=180, fill=(0, 0, 0, 0))
    draw.chord([(mid_x - radius, y_position_2 - radius), (mid_x + radius, y_position_2 + 1.3*radius)], outline=None, start=360, end=180, fill=(0, 0, 0, 0))

    return img


def v_neck_segment_neckline(img, segment_data, is_high):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    
    min_y = min(y_values)
    max_y = max(y_values)
    mid_y = (min_y + max_y) / 2
    
    min_x = min(x_values)
    max_x = max(x_values)
    mid_x = (min_x + max_x) / 2
    
    # Calculate half the distance between mid_x and min_x
    half_width = 0.9 * abs(mid_x - min_x)
    
    # Calculate the y position 10% below the minimum y
    y_position = min_y
    
    # Limit triangle_top value to not exceed mid_y
    # triangle_top = (mid_x, min(mid_y, y_position - 5 * abs(y_position - mid_y)))
    triangle_top = (mid_x, y_position - 5 * abs(y_position - mid_y))
    triangle_left = (mid_x - half_width, y_position)
    triangle_right = (mid_x + half_width, y_position)
    
    # Draw a triangle with the calculated points
    draw.polygon([triangle_top, triangle_left, triangle_right], fill='white')
    
    # Calculate y position for the second and third triangles
    # y_position_2 = min_y + 4 * abs(mid_y - min_y)
    # y_position_3 = min_y + 5 * abs(mid_y - min_y)
    # triangle_top2 = (mid_x, min(mid_y, y_position + 5 * abs(y_position - mid_y)))
    triangle_top2 = (mid_x, mid_y)
    triangle_top3 = (mid_x, 0.8*mid_y)
    
    # Draw triangles aligned to the bottom
    draw.polygon([triangle_top2, (mid_x - half_width, min_y), (mid_x + half_width, min_y)], fill=(0, 0, 0, 0))
    
    draw.polygon([triangle_top3, (mid_x - half_width, min_y), (mid_x + half_width, min_y)], fill='white')
    
    return img

def square_neck_segment_neckline(img, segment_data, is_high):
    draw = ImageDraw.Draw(img)
    # Reshape the array to a 2D array
    xy = segment_data.xy[0]

    # Separate X and Y values into 1D arrays
    x_values = xy[:, 0]
    y_values = xy[:, 1]
    
    min_y = min(y_values)
    max_y = max(y_values)
    mid_y = (min_y + max_y) / 2
    
    min_x = min(x_values)
    max_x = max(x_values)
    mid_x = (min_x + max_x) / 2
    
    # Calculate half the distance between mid_x and min_x
    half_width = 0.8 * abs(mid_x - min_x)
    
    # Calculate the y position 10% below the minimum y
    y_position = 0.8 * min_y
    
    # Calculate the first rectangle coordinates
    rectangle_top1 = (mid_x - half_width, y_position)
    rectangle_bottom1 = (mid_x + half_width, min_y)
    
    # Draw the first rectangle
    draw.rectangle([rectangle_top1, rectangle_bottom1], fill='white')
    
    # Calculate the second rectangle coordinates
    rectangle_top2 = (mid_x - half_width, min_y)
    rectangle_bottom2 = (mid_x + half_width, mid_y)
    
    # Draw the second rectangle
    draw.rectangle([rectangle_top2, rectangle_bottom2], fill=(0, 0, 0, 0))
    
    # Decrease half_width by 10%
    decreased_half_width = 0.75 * half_width
    
    # Calculate the third rectangle coordinates
    rectangle_top3 = (mid_x - decreased_half_width, min_y)
    rectangle_bottom3 = (mid_x + decreased_half_width, 0.8 * mid_y)
    
    # Draw the third rectangle
    draw.rectangle([rectangle_top3, rectangle_bottom3], fill='white')
    
    return img