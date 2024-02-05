from sklearn.cluster import KMeans
import numpy as np
from PIL import Image, ImageDraw

#Function to detect major color of image
def detect_major_color(img):
    # Get the dimensions of the image
    width, height = img.size

    # Calculate the dimensions for the center portion (30% of the width and height)
    left = int(0.35 * width)
    top = int(0.35 * height)
    right = int(0.65 * width)
    bottom = int(0.65 * height)

    img_center = img.crop((left, top, right, bottom))
    img_rgb = img_center.convert("RGB")

    # img_rgb.show()

    img_array = np.array(img_rgb)
    pixel_values = img_array.reshape((-1, 3))

    # Create a KMeans object with the desired number of clusters
    kmeans = KMeans(n_clusters=2, n_init=1)

    # Fit the KMeans object to the image array
    kmeans.fit(pixel_values)

    # Get the cluster labels for each pixel in the image
    cluster_labels = kmeans.predict(pixel_values)

    # Group the pixels by cluster label
    clusters = np.unique(cluster_labels)

    # Calculate the mean RGB values for each cluster
    cluster_means = []
    for cluster in clusters:
        cluster_mean = np.mean(pixel_values[cluster_labels == cluster], axis=0)
        cluster_means.append(cluster_mean)

    # Sort the clusters by the mean RGB values
    cluster_means.sort(key=lambda x: x[0])


    # Get the color names for the top k dominant colors
    color_names = []
    for cluster_mean in cluster_means[:2]:
        # color_name = plt.color.rgb2hex(color_name)
        # color_name = '#%02x%02x%02x' % (int(cluster_mean[0]), int(cluster_mean[1]), int(cluster_mean[2]))
        color_name = (int(cluster_mean[0]), int(cluster_mean[1]), int(cluster_mean[2]))
        color_names.append(color_name)
    
    # print(color_names)

    return color_names[1]




#Function to detect major color of image
def detect_second_major_color(img):
    # Get the dimensions of the image
    width, height = img.size

    # Calculate the dimensions for the center portion (30% of the width and height)
    left = int(0.35 * width)
    top = int(0.35 * height)
    right = int(0.65 * width)
    bottom = int(0.65 * height)

    img_center = img.crop((left, top, right, bottom))
    img_rgb = img_center.convert("RGB")

    # img_rgb.show()

    img_array = np.array(img_rgb)
    pixel_values = img_array.reshape((-1, 3))

    # Create a KMeans object with the desired number of clusters
    kmeans = KMeans(n_clusters=2, n_init=1)

    # Fit the KMeans object to the image array
    kmeans.fit(pixel_values)

    # Get the cluster labels for each pixel in the image
    cluster_labels = kmeans.predict(pixel_values)

    # Group the pixels by cluster label
    clusters = np.unique(cluster_labels)

    # Calculate the mean RGB values for each cluster
    cluster_means = []
    for cluster in clusters:
        cluster_mean = np.mean(pixel_values[cluster_labels == cluster], axis=0)
        cluster_means.append(cluster_mean)

    # Sort the clusters by the mean RGB values
    cluster_means.sort(key=lambda x: x[0])


    # Get the color names for the top k dominant colors
    color_names = []
    for cluster_mean in cluster_means[:2]:
        # color_name = plt.color.rgb2hex(color_name)
        # color_name = '#%02x%02x%02x' % (int(cluster_mean[0]), int(cluster_mean[1]), int(cluster_mean[2]))
        color_name = (int(cluster_mean[0]), int(cluster_mean[1]), int(cluster_mean[2]))
        color_names.append(color_name)
    
    # print(color_names)

    return color_names[0]

