import cv2
import numpy as np
import platform
from decouple import config
import time
import subprocess
import requests
import sys, os
from datetime import datetime
from pathlib import Path
from networktables import NetworkTables

sys.path.append(str(Path("..").absolute().parent))
from misc.camera import set_camera


# Checks if log files exist. If not, creates them.
def systemctl_log():
    if not os.path.isdir(f'{config("WORKING_DIR")}/log/'):
        os.mkdir(f'{config("WORKING_DIR")}/log/')

    if not os.path.isfile(f'{config("WORKING_DIR")}/log/stdout.log'):
        with open(f'{config("WORKING_DIR")}/log/stdout.log', "w") as f:
            f.write(f"Created: {datetime.utcnow()}\n")

    if not os.path.isfile(f'{config("WORKING_DIR")}/log/stderr.log'):
        with open(f'{config("WORKING_DIR")}/log/stderr.log', "w") as f:
            f.write(f"Created: {datetime.utcnow()}\n")


# Checks internet connection.
def is_connected():
    try:
        request = requests.get("http://google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


# Takes action and defines the camera based on the OS type.
def os_action():
    if platform.system() == "Linux":
        while True:
            subprocess.run(["python", "misc/camera/fix_camera.py"], shell=False)
            break
        set_camera.set_exposure()
        time.sleep(0.5)
        camera = cv2.VideoCapture(int(config("CAMERA_INDEX")))

    else:
        while True:
            subprocess.call(["python", "misc/camera/fix_camera.py"], shell=False)
            break
        camera = cv2.VideoCapture(int(config("CAMERA_INDEX")))
        time.sleep(1)
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        camera.set(15, int(config("WINDOWS_EXPOSURE")))
    return camera


# Initialize NetworkTables.
def nt_init():
    if int(config("NETWORKTABLES_TEST_MODE")):
        NetworkTables.initialize()
    else:
        NetworkTables.initialize(server=config("NETWORKTABLES_SERVER"))
    return NetworkTables.getTable(config("NETWORKTABLES_TABLE"))


# Initialize NetworkTables listener.
def nt_listener_init():
    NetworkTables.initialize(server=config("NETWORKTABLES_SERVER"))
    return NetworkTables.getTable(config("NETWORKTABLES_TABLE"))


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


# Calculates the distance between the crosshair and the hoop's center.
def calculate_rotation(x_defined, x, w):
    try:
        x_c = x + (w / 2)
        return x_c - (x_defined / 2)
    except Exception:
        return None


# Calculates the focal length.
def calibrate(kpw, kd, kw):
    return (kpw * kd) / kw


# Calculates the distance between camera and the hoop.
def current_distance(kpw, kd, kw, w):
    try:
        return (kw * calibrate(kpw, kd, kw)) / w
    except Exception:
        pass


# Takes a frame and returns the frame with the crosshair drawn on it.
def crosshair(frame):
    color = (0, 255, 0)
    fpt1 = (int(((int(config("FRAME_WIDTH"))) / 2) - 20)), int(
        config("FRAME_HEIGHT")
    ) // 2

    fpt2 = (int(((int(config("FRAME_WIDTH"))) / 2) + 20)), int(
        config("FRAME_HEIGHT")
    ) // 2

    spt1 = int(config("FRAME_WIDTH")) // 2, (
        int(((int(config("FRAME_HEIGHT"))) / 2) - 20)
    )

    spt2 = int(config("FRAME_WIDTH")) // 2, (
        int(((int(config("FRAME_HEIGHT"))) / 2) + 20)
    )

    crosshair = cv2.line(
        frame,
        fpt1,
        fpt2,
        color,
        2,
    )

    crosshair = cv2.line(
        crosshair,
        spt1,
        spt2,
        color,
        2,
    )
    return crosshair


# Checks if the hoop is in the frame.
def is_detected(key):
    return key is not None


# Processes the frame, detects the cascade classifier and returns the frame with squares drawn on the detected object.
def vision(frame, cascade_classifier):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hoops = cascade_classifier.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in hoops:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if not len(hoops):
        x, y, w, h = "none", "none", "none", "none"

    return frame, x, y, w, h


# Masks colors.
def mask_color(frame, lower, upper):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_range = np.array([lower])
    upper_range = np.array([upper])

    mask = cv2.inRange(hsv_frame, lower_range, upper_range)

    imask = mask > 0
    color = np.zeros_like(frame, np.uint8)
    color[imask] = frame[imask]

    return color


# Run Flask
def run_flask():
    if int(config("STREAM_FRAME")):
        return subprocess.Popen(["python", "misc/flask/flask_server.py"], shell=False)
