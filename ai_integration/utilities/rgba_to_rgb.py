from PIL import Image

# Function to convert RGBA images to RGB
def rgba_to_rgb(img_path):
    img = Image.open(img_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(img_path)