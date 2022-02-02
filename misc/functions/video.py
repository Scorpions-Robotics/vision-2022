import cv2
import sys
import imutils
from pathlib import Path
from configparser import ConfigParser

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import camera


config = ConfigParser()
config.read("settings.ini")


frame_width = config.getint("camera", "FRAME_WIDTH")
frame_height = config.getint("camera", "FRAME_HEIGHT")


# Calculates the distance between the crosshair and the hoop's center.
def rotation(x_defined, x, w) -> float or None:
    try:
        x_c = x + (w / 2)
        return x_c - (x_defined / 2)
    except Exception:
        return None


# Calculates the focal length.
def focal_length(kpw, kd, kw) -> float:
    return (kpw * kd) / kw


# Calculates the distance between camera and the hoop.
def current_distance(kpw, kd, kw, w) -> float:
    try:
        return (kw * focal_length(kpw, kd, kw)) / w
    except Exception:
        pass


# Checks if the hoop is in the frame.
def is_detected(key) -> bool:
    return key is not None


# Safely rounds input to 2 decimal places.
def safe_round(key) -> float:
    try:
        return round(key, 2)
    except Exception:
        return key


# Video settings.
def settings(frame, resolution_rate: int or float = 1):

    frame = imutils.resize(
        frame,
        width=config.getint("camera", "FRAME_WIDTH") * resolution_rate,
        height=config.getint("camera", "FRAME_HEIGHT") * resolution_rate,
    )

    if config.getint("fancy", "FLIP_FRAME"):
        frame = cv2.flip(frame, 1)

    frame = imutils.rotate(frame, config.getint("fancy", "FRAME_ANGLE"))

    if config.getint("fancy", "WHITE_BALANCE"):
        frame = camera.white_balance(frame)

    return frame


# Takes a frame and returns the frame with the crosshair drawn on it.
def crosshair(frame):
    color = (0, 255, 0)

    fpt1 = frame_width // 2 - 20, frame_height // 2
    fpt2 = frame_width // 2 + 20, frame_height // 2
    spt1 = frame_width // 2, frame_height // 2 - 20
    spt2 = frame_width // 2, frame_height // 2 + 20

    processed_crosshair = cv2.line(
        frame,
        fpt1,
        fpt2,
        color,
        2,
    )

    processed_crosshair = cv2.line(
        processed_crosshair,
        spt1,
        spt2,
        color,
        2,
    )
    return processed_crosshair
