import cv2
import numpy as np
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")


# Processes the frame, detects the cascade classifier and
# returns the frame with squares drawn on the detected object.
def vision(frame, cascade_classifier) -> tuple:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    objects = cascade_classifier.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=config.getint("cascade", "MIN_NEIGHBORS"),
        minSize=tuple(map(int, config.get("cascade", "MIN_SIZE").split("\n"))),
    )

    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if not objects:
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
