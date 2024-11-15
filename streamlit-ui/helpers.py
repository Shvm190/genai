import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.metrics import structural_similarity
import matplotlib.image as mpimg

# Define the Barclays color scheme
colours = {
    "barclays_blue": "#14375A",
    "barclays_medium_blue": "#204D76",
    "barclays_light_blue": "#00AEEF",
    "barclays_white": "#FFFFFF",
    "barclays_grey": "#A0A0A0",
}

def create_geolocation_map(coordinates):
    coordinates = sorted(coordinates, key=lambda x: x[0])
    datetimes, coordinates = [x[0] for x in coordinates], [[x[1], x[2]] for x in coordinates]
    # Calculate the center of the map for better visualization
    map_center = [sum(x) / len(x) for x in zip(*coordinates)]
    # Create a folium map centered around the calculated center
    m = folium.Map(location=map_center, zoom_start=2)
    # Add heatmap to the map
    # HeatMap(coordinates).add_to(m)
    # Add markers for each unique location
    for datetime, coordinate in zip(datetimes, coordinates):
        folium.Marker(location=coordinate, popup=datetime).add_to(m)

    danger_line = folium.PolyLine(
        coordinates,
        weight=10,
        color="orange",
        opacity=0.8
    ).add_to(m)

    attr = {"fill": "red"}

    folium.plugins.PolyLineTextPath(
        danger_line, "\u25BA", repeat=True, offset=6, attributes=attr
    ).add_to(m)

    # Save the map to an HTML file
    # m.save("heatmap.html")
    # Display the map in the app
    folium_static(m, width=1000, height=500)


def compare_faces(image_path_1, image_path_2, threshold=0.6):
    """
    Compare two images to determine if they represent the same person.

    Args:
    - image_path_1 (str): Path to the first image file (PNG or JPG).
    - image_path_2 (str): Path to the second image file (PNG or JPG).
    - threshold (float): Threshold for similarity score to determine if the faces are the same person. Default is 0.6.

    Returns:
    - result (str): A statement indicating whether the two images represent the same person.
    """

    ## Load the images

    img1 = Image.open(image_path_1).convert('L')
    img2 = Image.open(image_path_2).convert('L')

    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    img_matrix_1 = np.array(img1)
    img_matrix_2 = np.array(img2)

    ssim_index, _ = structural_similarity(img_matrix_1, img_matrix_2, full=True)

    # Determine if the faces are similar enough based on the threshold
    if ssim_index <= threshold:
        #return f"The similarity score between the two images is {ssim_index:.2f}. Based on the threshold of {threshold}, the two images are similar enough to indicate they represent the same person."
        return round(ssim_index, 2), "different"
    else:
        #return f"The similarity score between the two images is {ssim_index:.2f}. Based on the threshold of {threshold}, the two images are not similar enough to indicate they represent the same person."
        return round(ssim_index, 2), "same"