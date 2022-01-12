import platform
import time
import subprocess
import cv2
import numpy as np
from configparser import ConfigParser
from misc.camera import set_camera

config = ConfigParser()
config.read("settings.ini")

camera_index = int(config.get("camera", "CAMERA_INDEX"))


# Gets the dimensions of the camera.
def get_dimensions(camera, x_y):
    if x_y == "x":
        try:
            dim_x = camera.get(3)
        except Exception:
            dim_x = 0
        return dim_x
    if x_y == "y":
        try:
            dim_y = camera.get(4)
        except Exception:
            dim_y = 0
        return dim_y


# Takes action and defines the camera based on the OS type.
def os_action():
    if platform.system() == "Linux":
        while True:
            subprocess.run(["python", "misc/camera/fix_camera.py"], shell=False)
            break
        set_camera.set_exposure()
        time.sleep(0.5)
        camera = cv2.VideoCapture(camera_index)

    else:
        while True:
            subprocess.call(["python", "misc/camera/fix_camera.py"], shell=False)
            break
        camera = cv2.VideoCapture(camera_index)
        time.sleep(1)
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        camera.set(15, int(config.get("camera", "WINDOWS_HOOP_EXPOSURE")))
    return camera


# Takes a frame and returns the frame white balanced.
def white_balance(frame):
    result = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - (
        (avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1
    )
    result[:, :, 2] = result[:, :, 2] - (
        (avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1
    )
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result
