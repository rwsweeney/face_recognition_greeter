import face_recognition
import cv2
import os
import numpy as np
from functions import play_and_reco
from multiprocessing import Process


# Crawl through the images folder to identify faces and train the model
def train_model():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    dir_image = os.path.join(base_dir, "images/")

    kfnc = 0
    known_face_names = []
    known_face_encodings = []

    for (root,dirs,files) in os.walk(dir_image, topdown=True):
        for dir in dirs:
            known_face_names.append(dir)

        for file in files:
            if '.jpg' in file:
                image_path = os.path.join(dir_image, known_face_names[kfnc], file)
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(face_encoding)
                kfnc = kfnc + 1
                break

    return known_face_names, known_face_encodings

def start_video(ip):

    video_capture = cv2.VideoCapture(ip)

    known_face_names, known_face_encodings = train_model()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    unseen = True

    # Starts video loop
    while True:
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
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
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    # If it recognizes someone2 or I
                    while unseen:
                        p = Process(target=play_and_reco, args=(name,))
                        p.start()
                        unseen = False

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
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

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
