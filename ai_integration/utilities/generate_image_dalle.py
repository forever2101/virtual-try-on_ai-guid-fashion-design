# Import necessary modules and classes
import os
from openai import AzureOpenAI
import json
import requests
from PIL import Image
from io import BytesIO
import time

from decouple import config

# Retrieve Azure OpenAI API configuration from environment variables
api_key = config('AZURE_API_KEY_DALLE3')
api_version = config('AZURE_API_VERSION_DALLE3')
azure_endpoint = config('AZURE_ENDPOINT_DALLE3')
model = config('AZURE_MODEL_DALLE_CREATE')

# Create an instance of the AzureOpenAI client with the provided API key and endpoint
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    api_key=api_key,
)

# Function to convert an image URL to a Pillow Image object
def url_to_image(image_url):
    # Make a GET request to download the image
    response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Read the content of the response (image data) into a BytesIO object
        image_data = BytesIO(response.content)

        # Open the image from the BytesIO object using Pillow
        image_pil = Image.open(image_data)
        # image_pil.show()  # Uncomment this line to display the downloaded image
        return image_pil

    else:
        print('Failed to download the image from ', image_url)
        return None

# Function to generate an image based on a prompt using the Azure OpenAI model
def generate_image(prompt):
    # delay = 3
    count = 4

    # Retry up to 4 times in case of errors
    while count != 0:
        try:
            count -= 1
            # Make a request to the Azure OpenAI API to generate an image
            result = client.images.generate(
                model=model,
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard",
            )

            # Extract the generated image URL from the API response
            image_url = json.loads(result.model_dump_json())['data'][0]['url']

            # Call the function to convert the image URL to a Pillow Image object
            return url_to_image(image_url), image_url

        except Exception as e:
            print(f"Error encountered: {e}")
            # print(f"Retrying in {delay} seconds...")
            # time.sleep(delay)

    # Return None if the image generation fails after multiple retries
    return None, None
