import matplotlib.pyplot as plt
import cv2
import numpy as np
import pandas as pd

from keras.preprocessing import image


# def load_image(image_path, grayscale=False, target_size=None):
#     pil_image = image.load_img(image_path, grayscale, target_size)
#     return image.img_to_array(pil_image)
def load_image(image_path, grayscale=False, target_size=None):
    color_mode = 'grayscale'
    if not grayscale:
        color_mode = 'rgb'
    else:
        grayscale = False
    pil_image = image.load_img(image_path, grayscale, color_mode, target_size)
    return image.img_to_array(pil_image)


def detect_faces(detection_model, gray_image_array):
    return detection_model.detectMultiScale(gray_image_array, 1.3, 5)


def draw_bounding_box(face_coordinates, image_array, color):
    x, y, w, h = face_coordinates
    cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)


def get_coordinates(face_coordinates):
    x, y, width, height = face_coordinates
    return x, x + width, y, y + height


def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0, font_scale=2, thickness=2):
    x, y = coordinates[:2]
    cv2.putText(image_array, text, (x + x_offset, y + y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, color, thickness, cv2.LINE_AA)


def load_data(data_file):
    """ loads fer2013.csv dataset
    # Arguments: data_file fer2013.csv
    # Returns: faces and emotions
            faces: shape (35887,48,48,1)
            emotions: are one-hot-encoded
    """
    data = pd.read_csv(data_file)
    pixels = data['pixels'].tolist()
    width, height = 48, 48
    faces = []
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.asarray(face).reshape(width, height)
        faces.append(face)
    faces = np.asarray(faces)
    print(faces.shape)
    # faces = preprocess_input(faces)
    faces = np.expand_dims(faces, -1)
    df = pd.get_dummies(data['emotion'])
    emotions = df.as_matrix()
    return faces, emotions


def preprocess_input(images):
    """ preprocess input by substracting the train mean
    # Arguments: images or image of any shape
    # Returns: images or image with substracted train mean (129)
    """
    images = images / 255.0
    return images
