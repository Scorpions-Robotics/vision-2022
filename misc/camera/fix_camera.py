import cv2
import time
import platform
import set_camera
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

camera_index = int(config.get("camera", "CAMERA_INDEX"))

if platform.system() == "Linux":
    set_camera.set_format()
    time.sleep(0.5)
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        time.sleep(0.5)
        cap.release()
        break


if platform.system() != "Linux":
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    while True:
        ret, frame = cap.read()
        time.sleep(0.5)
        cap.release()
        break
