from scipy.spatial import distance as dist
from imutils import face_utils
import dlib
import cv2
from DigitalEyeDetectEye import detect_eye

# initialize the frame counters and the total number of blinks
TOTAL = 0
COUNTER = 0


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear


# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSTANT_FRAMES = 3
CLOSENESS_THRESH = 200

EYE_DETECT_COUNTER = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat_2")

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def process_image_for_blink_detection(image):
    global COUNTER
    global TOTAL
    global CLOSENESS_THRESH
    global EYE_DETECT_COUNTER
    greyImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceBounds = detector(greyImage, 0)
    eye_bounds = detect_eye(greyImage)
    face_detected = False
    for faceBound in faceBounds:
        CLOSENESS_THRESH = 0;
        face_detected = True
        faceLandmarks = predictor(greyImage, faceBound)
        faceLandmarks = face_utils.shape_to_np(faceLandmarks)
        leftEye = faceLandmarks[lStart:lEnd]
        rightEye = faceLandmarks[rStart:rEnd]
        leftEar = eye_aspect_ratio(leftEye)
        rightEar = eye_aspect_ratio(rightEye)
        averageEar = (leftEar + rightEar) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)
        if averageEar < EYE_AR_THRESH:
            COUNTER += 1
            # otherwise, the eye aspect ratio is not below the blink
            # threshold
        else:
            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            if COUNTER >= EYE_AR_CONSTANT_FRAMES:
                TOTAL += 1

            # reset the eye frame counter
            COUNTER = 0
            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
    print("Blinks: {}".format(TOTAL))
    if not face_detected:
        if len(eye_bounds) > 0:
            if EYE_DETECT_COUNTER >= CLOSENESS_THRESH :
                return "Eye is too close"
            else:
                EYE_DETECT_COUNTER += 1
    return TOTAL


def get_blink_count():
    global TOTAL
    return TOTAL
