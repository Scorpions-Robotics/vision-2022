import cv2
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import process
from misc.functions import video
from misc.functions import camera


mode = input("Enter mode: ")
test_type = input("Enter test type (camera or image): ")
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


if test_type == "camera":
    cap = camera.camera_init()
    while True:
        grabbed, frame = cap.read()
        camera.switch(cap, mode)
        if grabbed:
            frame = video.settings(frame)
            if mask is True:
                frame = process.mask_color(frame, lower, upper)
            result, x, y, w, h = process.vision(frame, classifier)
            print(x, y, w, h)
            cv2.imshow("result", result)
            cv2.waitKey(1)

elif test_type == "image":
    image = cv2.imread(input("Enter image path: "))
    frame = video.settings(image)
    if mask is True:
        frame = process.mask_color(frame, lower, upper)
    result, x, y, w, h = process.vision(frame, classifier)
    print(x, y, w, h)
    cv2.imshow("result", result)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
