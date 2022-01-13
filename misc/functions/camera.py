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
def get_dimensions(cap, x_y):
    if x_y == "x":
        try:
            dim_x = cap.get(3)
        except Exception:
            dim_x = 0
        return dim_x
    if x_y == "y":
        try:
            dim_y = cap.get(4)
        except Exception:
            dim_y = 0
        return dim_y


# Takes action and defines the camera based on the OS type.
def os_action():
    path = r"misc/camera/fix_camera.py"

    while True:
        subprocess.run(["python", path], shell=False)
        break

    if platform.system() == "Linux":
        set_camera.hoop_exposure()
        time.sleep(0.5)
        cap = cv2.VideoCapture(camera_index)

    else:
        cap = cv2.VideoCapture(camera_index)
        time.sleep(1)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cap.set(15, int(config.get("camera", "WINDOWS_HOOP_EXPOSURE")))
    return cap


# Sets the auto exposure.
def set_auto_exposure(auto_exposure):
    cap = cv2.VideoCapture(camera_index)
    time.sleep(1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)

    return cap


# Switch camera modes.
def switch(mode):
    count = 0
    if mode == "ball" and count == 0:
        if platform.system() == "Linux":
            set_camera.ball_exposure()
            time.sleep(0.5)
            cap = cv2.VideoCapture(camera_index)

        else:
            cap = set_auto_exposure(0.75)
        count += 1

    elif mode == "hoop" and count == 1:
        if platform.system() == "Linux":
            set_camera.hoop_exposure()
            time.sleep(0.5)
            cap = cv2.VideoCapture(camera_index)

        else:
            cap = set_auto_exposure(0.25)
            cap.set(15, int(config.get("camera", "WINDOWS_HOOP_EXPOSURE")))
        count -= 1

    return cap


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
