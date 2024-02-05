# Import the YOLO class from the Ultralytics library
from ultralytics import YOLO

# Load a pre-trained YOLO model for semantic segmentation of fashion items
model = YOLO('./ai_integration/model_weights/dress_seg.pt')  # load an official model

"""
Mapping of class indices to corresponding fashion item names for the YOLO model.
This mapping is crucial for identifying segmented fashion elements in the predictions.
"""
names = {
    0: 'bandeau_torso', 1: 'calf_hem', 2: 'cap_sleeve_left', 3: 'cap_sleeve_right',
    4: 'collar_neck_torso', 5: 'deep_round_neck_torso', 6: 'deep_v_neck_torso',
    7: 'depe_v_neck_torso', 8: 'elbow_sleeve_left', 9: 'elbow_sleeve_right',
    10: 'full_hem', 11: 'knee_hem', 12: 'long_sleeve_left', 13: 'long_sleeve_right',
    14: 'micro_mini_hem', 15: 'mini_hem', 16: 'one_shoulder_torso',
    17: 'shallow_round_neck', 18: 'shallow_v_neck', 19: 'square_neck_torso',
    20: 'straight_neck_torso', 21: 'turtle_neck_torso'
}

# Confidence threshold for filtering predictions
confidence = 0.1


# Function to retrieve predictions for torso segments in an image
def get_predictions_torso(img_path):
    # Predict on a local image
    predictions = model.predict(img_path, conf=confidence, verbose=False)

    # Initialize variables to store segment instances
    instance_torso = None

    try:
        for result in predictions:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks
            mask_list = [mask for mask in masks]
            for i in range(len(boxes)):
                # Filter predictions based on class indices related to torso
                if boxes[i].cls in [0, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21]:
                    instance_torso = mask_list[i]
                    break
    except Exception as e:
        pass

    return instance_torso


# Function to retrieve predictions for hem segments in an image
def get_predictions_hem(img_path):
    # Predict on a local image
    predictions = model.predict(img_path, conf=confidence, verbose=False)

    # Initialize variables to store segment instances
    instance_hem = None

    try:
        for result in predictions:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks
            mask_list = [mask for mask in masks]
            for i in range(len(boxes)):
                # Filter predictions based on class indices related to hem
                if boxes[i].cls in [1, 10, 11, 14, 15]:
                    instance_hem = mask_list[i]
                    break
    except Exception as e:
        pass

    return instance_hem


# Function to retrieve predictions for sleeves segments in an image
def get_predictions_sleeves(img_path):
    # Predict on a local image
    predictions = model.predict(img_path, conf=confidence, verbose=False)

    # Initialize variables to store segment instances for left and right sleeves
    instance_left_sleeve = None
    instance_right_sleeve = None

    try:
        for result in predictions:
            boxes = result.boxes  # Boxes object for bbox outputs
            masks = result.masks
            mask_list = [mask for mask in masks]
            for i in range(len(boxes)):
                # Filter predictions based on class indices related to left sleeves
                if boxes[i].cls in [2, 8, 12]:
                    if instance_left_sleeve is None:
                        instance_left_sleeve = mask_list[i]
                # Filter predictions based on class indices related to right sleeves
                if boxes[i].cls in [3, 9, 13]:
                    if instance_right_sleeve is None:
                        instance_right_sleeve = mask_list[i]
    except Exception as e:
        pass

    return instance_left_sleeve, instance_right_sleeve
