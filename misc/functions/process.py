import cv2
import numpy as np
import operator
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")


# Processes the frame, detects the cascade classifier and
# returns the biggest detected object's coordinates.
def vision(frame, cascade_classifier) -> tuple:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    objects = cascade_classifier.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=config.getint("cascade", "MIN_NEIGHBORS"),
        minSize=tuple(map(int, config.get("cascade", "MIN_SIZE").split("\n"))),
    )

    detected = []

    try:
        detected.extend((x, y, w, h) for x, y, w, h in objects)
        wh = {index: object[2] * object[3] for index, object in enumerate(detected)}
        sorted_wh = sorted(wh.items(), key=operator.itemgetter(1))
        x, y, w, h = detected[sorted_wh[-1][0]]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    except Exception:
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
