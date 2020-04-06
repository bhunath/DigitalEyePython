from imutils import face_utils
import numpy as np
import dlib
import cv2
from DigitalEyeDetectEye import detect_eye


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat_2")


def check_face_is_close(image):
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_bounds = detector(grey_image, 1)
    eye_bound = detect_eye(grey_image)
    face_detected = False
    for faceBound in face_bounds:
        face_detected = True
        break

    if face_detected == False and len(eye_bound) > 0:
        return True
    else:
        return False