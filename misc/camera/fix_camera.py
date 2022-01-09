import cv2
import time
from decouple import config
import platform
import set_camera


if platform.system() == "Linux":
    set_camera.set_format()
    time.sleep(0.5)
    cap = cv2.VideoCapture(int(config("CAMERA_INDEX")))
    while True:
        ret, frame = cap.read()
        time.sleep(0.5)
        cap.release()
        break


if platform.system() != "Linux":
    cap = cv2.VideoCapture(int(config("CAMERA_INDEX")))
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    while True:
        ret, frame = cap.read()
        time.sleep(0.5)
        cap.release()
        break
