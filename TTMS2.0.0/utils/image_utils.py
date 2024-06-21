import cv2
import numpy as np
from PIL import Image

def process_image_for_edges(file_path):
    image = cv2.imread(file_path, 0)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(image, 100, 200)
    return edges

def filter_contours(image, min_contour_area):
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_image = np.zeros_like(image)
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            cv2.drawContours(filtered_image, [contour], -1, 255, thickness=cv2.FILLED)
    return filtered_image

def preprocess_image(image_path, target_size=(224, 224)):
    img = cv2.imread(image_path)
    img = cv2.resize(img, target_size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def save_processed_image(image, file_path):
    processed_pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB))
    processed_pil_img.save(file_path)
    return processed_pil_img
