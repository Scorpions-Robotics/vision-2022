import cv2
import sys
import imutils
import math
from pathlib import Path
from configparser import ConfigParser

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import camera


config = ConfigParser()
config.read("settings.ini")


frame_width = config.getint("camera", "FRAME_WIDTH")
frame_height = config.getint("camera", "FRAME_HEIGHT")

vertical_fov = config.getfloat("camera", "VERTICAL_FOV")
camera_mount_angle_hoop = config.getfloat("camera", "MOUNT_ANGLE_HOOP")
camera_mount_angle_ball = config.getfloat("camera", "MOUNT_ANGLE_BALL")


# Calculates the distance between the crosshair and the hoop's center.
def rotation(dimension, x_y, w_h) -> float or None:
    try:
        dimension_c = x_y + (w_h / 2)
        return dimension_c - (dimension / 2)
    except Exception:
        return None


# Calculates the distance between the camera and the hoop.
# http://docs.limelightvision.io/en/latest/cs_estimating_distance.html
def distance(target_center_y, mode):
    try:
        if mode == "hoop":
            mount_angle = camera_mount_angle_hoop
            height_diff = config.getint("calibration", "HOOP_HEIGHT") - config.getint(
                "camera", "CAMERA_MOUNT_HEIGHT"
            )

        else:
            mount_angle = camera_mount_angle_ball
            height_diff = config.getint("calibration", "BALL_HEIGHT") - config.getint(
                "camera", "CAMERA_MOUNT_HEIGHT"
            )

        pixel_per_angle = float(frame_height / vertical_fov)
        middle_of_camera = frame_height / 2.0

        pixel_diff = middle_of_camera - target_center_y
        angle_diff = float(pixel_diff / pixel_per_angle)

        a2 = math.radians(angle_diff)
        a1 = math.radians(mount_angle)

        if a1 + a2 == 0:
            return 0

        return abs(height_diff / math.tan(abs(a1 + a2)))

    except Exception:
        return None


# Checks if the hoop is in the frame.
def is_detected(key) -> bool:
    return key is not None


# Safely rounds input to wanted decimal places.
def safe_round(key, point: int = 2) -> float:
    try:
        return round(key, point)
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
