import requests
import json
from PIL import Image
import io
import os
from decouple import config



login_url = config('POSTDATA_LOGIN_URL')
api_endpoint = config('POSTDATA_API_ENDPOINT')
username = config('POSTDATA_USERNAME')
password = config('POSTDATA_PASSWORD')

# Payload for the login request
login_data = {
    'username': username,
    'password': password
}

def post_prompt_images(prompt, front_image, mask_image, labels):
    # Convert Pillow image to bytes
    front_image = front_image.convert('RGB')
    front_image_bytes = io.BytesIO()
    front_image.save(front_image_bytes, format='JPEG')
    front_image_bytes.seek(0)

    back_image = mask_image.convert('RGB')
    back_image_bytes = io.BytesIO()
    back_image.save(back_image_bytes, format='JPEG')
    back_image_bytes.seek(0)

    # Make a POST request to get JWT token
    response_login = requests.post(login_url, json=login_data)

    file_name = prompt.replace(' ','_').replace('.','')
    
    # Check if login was successful and obtain the token
    if response_login.status_code == 200:
        jwt_token = response_login.json().get('access')
        headers = {
            'Authorization': f'Bearer {jwt_token}',
        }


        # Add front and back images to the image data
        data = {
            'prompt': prompt,
            'inputs': labels
        }
        image_files = {
            'image': (f'{file_name}_front_image.jpg', front_image_bytes, 'image/jpeg'),
            'masked_image': (f'{file_name}_back_image.jpg', back_image_bytes, 'image/jpeg'),
        }

        # Make a POST request to upload image with JWT token as header
        response_upload = requests.post(api_endpoint, headers=headers, data=data, files=image_files)

        # Check if the image upload was successful
        if response_upload.status_code == 200:
            print('Image uploaded successfully!')
        else:
            print('Image upload failed:', response_upload.text)
    else:
        print('Login failed:', response_login.text)
