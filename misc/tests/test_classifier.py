import cv2
from misc.functions import camera
from misc.functions import video
from misc.functions import process

cap = camera.camera_init()
classifier = cv2.CascadeClassifier("ball_classifier.xml")

while True:
    grabbed, frame = cap.read()
    if grabbed:
        frame = video.settings(frame)
        result, x, y, w, h = process.vision(frame, classifier)
        print(x, y, w, h)
        cv2.imshow("frame", result)
        cv2.waitKey(1)
