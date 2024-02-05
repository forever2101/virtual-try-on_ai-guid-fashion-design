import os
from openai import OpenAI
import json
import requests
from PIL import Image
from io import BytesIO
import time
import io
from decouple import config

# Load credentials from JSON file
# with open('credentials/openai_creds.json', 'r') as file:
#     credentials = json.load(file)

api_key = config('OPENAI_API_KEY')
model = config('OPENAI_MODEL_DALLE_INPAINT')
client = OpenAI(api_key=api_key)



def url_to_image(image_url):
    # Make a GET request to download the image
    response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Read the content of the response (image data) into a BytesIO object
        image_data = BytesIO(response.content)

        # Open the image from the BytesIO object using Pillow
        image_pil = Image.open(image_data)
        # image_pil.show()
        return image_pil

    else:
        print('Failed to download the image from ', image_url)
        return None


def generate_inpainting_back(img, mask, prompt):
    delay = 3
    img = img.convert('RGBA')
    mask = mask.convert('RGBA')

    # Convert the  Pillow image into binary mode
    buffer1 = io.BytesIO()
    img.save(buffer1, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
    buffer1.seek(0)
    img_bytes = buffer1.read()

    # Convert the  Pillow image into binary mode
    buffer2 = io.BytesIO()
    mask.save(buffer2, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
    buffer2.seek(0)
    mask_bytes = buffer2.read()


    while(True):
        try:
            result = client.images.edit(
                model=model,  
                image=img_bytes,
                mask=mask_bytes,
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
            image_url = json.loads(result.model_dump_json())['data'][0]['url']

            return url_to_image(image_url)
        
        except Exception as e:
            print(f"Error encountered: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

def generate_inpainting_neck(mask, prompt):
    delay = 3
    mask = mask.convert('RGBA')

    # Convert the  Pillow image into binary mode
    buffer2 = io.BytesIO()
    mask.save(buffer2, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
    buffer2.seek(0)
    mask_bytes = buffer2.read()


    while(True):
        try:
            result = client.images.edit(
                model=model,  
                image=mask_bytes,
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
            image_url = json.loads(result.model_dump_json())['data'][0]['url']

            return url_to_image(image_url)
        
        except Exception as e:
            print(f"Error encountered: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)





#old testing code for generating back, sleeve and necklines
# def generate_inpainting_back(img, mask):
#     delay = 3
#     img = img.convert('RGBA')
#     mask = mask.convert('RGBA')

#     # Convert the  Pillow image into binary mode
#     buffer1 = io.BytesIO()
#     img.save(buffer1, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
#     buffer1.seek(0)
#     img_bytes = buffer1.read()

#     # Convert the  Pillow image into binary mode
#     buffer2 = io.BytesIO()
#     mask.save(buffer2, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
#     buffer2.seek(0)
#     mask_bytes = buffer2.read()


#     while(True):
#         try:
#             result = client.images.edit(
#                 model=model,  
#                 image=img_bytes,
#                 mask = mask_bytes,
#                 prompt='for the product in the image generate back side covering entire area and mainting all features of product',
#                 n=1,
#                 size="1024x1024",
#             )
#             image_url = json.loads(result.model_dump_json())['data'][0]['url']

#             return url_to_image(image_url)
        
#         except Exception as e:
#             print(f"Error encountered: {e}")
#             print(f"Retrying in {delay} seconds...")
#             time.sleep(delay)

# def generate_inpainting_sleeve(img, mask):
#     delay = 3
#     img = img.convert('RGBA')
#     mask = mask.convert('RGBA')

#     # Convert the  Pillow image into binary mode
#     buffer1 = io.BytesIO()
#     img.save(buffer1, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
#     buffer1.seek(0)
#     img_bytes = buffer1.read()

#     # Convert the  Pillow image into binary mode
#     buffer2 = io.BytesIO()
#     mask.save(buffer2, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
#     buffer2.seek(0)
#     mask_bytes = buffer2.read()


#     while(True):
#         try:
#             result = client.images.edit(
#                 model=model,  
#                 image=img_bytes,
#                 mask = mask_bytes,
#                 prompt='for the product in the image generate sleeves back side covering entire area and mainting all features of product',
#                 n=1,
#                 size="1024x1024",
#             )
#             image_url = json.loads(result.model_dump_json())['data'][0]['url']

#             return url_to_image(image_url)
        
#         except Exception as e:
#             print(f"Error encountered: {e}")
#             print(f"Retrying in {delay} seconds...")
#             time.sleep(delay)


# def generate_inpainting_neckline(img, mask, type):
#     delay = 3
#     img = img.convert('RGBA')
#     mask = mask.convert('RGBA')

#     # Convert the  Pillow image into binary mode
#     buffer1 = io.BytesIO()
#     img.save(buffer1, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
#     buffer1.seek(0)
#     img_bytes = buffer1.read()

#     # Convert the  Pillow image into binary mode
#     buffer2 = io.BytesIO()
#     mask.save(buffer2, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
#     buffer2.seek(0)
#     mask_bytes = buffer2.read()


#     while(True):
#         try:
#             result = client.images.edit(
#                 model=model,  
#                 image=mask_bytes,
#                 # mask=mask_bytes,
#                 prompt=f'change the skirt length of dress to {type}',
#                 n=1,
#                 size="1024x1024",
#             )
#             image_url = json.loads(result.model_dump_json())['data'][0]['url']

#             return url_to_image(image_url)
        
#         except Exception as e:
#             print(f"Error encountered: {e}")
#             print(f"Retrying in {delay} seconds...")
#             time.sleep(delay)

# if __name__=="__main__":
#     img = Image.open("./test_images/full.jpeg")
#     gene = generate_inpainting_back(img)
#     gene.show()