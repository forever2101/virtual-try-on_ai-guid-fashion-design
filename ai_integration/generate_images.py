import random
from .utilities.generate_image_prompt import GenerateImagePrompt
from .utilities.count_objects import count_objects
from .utilities.analysis_image_gpt4 import analysis_image, check_product_only, analysis_image_v2
from .utilities.change_background import change_background_white, change_background_transparent
from .utilities.post_prompt_image import post_prompt_images
from .utilities.generate_image_dalle import generate_image
import json
import copy 
from .utilities.get_predections_yolo import get_predictions_sleeves, get_predictions_torso
from PIL import Image
from .utilities.back_segment_processing import transparent_segment
from .utilities.generate_dalle_inpainting import generate_inpainting_back
from django.db import models
from django.contrib.postgres.fields import JSONField
from io import BytesIO
from django.core.files.base import ContentFile
import io
import concurrent.futures
from questions.models import QAResponse
from promptdatabase.models import Prompt
import time

def convert_pillow_image_to_django_file(pillow_image, image_format='PNG', image_name='image.png'):
    image_io = BytesIO()
    pillow_image.save(image_io, format=image_format)
    image_io.seek(0)
    image_file = ContentFile(image_io.getvalue(), name=image_name)
    return image_file

def check_generate(prompt, response, generated_images):
    count = 0
    # prompt_number = 0
    while True:
        if count>4 or len(generated_images)==2:
            return generated_images
        print('Attempt : ',count+1)

        # prompt = prompt_list[prompt_number]
        generated_image, url = generate_image(prompt)

        if generated_image!=None:
            # qa_response = QAResponse()
            # qa_response.question_response = response
            # qa_response.image = convert_pillow_image_to_django_file(change_background_transparent(generated_image), 'png', 'variant_qa.png')
            # qa_response.image_prompt = prompt

            qa_create = Prompt()
            qa_create.prompt = prompt
            qa_create.survey_response = response
            qa_create.image = convert_pillow_image_to_django_file(change_background_transparent(generated_image), 'png', 'variant_qa.png')


            generated_image_labels = analysis_image_v2(url)
            qa_create.qa = generated_image_labels

            # Extract information
            count_objects_index = generated_image_labels.lower().find("count all objects in image [")
            is_mannequin_index = generated_image_labels.lower().find("is there mannequin or human or dummy in image? [")

            # Get the count of objects
            try:
                count_objects_value = int(generated_image_labels[count_objects_index + len("Count all objects in image ["):generated_image_labels.find("]", count_objects_index)])
            except ValueError:
                # Set count_objects_value to 0 if conversion to int fails
                count_objects_value = 0

            # Check if there is a mannequin
            is_product = generated_image_labels[is_mannequin_index + len("is there mannequin or human or dummy in image? ["):generated_image_labels.find("]", is_mannequin_index)]


            if count_objects_value == 1 and is_product == 'no':
                print('qa pass')
                # qa_response.qa_status = 'pass'
                qa_create.accept = True
                generated_images.append(change_background_transparent(generated_image))
                try:
                    # qa_response.save()
                    # pass
                    qa_create.save()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    
            else:
                print('qa fail')
                qa_create.accept = False
                # qa_response.qa_status = 'fail'
                try:
                    qa_create.save()
                    # qa_response.save()
                    # pass
                except Exception as e:
                    print(f"An error occurred: {e}")
        else:
            print('Image generation fail')
        count+=1

# Function to send data using separated front and back images
def send_data(prompt, image, image_labels):
    # front_image, back_image = seprate_front_back(image)
    post_prompt_images(prompt, front_image=image, mask_image=image,  labels=image_labels)

# Function to swap neckline and torso between the original and reference images
def gen_variant_back(img):
    pred_torso = get_predictions_torso(img)

    img = change_background_white(img).convert('RGBA')
    # print(img)
    if pred_torso!=None:
        new_img = copy.deepcopy(img)
        mask_img = transparent_segment(new_img, pred_torso)
        mask_img = mask_img.convert('RGBA')
        # mask_img.show()
        prompt = 'Generate back view of the clothing product'

        inpainting = generate_inpainting_back(new_img,mask_img,prompt)
        inpainting = change_background_transparent(inpainting)

        return convert_pillow_image_to_django_file(inpainting, 'png', 'back.png')
    else:
        return convert_pillow_image_to_django_file(change_background_transparent(img), 'png', 'back.png')


def generate_image_con(prompt, response, prompt_number):
    print(f'Generating Image {prompt_number} ....')
    return check_generate(prompt, response)


def generateImages(json_data):
    data = json.loads(json_data['response'])
    # print(data)
    prompt_object = GenerateImagePrompt(data)

    generated_images = []

    start_time = time.time()

    # print('Generating variant 1')
    main_prompt = prompt_object.generate_main_image_prompt()
    second_prompt = prompt_object.generate_second_image_prompt()
    third_prompt = prompt_object.generate_third_image_prompt()

    prompt_list = [main_prompt,second_prompt,third_prompt]
    print('Generating Image 1 ....')
    # generate_image_1, genrated_image1_labels = check_generate(main_prompt)
    # generated_images = check_generate(main_prompt, data, generated_images)
    generated_images = check_generate(main_prompt, data, generated_images)

    print('Generating variant 2')
    generated_images = check_generate(second_prompt, data, generated_images)
    # print('Generating Image 2 ....')
    # generate_image_2, genrated_image2_labels = check_generate(second_prompt)

    print('Generating variant 3')
    generated_images = check_generate(third_prompt, data, generated_images)
    # print('Generating Image 3 ....')
    # generate_image_3, genrated_image3_labels = check_generate(third_prompt)

    end_time = time.time() - start_time

    print(f'Time taken for generation -> {end_time} sec')

    generate_image_1 =None
    generate_image_2 =None
    generate_image_3 =None

    if len(generated_images)==1:
        generate_image_1 = convert_pillow_image_to_django_file(generated_images[0], 'png', 'first.png')
        generate_image_2 = None
        generate_image_3 = None
    elif len(generated_images)==2:
        generate_image_1 = convert_pillow_image_to_django_file(generated_images[0], 'png', 'first.png')
        generate_image_2 = convert_pillow_image_to_django_file(generated_images[1], 'png', 'second.png')
        generate_image_3 = None
    elif len(generated_images)==3:
        generate_image_1 = convert_pillow_image_to_django_file(generated_images[0], 'png', 'first.png')
        generate_image_2 = convert_pillow_image_to_django_file(generated_images[1], 'png', 'second.png')
        generate_image_3 = convert_pillow_image_to_django_file(generated_images[2], 'png', 'third.png')



    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     # Adjust the prompt_object and prompt_number accordingly
    #     future1 = executor.submit(generate_image_con, main_prompt, data, 1)
    #     future2 = executor.submit(generate_image_con, second_prompt, data, 2)
    #     # future3 = executor.submit(generate_image_con, third_prompt, 3)

    #     # Wait for all tasks to complete
    #     concurrent.futures.wait([future1, future2])

    #     # Get the results
    #     generate_image_1, genrated_image1_labels = future1.result()
    #     generate_image_2, genrated_image2_labels = future2.result()
        # generate_image_3, genrated_image3_labels = future3.result()

    return generate_image_1, generate_image_2, generate_image_3


