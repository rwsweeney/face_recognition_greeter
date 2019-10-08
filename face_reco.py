import face_recognition
import cv2
import os
import numpy as np
from functions import play_and_reco
from multiprocessing import Process

# Crawl through the images folder to identify faces and train the model
def train_model():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(base_dir, "images/")

    # Known face names counter
    kfnc = 0

    known_face_names = []
    known_face_encodings = []

    for (root, dirs, files) in os.walk(image_dir, topdown=True):
        
        # Creates a list of names to try to recognize based on directory name
        for dir in dirs:
            known_face_names.append(dir)

        # Pulls an image from the named directory, and encodes the face in the image.
        for file in files:
            if ".jpg" in file:
                image_path = os.path.join(image_dir, known_face_names[kfnc], file)
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(face_encoding)
                kfnc = kfnc + 1
                break

    return known_face_names, known_face_encodings

def start_video(ip, app_function=None):

    video_capture = cv2.VideoCapture(ip)

    known_face_names, known_face_encodings = train_model()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    #rachel_unseen = True
    #sarah_unseen = True
    unseen = True

    # Starts video loop to process each frame
    while True:
        ret, frame = video_capture.read()

        # Resize frame to 1/2 size for performance
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding
                )
                name = "Stranger danger"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                if app_function:
                    if app_function == "wikipedia":

                        # If it recognizes someone start a separate process on another core to greet them.
                        # How to keep while unseen: in face_reco portion of code?
                        while unseen:
                            p = Process(target=play_and_reco, args=(name,))
                            p.start()
                            unseen = False
                    
                    if app_function == "alarm":
                        # instantiate alarm class
                        pass

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results, and scale the image back
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw and label a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )

        # Display the resulting image
        cv2.imshow("Skynet 1.0", frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
