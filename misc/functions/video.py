import cv2
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")


frame_width = int(config.get("camera", "FRAME_WIDTH"))
frame_height = int(config.get("camera", "FRAME_HEIGHT"))

# Calculates the distance between the crosshair and the hoop's center.
def rotation(x_defined, x, w):
    try:
        x_c = x + (w / 2)
        return x_c - (x_defined / 2)
    except Exception:
        return None


# Calculates the focal length.
def focal_length(kpw, kd, kw):
    return (kpw * kd) / kw


# Calculates the distance between camera and the hoop.
def current_distance(kpw, kd, kw, w):
    try:
        return (kw * focal_length(kpw, kd, kw)) / w
    except Exception:
        pass


# Checks if the hoop is in the frame.
def is_detected(key):
    return key is not None


# Takes a frame and returns the frame with the crosshair drawn on it.
def crosshair(frame):
    color = (0, 255, 0)
    fpt1 = ((frame_width / 2) - 20), (frame_height // 2)

    fpt2 = ((frame_width / 2) + 20), (frame_height // 2)

    spt1 = (frame_width // 2), ((frame_height / 2) - 20)

    spt2 = (frame_width // 2), ((frame_height / 2) + 20)

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
