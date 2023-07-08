
import cv2 as cv
from flask import Flask, Response

import datetime
from utils import *

app = Flask(__name__)


@app.route('/')
def stream():
    employees = [ "elon.jpg", "maria.jpg", "mark.jpg", "tate.jpg"]
    model = get_model()
    original_embeddings = []
    detected_employees = []
    for employee in employees:
        embedding = get_original_embedding(model,employee)
        original_embeddings.append(embedding)
    vid = cv.VideoCapture(0)

    def generate():
        while(True):
            
            # Capture the video frame
            # by frame
            ret, frame = vid.read()
            cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # extract faces from image using mediapipe
            face_image, draw_image, (xmin,ymin) = get_main_face(frame)
            if (face_image == "no face detected"):
                continue
            # resizing the image to (224, 224, 3) to match to model input
            face_image = cv.resize(face_image, (224,224))
            # use some pre_processing before presenting to model 
            processed_image = process_image(face_image)
            #extracting embeddings from faces with vgg model
            embedding2 = get_face_embedding(processed_image, model)
            distances = []
            # calculating the distance between the face embeddings and all employees to see if there's a match
            for idx in range(len(original_embeddings)):
                distance = calculate_distance_between_embeddings(original_embeddings[idx], embedding2)
                distances.append(distance)
            min_distance = np.min(distances)
            min_distance_index = distances.index(min_distance)
            if (min_distance > 0.6):
                text = "not allowed : unknown person"
            else:
                text = "allowed : " + employees[min_distance_index].split(".")[0] + str(min_distance)
            
            detected_employees.append(employees[min_distance_index].split(".")[0])
            cv.putText(draw_image, text, (xmin,ymin), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            cv.imshow('MediaPipe Face Detection', draw_image)
            yield text +"\n"
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    
    return Response(generate())

# After the loop release the cap object

# Destroy all the windows
cv.destroyAllWindows()

if __name__ == '__main__':
    app.run( debug=True)