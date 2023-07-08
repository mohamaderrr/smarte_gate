# Import necessary libraries
import numpy as np
import tensorflow
from tensorflow import keras
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Sequential
from keras.layers import Input, Flatten, Dense
from scipy.spatial.distance import cosine
import mediapipe as mp
import cv2 as cv


# function to get the model used to have embeddings of face images
def get_model():
    #input shape of the model
    input_shape = (224, 224, 3) 
    # Create the base model using VGG16
    vgg_model = VGG16(include_top=False, input_shape=input_shape)
    model = Sequential()
    model.add(vgg_model)
    model.add(Flatten())
    model.add(Dense(50))
    # set the model weight to be untrainable
    for layer in model.layers:
        layer.trainable = False
    
    return model


def process_image(face_image):
    # the image will come from opencv and mediapipe video stream
    face_image = preprocess_input(face_image)
    return np.array([face_image])

# fct that returns a crop from original image containing face
def get_main_face(image):
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    draw_image = image
    # get faces from mediapipe model
    with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(image)
        if results.detections:
            for detection in results.detections:
                xmin = int(detection.location_data.relative_bounding_box.xmin * image.shape[1])
                ymin = int(detection.location_data.relative_bounding_box.ymin * image.shape[0])
                width = int(detection.location_data.relative_bounding_box.width  * image.shape[1])
                height = int(detection.location_data.relative_bounding_box.height  * image.shape[0])
                mp_drawing.draw_detection(draw_image, detection)

        else:
            return "no face detected", draw_image, (0.0 , 0.0)
    image = np.array(image)
    face_image = image[ymin:ymin+height , xmin:xmin+width]
    return face_image, draw_image ,(xmin,ymin)

# get embedding of the face
def get_face_embedding(face_image, model):
    embeddings = model.predict(face_image)
    return embeddings

# get the distance between two embeddings to check for similarity
def calculate_distance_between_embeddings(embedding1, embedding2):
    distance = cosine(embedding1[0], embedding2[0])
    return distance

# fct used to get original embeddings of all employees
def get_original_embedding(model, image_filename):
    image = cv.imread(filename=image_filename)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    face_image, draw_image, (xmin,ymin) = get_main_face(image)
    face_image = cv.resize(face_image, (224,224))
    processed_image = process_image(face_image)
    embedding = get_face_embedding(processed_image, model)
    return embedding


