#This file was originally for create module qa but now we are using GPT vision for count images

# Import necessary libraries and modules
from PIL import Image
import cv2
from ultralytics import YOLO
import numpy as np

# Load YOLO model with pre-trained weights
model = YOLO('./ai_integration/model_weights/types_yolo_best.pt')

'''
Public model not inhouse trained
Classes model trained on

Dress
Jumper
Polo
tshirt
Skirt
Shirt
Hoodie
Jeans
Coat
Shorts
'''

# Confidence threshold for filtering predictions
confidence = 0.8

# Function to count the number of objects in an image
def count_objects(img):
    # Convert the image to a NumPy array
    img_np = np.array(img)

    # Use YOLO model to predict objects in the image
    predictions = model.predict(img_np, conf=confidence, verbose=False)

    # Initialize counts for each object type
    object_count = 0
    dress_count = 0
    jumper_count = 0
    polo_count = 0
    tshirt_count = 0
    skirt_count = 0
    shirt_count = 0
    hoodie_count = 0
    jeans_count = 0
    coat_count = 0
    shorts_count = 0

    # Iterate through the predictions to count each object type
    for result_types in predictions:
        boxes_types = result_types.boxes
        for i in boxes_types:
            if i.cls.numpy()[0] == 0.0:
                dress_count += 1
            if i.cls.numpy()[0] == 1.0:
                jumper_count += 1
            if i.cls.numpy()[0] == 2.0:
                polo_count += 1
            if i.cls.numpy()[0] == 3.0:
                tshirt_count += 1
            if i.cls.numpy()[0] == 4.0:
                skirt_count += 1
            if i.cls.numpy()[0] == 5.0:
                shirt_count += 1
            if i.cls.numpy()[0] == 6.0:
                hoodie_count += 1
            if i.cls.numpy()[0] == 7.0:
                jeans_count += 1
            if i.cls.numpy()[0] == 8.0:
                coat_count += 1
            if i.cls.numpy()[0] == 9.0:
                shorts_count += 1

    # Determine the dominant object type based on counts
    if dress_count > 0 or coat_count > 0:
        return max(dress_count, coat_count)
    elif jumper_count > 0:
        return jumper_count
    elif polo_count > 0 or tshirt_count > 0 or shirt_count > 0 or hoodie_count > 0:
        return max(hoodie_count, tshirt_count, shirt_count, hoodie_count)
    elif skirt_count > 0:
        return skirt_count
    elif shorts_count > 0:
        return shorts_count
    elif jeans_count > 0:
        return jeans_count
    else:
        return object_count
