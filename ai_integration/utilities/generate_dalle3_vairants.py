# Import necessary utilities and modules
from ..utilities.generate_image_dalle import generate_image
from ..utilities.analysis_image_gpt4 import analysis_image_variants
from ..utilities.get_predections_yolo import get_predictions_hem, get_predictions_sleeves
import time

# Set delay for retrying in case of errors
delay = 3

# Function to generate DALL-E variant for skirt based on specified hem length
def gen_dalle_vairant_skirt(img, change_length):
    # Get the analysis prompt for the input image
    prompt = analysis_image_variants(img)

    # Extract the specified hem length from the input
    change_length = change_length.split('-')[0]

    # Define categories for different hem lengths
    if change_length.lower() == 'full':
        change_length_check = ['full', 'long', 'midi']
    if change_length.lower() == 'knee':
        change_length_check = ['knee', 'mid']
    if change_length.lower() == 'mini':
        change_length_check = ['mini', 'short']

    # Extract relevant information from the analysis prompt
    hem_index = prompt.index('hem length')
    tren_index = prompt.index('trend parameter')
    hem_fit = prompt.index('fit [')
    tren_but = prompt.index('buttons [')
    analyis_hem_fit = prompt[hem_fit:tren_but]
    index_open_brac_fit = analyis_hem_fit.index('[')
    index_close_brac_fit = analyis_hem_fit.index(']')
    analyis_hem_fit = analyis_hem_fit[index_open_brac_fit+1:index_close_brac_fit]
    skirt_style = prompt.index('skirt style [')
    pleat_index = prompt.index('pleats [')
    analyis_skirt_style = prompt[skirt_style:pleat_index]
    index_open_brac_style = analyis_skirt_style.index('[')
    index_close_brac_style = analyis_skirt_style.index(']')
    analyis_skirt_style = analyis_skirt_style[index_open_brac_style+1:index_close_brac_style]

    # Create a new prompt with the specified hem length
    new_prompt = 'Generate a realistic single front view of a product with following specification: \n' + \
        prompt[:hem_index] + f'hem length [{change_length}] \n' + prompt[tren_index:]

    count = 0
    # Retry up to 10 times in case of errors
    while count < 10:
        try:
            # Generate a new image variant using DALL-E
            new_variant, _ = generate_image(new_prompt)
            # Get the analysis prompt for the generated variant
            prompt_qa = analysis_image_variants(new_variant)

            # Extract relevant information from the analysis prompt of the generated variant
            hem_index_qa = prompt_qa.index('hem length')
            tren_index_qa = prompt_qa.index('trend parameter')
            analyis_hem_length_qa = prompt_qa[hem_index_qa:tren_index_qa]
            index_open_brac_hem = analyis_hem_length_qa.index('[')
            index_close_brac_hem = analyis_hem_length_qa.index(']')
            analyis_hem_length_qa = analyis_hem_length_qa[index_open_brac_hem+1:index_close_brac_hem]

            hem_fit_qa = prompt_qa.index('fit [')
            tren_but_qa = prompt_qa.index('buttons')
            analyis_hem_fit_qa = prompt_qa[hem_fit_qa:tren_but_qa]
            index_open_brac_fit = analyis_hem_fit_qa.index('[')
            index_close_brac_fit = analyis_hem_fit_qa.index(']')
            analyis_hem_fit_qa = analyis_hem_fit_qa[index_open_brac_fit+1:index_close_brac_fit]

            skirt_style_qa = prompt_qa.index('skirt style [')
            pleat_index_qa = prompt_qa.index('pleats')
            analyis_skirt_style_qa = prompt_qa[skirt_style_qa:pleat_index_qa]
            index_open_brac_ss = analyis_skirt_style_qa.index('[')
            index_close_brac_ss = analyis_skirt_style_qa.index(']')
            analyis_skirt_style_qa = analyis_skirt_style_qa[index_open_brac_ss+1:index_close_brac_ss]

            # Check if the generated variant meets the specified criteria
            qa_hem_length = False
            for i in change_length_check:
                if i in analyis_hem_length_qa.lower():
                    qa_hem_length = True
                    break

            if (analyis_skirt_style_qa.lower() in analyis_skirt_style.lower() or analyis_skirt_style.lower() in analyis_skirt_style_qa.lower()) and qa_hem_length and (analyis_hem_fit_qa.lower() in analyis_hem_fit.lower() or analyis_hem_fit.lower() in analyis_hem_fit_qa.lower()) and get_predictions_hem(new_variant) != None:
                print('QA pass')
                return new_variant
            else:
                print(f'Image generated QA failed, trying again in {delay} sec...')
                time.sleep(delay)
                count += 1

        except:
            continue

    return None


