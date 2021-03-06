import cv2
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import process
from misc.functions import video
from misc.functions import camera

cap = cv2.VideoCapture(input("Enter video path: "))
classifier = cv2.CascadeClassifier(input("Enter classifier path: "))
mask = input("Do you want to mask colors? (y/n): ")


if mask in ["y", "Y", "yes", "Yes", "YES"]:
    mask = True

if mask is True:
    lower = tuple(
        map(
            int,
            input("Enter lower HSV bound seperated by commas (e.g. 0,0,0): ").split(
                ","
            ),
        )
    )
    upper = tuple(
        map(
            int,
            input(
                "Enter upper HSV bound seperated by commas (e.g. 179,255,255): "
            ).split(","),
        )
    )


while True:
    grabbed, frame = cap.read()
    if grabbed:
        frame = video.settings(frame)
        if mask is True:
            frame = process.mask_color(frame, lower, upper)
        result, x, y, w, h = process.vision(frame, classifier)
        print(x, y, w, h)
        cv2.imshow("result", result)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera.stop(cv2, cap)