#Function to detect major color of segment
def detect_major_color_segment(img):

    # img_rgb.show()

    img_array = np.array(img.convert('RGB'))
    pixel_values = img_array.reshape((-1, 3))

    # Create a KMeans object with the desired number of clusters
    kmeans = KMeans(n_clusters=2, n_init=1)

    # Fit the KMeans object to the image array
    kmeans.fit(pixel_values)

    # Get the cluster labels for each pixel in the image
    cluster_labels = kmeans.predict(pixel_values)

    # Group the pixels by cluster label
    clusters = np.unique(cluster_labels)

    # Calculate the mean RGB values for each cluster
    cluster_means = []
    for cluster in clusters:
        cluster_mean = np.mean(pixel_values[cluster_labels == cluster], axis=0)
        cluster_means.append(cluster_mean)

    # Sort the clusters by the mean RGB values
    cluster_means.sort(key=lambda x: x[0])


    # Get the color names for the top k dominant colors
    color_names = []
    for cluster_mean in cluster_means[:2]:
        # color_name = plt.color.rgb2hex(color_name)
        # color_name = '#%02x%02x%02x' % (int(cluster_mean[0]), int(cluster_mean[1]), int(cluster_mean[2]))
        color_name = (int(cluster_mean[0]), int(cluster_mean[1]), int(cluster_mean[2]))
        color_names.append(color_name)
    
    # print(color_names)


    return color_names[1]

#Function to change color to object
def blend_new_color(img, detected_color, new_color):
    img_rgba = img.convert("RGBA")
    width, height = img.size

    # Loop through each pixel and apply the same logic for RGBA values
    for y in range(height):
        for x in range(width):
            # Get the pixel at the current location
            current_pixel = img_rgba.getpixel((x, y))

            # Separate alpha channel from RGB channels
            alpha = current_pixel[3]
            blended_rgb = tuple(max(0, min(255, value - detected_color[i] + new_color[i])) for i, value in enumerate(current_pixel[:3]))

            # Combine the blended RGB values with the original alpha channel
            new_pixel = blended_rgb + (alpha,)

            # Update the pixel in the image
            img_rgba.putpixel((x, y), new_pixel)

    return img_rgba

#Function to add pattern to object
def blend_pattern_segments(img, detected_color, pattern, segments):
    # Resize pattern to match original image dimensions
    pattern = pattern.resize(img.size)
    
    # Loop through each pixel and reduce its RGB values 
    for segment in segments:
        # segment_x = int(segment['x']) - int(segment['width'])
        # segment_y = int(segment['y']) - int(segment['height'])

        xy = segment.xy[0]

        # Separate X and Y values into 1D arrays
        x_values = list(xy[:, 0])
        y_values = list(xy[:, 1])

        # Extract bounding box information from segment points
        min_x, min_y = min(x_values), min(y_values)
        max_x, max_y = max(x_values), max(y_values)
        width, height = max_x - min_x, max_y - min_y

        # Crop the image based on the bounding box
        cropped_img = img.crop((min_x, min_y, min_x + width, min_y + height))
        mask = Image.new('L', cropped_img.size, 0)
        draw = ImageDraw.Draw(mask)

        # Offset the points to match the cropped area
        # offset_points = [{'x': x - min_x, 'y': y - min_y} for x,y in zip(x_values,y_values)]
        # polygon_points = [(point['x'], point['y']) for point in offset_points]

        # offset_points = [{'x': x - min_x, 'y': y - min_y} for x,y in zip(x_values,y_values)]
        polygon_points = [(x- min_x, y- min_y) for x,y in zip(x_values,y_values)]

        # Create a polygon mask and apply it to extract the segmented area
        draw.polygon(polygon_points, outline=1, fill=1)
        # segmented_img = Image.new('RGBA', cropped_img.size, (0, 0, 0, 0))
        for x in range(cropped_img.width):
            for y in range(cropped_img.height):
                if mask.getpixel((x, y)):
                    current_pixel = cropped_img.getpixel((x, y))
                    pattern_pixel = pattern.getpixel((x, y))
                    img.putpixel((int(min_x)+x, int(min_y)+y), tuple(max(0, current_pixel[i] - detected_color[i] + pattern_pixel[i]) for i in range (3)))

    return img