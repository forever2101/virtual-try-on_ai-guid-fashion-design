from PIL import Image, ImageDraw

# Function to make transparent segments based on their points
def transparent_segment(img, segment_data):
    draw = ImageDraw.Draw(img)
    points = [tuple(point) for point in segment_data.xy[0]]
    draw.polygon(points, fill=(0, 0, 0, 0))
    return img.convert('RGBA')