# Function to generate DALL-E variant for sleeve based on specified sleeve length
def gen_dalle_vairant_sleeve(img, sleeve_length):
    # Get the analysis prompt for the input image
    prompt = analysis_image_variants(img)

    # Extract the specified sleeve length from the input
    sleeve_length = sleeve_length.split('-')[0]

    # Define categories for different sleeve lengths
    if sleeve_length.lower() == 'cap':
        sleeve_length_check = ['short', 'cap']
    if sleeve_length.lower() == 'elbow':
        sleeve_length_check = ['half', 'quater']
    if sleeve_length.lower() == 'full':
        sleeve_length_check = ['full', 'long']

    # Extract relevant information from the analysis prompt
    sleeve_index = prompt.index('sleeve length')
    style_index = prompt.index('sleeve style')
    neckline_index = prompt.index('neckline')
    analyis_sleeve_style = prompt[style_index:neckline_index]
    index_open_brac_style = analyis_sleeve_style.index('[')
    index_close_brac_style = analyis_sleeve_style.index(']')
    org_analyis_sleeve_style = analyis_sleeve_style[index_open_brac_style+1:index_close_brac_style]

    # Create a new prompt with the specified sleeve length
    new_prompt = 'Generate a realistic single front view of a product with following specification: \n' + \
        prompt[:sleeve_index] + f'sleeve length [{sleeve_length}] \n' + prompt[style_index:]

    count = 0
    # Retry up to 10 times in case of errors
    while count < 10:
        try:
            # Generate a new image variant using DALL-E
            new_variant, _ = generate_image(new_prompt)

            # Get the analysis prompt for the generated variant
            prompt_qa = analysis_image_variants(new_variant)

            # Extract relevant information from the analysis prompt of the generated variant
            sleeve_index_qa = prompt_qa.index('sleeve length')
            style_index_qa = prompt_qa.index('sleeve style')
            analyis_sleeve_length = prompt_qa[sleeve_index_qa:style_index_qa]
            index_open_brac_len = analyis_sleeve_length.index('[')
            index_close_brac_len = analyis_sleeve_length.index(']')
            analyis_sleeve_length = analyis_sleeve_length[index_open_brac_len+1:index_close_brac_len]
            neckline_index_qa = prompt_qa.index('neckline')
            analyis_sleeve_style = prompt_qa[style_index_qa:neckline_index_qa]
            index_open_brac_style = analyis_sleeve_style.index('[')
            index_close_brac_style = analyis_sleeve_style.index(']')
            analyis_sleeve_style = analyis_sleeve_style[index_open_brac_style+1:index_close_brac_style]

            # Check if the generated variant meets the specified criteria
            left, right = get_predictions_sleeves(new_variant)

            qa_sleeve_length = False
            for i in sleeve_length_check:
                if i in analyis_sleeve_length.lower():
                    qa_sleeve_length = True
                    break

            if qa_sleeve_length and left != None and right != None:
                print('QA pass')
                return new_variant
            else:
                print(f'Image generated QA failed, trying again in {delay} sec...')
                time.sleep(delay)
                count += 1

        except:
            continue

    return None

