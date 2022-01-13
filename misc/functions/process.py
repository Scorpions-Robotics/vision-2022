import cv2
import numpy as np


# Processes the frame, detects the cascade classifier and returns the frame with squares drawn on the detected object.
def hoop_vision(frame, cascade_classifier):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hoops = cascade_classifier.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in hoops:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if not len(hoops):
        x, y, w, h = "none", "none", "none", "none"

    return frame, x, y, w, h


# Processes the frame, detects the cascade classifier and returns the frame with squares drawn on the detected object.
def ballz_vision(frame, cascade_classifier):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hoops = cascade_classifier.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
    )

    for (x, y, w, h) in hoops:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if not len(hoops):
        x, y, w, h = "none", "none", "none", "none"

    return frame, x, y, w, h


# Processes the frame, detects the cascade classifier and returns the frame with squares drawn on the detected object.
def bumper_vision(frame, cascade_classifier):
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
