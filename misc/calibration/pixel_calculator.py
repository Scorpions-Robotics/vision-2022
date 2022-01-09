import cv2
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import functions


x = 0
y = 0
w = 0
h = 0

count = 0

cascade_classifier = cv2.CascadeClassifier("cascade.xml")

frame = cv2.imread("images/ref-pic.jpeg")

h_f, w_f, c_f = frame.shape

h_f = int(h_f - (h_f / 8))
w_f = int(w_f / 8)

font = cv2.FONT_HERSHEY_SIMPLEX
location = (w_f, h_f)
fontScale = 1
fontColor = (255, 255, 255)
thickness = 2
lineType = 2

while True:
    try:

        result, x, y, w, h = functions.vision(frame, cascade_classifier)

        if count == 0:
            print(f"X: {x} Y: {y} W: {w} H: {h}")
            count += 1

        cv2.imshow("img", result)
        if cv2.waitKey(1) & 0xFF == ord("y"):

            cv2.putText(
                frame,
                f"X: {x} Y: {y} W: {w} H: {h}",
                location,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType,
            )
            cv2.imwrite("images/ref-pic-post.jpeg", result)
            print("Processed image is written under images folder.")
            break

    except KeyboardInterrupt:
        break

cv2.destroyAllWindows()
