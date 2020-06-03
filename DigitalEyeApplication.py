from DigitalEyeServerThread import ServerThread
from DigitalEyeUIThread import UIThread
from DigitalEyeDetectBlink import process_image_for_blink_detection, get_blink_count
import cv2


def start_application():
    server_thread = ServerThread()
    ui_thread = UIThread()

    server_thread.start()
    ui_thread.start()
    path = r'F:\red_eyes\red_eye_1.jpg'
    image = cv2.imread(path)
    #cv2.imshow('image', image)
    blink_count = process_image_for_blink_detection(image)
    print(blink_count)


if __name__ == '__main__':
    start_application()
