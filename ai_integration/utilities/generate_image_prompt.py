# Import the random module to facilitate random choices
import random

# Define a class for generating image prompts
class GenerateImagePrompt:
    def __init__(self, data):
        # Initialize the class with the provided data
        self.data = data

        # Extract relevant data from the input dictionary
        self.product_type = self.data['Q1']['Q1-types']
        self.product_type_sleeve = self.data['Q1']['Q12-sleeve']
        self.product_type_length = self.data['Q1']['Q11-length']
        self.product_fitting = self.data['Q2-fitting']
        self.product_occasion = self.data['Q3-occasion']
        self.product_style_list = self.data['Q4-style(max 2)']
        self.product_color_list = self.data['Q5-color(max 3)']
        self.product_shades = self.data['Q6-shades']
        self.product_style_trend = self.data['Q7-style']
        self.product_style_fabric = self.data['Q8-fabric']

        if self.product_type.lower()=='pants' or self.product_type.lower()=='shorts':
            self.product_type_prompt = f'{self.product_type}.'
        else:
            self.product_type_prompt = f'a {self.product_type}.'

        if self.product_type_sleeve=='Sleeveless':
            self.product_type_sleeve = 'be sleeveless'
        if self.product_type_sleeve=='Short/Cap Sleeve':
            self.product_type_sleeve = 'have short or cap sleeves'
        if self.product_type_sleeve=='Three-Quarter Length':
            self.product_type_sleeve = 'have three-quarter length sleeves'
        if self.product_type_sleeve=='Long Sleeve':
            self.product_type_sleeve = 'have long sleeves'
        if self.product_type_sleeve=='Strapless':
            self.product_type_sleeve = 'be strapless'
        if self.product_type_sleeve=='Spaghetti Straps':
            self.product_type_sleeve = 'have spaghetti straps'
        if self.product_type_sleeve=='Asymmetric/One-Shoulder':
            self.product_type_sleeve = 'be asymmetric or one shoulder'
        if self.product_type_sleeve=='':
            self.product_type_sleeve = random.choice(['be sleeveless','have short or cap sleeves','have three-quarter length sleeves','have long sleeves','be strapless','have spaghetti straps','be asymmetric or one shoulder'])


        # Generate a prompt based on the product type, sleeve, and length
        if self.product_type =='dress':
            if self.product_type_length=='Micro-Mini':
                self.product_type_length= 'micro-mini length'
            elif self.product_type_length=='Short':
                self.product_type_length= 'short length'
            elif self.product_type_length=='Knee-Length':
                self.product_type_length= 'knee length'
            elif self.product_type_length=='Ankle-Length':
                self.product_type_length= 'ankle length'
            elif self.product_type_length=='Midi':
                self.product_type_length= 'midi length'
            elif self.product_type_length=='Long':
                self.product_type_length= 'long length'
            self.product_type_prompt = self.product_type_prompt + f' It should be {self.product_type_length}. It should {self.product_type_sleeve}. '
        elif self.product_type =='jumpsuit':
            if self.product_type_length=='Micro-Mini':
                self.product_type_length= 'micro-mini length'
            elif self.product_type_length=='Short':
                self.product_type_length= 'short length'
            elif self.product_type_length=='Knee-Length':
                self.product_type_length= 'knee length'
            elif self.product_type_length=='Ankle-Length':
                self.product_type_length= 'ankle length'
            elif self.product_type_length=='Midi':
                self.product_type_length= 'midi length'
            elif self.product_type_length=='Long':
                self.product_type_length= 'long length'
            self.product_type_prompt = self.product_type_prompt + f' It should be {self.product_type_length}. It should {self.product_type_sleeve}. '
        elif self.product_type =='top':
            if self.product_type_length=='Cropped':
                self.product_type_length= 'cropped length'
            elif self.product_type_length=='Waist-Length':
                self.product_type_length= 'waist length'
            elif self.product_type_length=='Hip-Length':
                self.product_type_length= 'hip length'
            elif self.product_type_length=='Mid-Thigh Length':
                self.product_type_length= 'mid-thigh length'
            self.product_type_prompt = self.product_type_prompt + f' It should be {self.product_type_length}. It should {self.product_type_sleeve}. '
        elif self.product_type =='pants':
            if self.product_type_length=='Knee-Length':
                self.product_type_length= 'knee length'
            elif self.product_type_length=='Midi':
                self.product_type_length= 'three-quarter or midi length'
            elif self.product_type_length=='Long':
                self.product_type_length= 'ankle or long length'
            self.product_type_prompt = self.product_type_prompt + f' It should be {self.product_type_length}. '
        elif self.product_type =='skirt':
            if self.product_type_length=='Micro-Mini':
                self.product_type_length= 'micro-mini length'
            elif self.product_type_length=='Short':
                self.product_type_length= 'short length'
            elif self.product_type_length=='Knee-Length':
                self.product_type_length= 'knee length'
            elif self.product_type_length=='Ankle-Length':
                self.product_type_length= 'ankle length'
            elif self.product_type_length=='Midi':
                self.product_type_length= 'midi length'
            elif self.product_type_length=='Long':
                self.product_type_length= 'long length'
            self.product_type_prompt = self.product_type_prompt + f' It should be {self.product_type_length}. '
        elif self.product_type =='shorts':
            if self.product_type_length=='Short':
                self.product_type_length= 'mid-thigh length'
            elif self.product_type_length=='Knee-Length':
                self.product_type_length= 'knee length'
            self.product_type_prompt = self.product_type_prompt + f' It should be {self.product_type_length}. '

        # Generate prompts for fitting, occasion, and style
        if self.product_fitting!="":
            self.fitting_prompt = f"It should have a {self.product_fitting}."
        else:
            fitting = random.choice(['fitted or body-con silhouette', 'straight or relaxed silhouette', 'oversized or boxy silhouette', 'loose or flowing silhouette'])
            self.fitting_prompt = f"It should have a {fitting}."
        
        if self.product_occasion!="":
            # ["Casual", "Formal/Business", "Day-To-Night", "Evening"]
            if self.product_occasion=="Casual":
                self.product_occasion = 'casual'
            elif self.product_occasion=="Formal/Business":
                self.product_occasion = 'formal or business'
            elif self.product_occasion=="Day-To-Night":
                self.product_occasion = 'day and night'
            elif self.product_occasion=="Evening":
                self.product_occasion = 'evening'
            self.occasion_prompt = f"It should be suitable for a {self.product_occasion} event."
        else:
            occasion = random.choice(['casual', 'formal or business', 'day and night', 'evening'])
            self.occasion_prompt = f"It should be suitable for a {occasion} event."

        # Generate a style prompt based on the provided style list
        if len(self.product_style_list) == 2:
            self.style_prompt = f"And have a style that is {self.product_style_list[0]} and {self.product_style_list[1]}."
        elif len(self.product_style_list) == 1:
            self.style_prompt = f"And have a style that is {self.product_style_list[0]}."
        else:
            style = random.choice(["edgy/fashion-forward/avant-garde", "feminine", "glamorous", "urban", "classic", "natural"])
            self.style_prompt = f"And have a style that is {style}."

        # Generate prompts for color based on the provided color list
        if len(self.product_color_list) == 0:
            self.color_1  = random.choice(['green', 'blue', 'white', 'black', 'grey', 'purple', 'red', 'pink', 'yellow', 'orange', 'cream', 'gold', 'silver', 'beige', 'navy'])
            self.color_2  = random.choice(['green', 'blue', 'white', 'black', 'grey', 'purple', 'red', 'pink', 'yellow', 'orange', 'cream', 'gold', 'silver', 'beige', 'navy'])
            self.color_3  = random.choice(['green', 'blue', 'white', 'black', 'grey', 'purple', 'red', 'pink', 'yellow', 'orange', 'cream', 'gold', 'silver', 'beige', 'navy'])         
        elif len(self.product_color_list) == 3:
            self.color_1, self.color_2, self.color_3 = self.product_color_list[0], self.product_color_list[1], self.product_color_list[2]
        elif len(self.product_color_list) == 2:
            self.color_1, self.color_2, self.color_3 = self.product_color_list[0], self.product_color_list[1], random.choice(self.product_color_list)
        elif len(self.product_color_list) == 1:
           self.color_1, self.color_2, self.color_3 = self.product_color_list[0], self.product_color_list[0], self.product_color_list[0]
        if self.color_1=="No Idea - Inspire Me With Whats Trending":
            self.color_1  = "any colour that is trending this season and "#random.choice(['green', 'blue', 'white', 'black', 'grey', 'purple', 'red', 'pink', 'yellow', 'orange', 'cream', 'gold', 'silver', 'beige', 'navy'])
        if self.color_2=="No Idea - Inspire Me With Whats Trending":
            self.color_2  = "any colour that is trending this season and "#random.choice(['green', 'blue', 'white', 'black', 'grey', 'purple', 'red', 'pink', 'yellow', 'orange', 'cream', 'gold', 'silver', 'beige', 'navy'])
        if self.color_3=="No Idea - Inspire Me With Whats Trending":
            self.color_3  = "any colour that is trending this season and"#random.choice(['green', 'blue', 'white', 'black', 'grey', 'purple', 'red', 'pink', 'yellow', 'orange', 'cream', 'gold', 'silver', 'beige', 'navy'])    

        # if self.product_shades=="inspire me":
        #     self.product_shades = 'Use shade of <color_name>.' 
        # Generate Shade prompt
        if self.product_shades=='':
            self.product_shades = random.choice([
                "light and fresh based on warm undertones",
                "subtle and muted shades based on cool undertones",
                "bold and clear shades based on cool undertones",
                "bold and vibrant shades based on warm undertones",
                "metallic",
                ])

        if self.product_shades!="Use a color that is in line with this seasons trends":
            self.product_shades = 'Use a shade of <color_name> that is '+ self.product_shades
            self.product_shades = self.product_shades +'.'
        else:
            self.product_shades = self.product_shades +'.'
   

        if self.product_style_trend=="I am conservative in my fashion choices":
            self.product_style_trend = "Generate for someone that is conservative in their fashion choices."
        elif self.product_style_trend=="I like to be in line with trends":
            self.product_style_trend = "Generate for someone that likes being in line with trends."
        elif self.product_style_trend=="I like making a statement with my fashion choices":
            self.product_style_trend = "Generate for someone that likes making a statement/is experimental/adventurous with their fashion choices."
        else:
            self.product_style_trend = random.choice(['Generate for someone that likes being in line with trends.', 'Generate for someone that is conservative in their fashion choices.', 'Generate for someone that likes making a statement with their fashion choices/ is experimental/adventurous with their fashion choices.'])
            

        if self.product_style_fabric=="":
            self.product_style_fabric= random.choice(["Use warm fabrics suitable for winter.", "Use cool or lightweight fabrics suitable for summer.", "Use silky or soft fabrics that skim the body.", "Use structured fabrics that hold their shape.", "Use eveningwear, textured, tactile or luxury fabrics.", "Use the most suitable fabric for this type of design."])
        else:
            self.product_style_fabric = "Use "+self.product_style_fabric+'.'
        # Define lists of variant necklines and features for later use
        self.variant_necklines_list = [
            'shallow v neck', 'deep v neck', 'shallow round neck', 'deep round neck',
            'straight neckline', 'square neckline', 'sweetheart neckline',
            'halterneck', 'crew neck', 'polo neck', 'shirt collar neck', 'turtle neck', ''
        ]
        self.variant_features_list = [
            'buttons', 'side zip', 'front zip', 'back zip',
            'ruching', 'front slit', 'side slit',
            'shirt style buttoned cuff', 'wrap style', 'pockets', 'no pockets',
            'zip', 'pull on', 'high waisted', 'low waisted', 'waistband', 'no waistband', ''
        ]

    # Method to generate the main image prompt
    def generate_main_image_prompt(self):
        # Replace <color_name> in shades with the first color
        if 'Use a color that is in line with this seasons trends' in self.product_shades:
            shade = 'Use a color that is in line with this seasons trends'
        elif self.product_shades=='':
            shade = ''
        else:
            shade = self.product_shades.replace('<color_name>', self.color_1)
        # Construct the final prompt for the main image
        final_prompt = f"""Generate just one photorealistic forward-facing product-only view of {self.product_type_prompt} {self.fitting_prompt} {self.occasion_prompt} {self.style_prompt} {shade} {self.product_style_trend} {self.product_style_fabric} Only show one front-facing view against a plain white background."""
        return final_prompt

    # Method to generate the second image prompt
    def generate_second_image_prompt(self):
        # Replace <color_name> in shades with the second color
        if 'Use a color that is in line with this seasons trends' in self.product_shades:
            shade = 'Use a color that is in line with this seasons trends'
        elif self.product_shades=='':
            shade = ''
        else:
            shade = self.product_shades.replace('<color_name>', self.color_2)
        # Randomly select a neckline and a clothing feature
        selected_neckline = random.choice(self.variant_necklines_list)
        if selected_neckline=='':
            neckline_prompt = ''
        else:
            neckline_prompt = f'It may have {selected_neckline}.'
        selected_clothing_feature = random.choice(self.variant_features_list)
        if selected_clothing_feature=='':
            selected_clothing_prompt = ''
        else:
            selected_clothing_prompt = f'It may have {selected_clothing_feature}.'
        # Construct the final prompt for the second image
        if self.product_type=='pants' or self.product_type=='shorts' or self.product_type=='skirt' or self.product_type_sleeve=='be asymmetric or one shoulder' or self.product_type_sleeve=='be sleeveless' or self.product_type_sleeve=='have spaghetti straps' or self.product_type_sleeve=='be strapless':
            final_prompt = f"""Generate just one photorealistic forward-facing product-only view of {self.product_type_prompt} {self.fitting_prompt} {selected_clothing_prompt} {self.occasion_prompt} {self.style_prompt} {shade} {self.product_style_trend} {self.product_style_fabric} Only show one front-facing view against a plain white background."""
        else:
            final_prompt = f"""Generate just one photorealistic forward-facing product-only view of {self.product_type_prompt} {self.fitting_prompt} {neckline_prompt} {selected_clothing_prompt} {self.occasion_prompt} {self.style_prompt} {shade} {self.product_style_trend} {self.product_style_fabric} Only show one front-facing view against a plain white background."""
        return final_prompt

    # Method to generate the third image prompt
    def generate_third_image_prompt(self):
        # Replace <color_name> in shades with the third color
        if 'Use a color that is in line with this seasons trends.' in self.product_shades:
            shade = 'Use a color that is in line with this seasons trends.'
        elif self.product_shades=='':
            shade = ''
        else:
            shade = self.product_shades.replace('<color_name>', self.color_3)
        # Randomly select a neckline and a clothing feature
        selected_neckline = random.choice(self.variant_necklines_list)
        if selected_neckline=='':
            neckline_prompt = ''
        else:
            neckline_prompt = f'It may have {selected_neckline}.'
        selected_clothing_feature = random.choice(self.variant_features_list)
        if selected_clothing_feature=='':
            selected_clothing_prompt = ''
        else:
            selected_clothing_prompt = f'It may have {selected_clothing_feature}.'
        # Construct the final prompt for the second image
        if self.product_type=='pants' or self.product_type=='shorts' or self.product_type=='skirt' or self.product_type_sleeve=='be asymmetric or one shoulder' or self.product_type_sleeve=='be sleeveless' or self.product_type_sleeve=='have spaghetti straps' or self.product_type_sleeve=='be strapless':
            final_prompt = f"""Generate just one photorealistic forward-facing product-only view of {self.product_type_prompt} {self.fitting_prompt} {selected_clothing_prompt} {self.occasion_prompt} {self.style_prompt} {shade} {self.product_style_trend} {self.product_style_fabric} Only show one front-facing view against a plain white background."""
        else:
            final_prompt = f"""Generate just one photorealistic forward-facing product-only view of {self.product_type_prompt} {self.fitting_prompt} {neckline_prompt} {selected_clothing_prompt} {self.occasion_prompt} {self.style_prompt} {shade} {self.product_style_trend} {self.product_style_fabric} Only show one front-facing view against a plain white background."""
        return final_prompt
