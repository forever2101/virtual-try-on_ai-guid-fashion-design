# Import necessary libraries
import os
from openai import OpenAI
import json
import requests
from PIL import Image
from io import BytesIO
import base64
import time
from decouple import config

# Get API key and model from environment variables
api_key = config('OPENAI_API_KEY')
model = config('OPENAI_MODEL_GPT4_VISION')

# Create OpenAI client
client = OpenAI(
    api_key=api_key,
)

def analysis_image_variants(img):
    # img = img.convert('RGBA')

    # Convert the  Pillow image into binary mode
    buffer1 = BytesIO()
    img.save(buffer1, format='PNG')  # Change format if needed (JPEG, PNG, etc.)
    # buffer1.seek(0)
    # img_bytes = buffer1.read()
    base64_image =  base64.b64encode(buffer1.getvalue()).decode('utf-8')
    delay = 3
    while(True):
        try:
            response = client.chat.completions.create(
            model=model,
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": "for the product in image fill up the below form, and also provide extra tags that would be useful to labelling data. provide output in exact same format text colour [ ] colour shade [ ] product type [ ] sleeve length [ ] sleeve style [ ] neckline [ ] hem length [ ] trend parameter [1-5] fashion style [ ] print type [ ] print size [ ] bodice style [ ] bodice length [ ] fit [ ] buttons[yes, no] zip [yes, no] image view [front, back] skirt style [ ] pleats [yes, no] ruffles [yes, no]"},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
            )

            response = json.loads(response.model_dump_json())['choices'][0]['message']['content']

            return response
        except Exception as e:
            print(f"Error encountered: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

def analysis_image_v2(url):
    try:
        response = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "for the product in image fill up the below form. provide output in exact same format -> Count all objects in image [ ] is there mannequin or human or dummy in image? [yes, no]"},
                {
                "type": "image_url",
                "image_url": {
                    # "url": f"data:image/jpeg;base64,{url}",
                    "url": url,

                },
                },
            ],
            }
        ],
        max_tokens=300,
        )

        response = json.loads(response.model_dump_json())['choices'][0]['message']['content']

        return response
    except:
        return "Count objects in image [ ] mannequin/human/dummy in image? [yes, no]"


def analysis_image(url):
    try:
        response = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "for the product in image fill up the below form, and also provide extra tags that would be useful to labelling data. provide output in exact same format text colour [ ] colour shade [ ] product type [ ] sleeve length [ ] sleeve style [ ] neckline [ ] hem length [ ] trend parameter [1-5] fashion style [ ] print type [ ] print size [ ] bodice style [ ] bodice length [ ] fit [ ] buttons[yes, no] zip [yes, no] image view [front, back] skirt style [ ] pleats [yes, no] ruffles [yes, no] Count all objects in image [ ] is there mannequin or human or dummy in image? [yes, no]"},
                {
                "type": "image_url",
                "image_url": {
                    # "url": f"data:image/jpeg;base64,{url}",
                    "url": url,

                },
                },
            ],
            }
        ],
        max_tokens=300,
        )

        response = json.loads(response.model_dump_json())['choices'][0]['message']['content']

        return response
    except:
        return "text colour [ ] colour shade [ ] product type [ ] sleeve length [ ] sleeve style [ ] neckline [ ] hem length [ ] trend parameter [1-5] fashion style [ ] print type [ ] print size [ ] bodice style [ ] bodice length [ ] fit [ ] buttons[yes, no] zip [yes, no] image view [front, back] skirt style [ ] pleats [yes, no] ruffles [yes, no]  Count objects in image [ ] mannequin/human/dummy in image? [yes, no]"

def check_number_objects(url):
    try:
        response = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "in the image provided are there more than one clothing product? provide answer in yes or no"},
                {
                "type": "image_url",
                "image_url": {
                    "url": url,
                },
                },
            ],
            }
        ],
        max_tokens=250,
        )

        response = json.loads(response.model_dump_json())['choices'][0]['message']['content']

        print(response)

        print(f'response -> {response}')

        if 'no' in response.lower():
            return 'no'
        else:
            return 'yes'

    except:
        return "yes"

def check_product_only(url):
    # try:
    response = client.chat.completions.create(
    model=model,
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "In the image provided if there are any humans or dummies or models or mannequins and if the image is not a product only image then answer yes. Otherwise answer no"},
            {
            "type": "image_url",
            "image_url": {
                # "url": f"data:image/jpeg;base64,{url}",
                "url": url,
                "detail": "low"
            },
            },
        ],
        }
    ],
    max_tokens=250,
    )

    response = json.loads(response.model_dump_json())['choices'][0]['message']['content']

    print(f'response -> {response}')

    if 'no' in response.lower():
        return 'no'
    else:
        return 'yes'

def get_image_prompt(prompt,img):
    img = img.convert('RGB')
    img_byte_array = BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()
    # Encode the image bytes to base64
    base64_image = base64.b64encode(img_byte_array).decode('utf-8')

    try:
        response = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )

        response = json.loads(response.model_dump_json())['choices'][0]['message']['content']

        return response
    except Exception as e:
        print(f"Error encountered: {e}")