from configparser import ConfigParser
import cv2
import sys
from pathlib import Path


sys.path.append(str(Path("..").absolute().parent))
from misc.functions import process

config = ConfigParser()
config.read("settings.ini")

for item, item_result in config.items("colors"):
    print(item, tuple(map(int, item_result.split("\n"))))

cap = cv2.VideoCapture(0)

while True:
    grabbed, frame = cap.read()

    result = process.mask_color(frame, (160, 165, 0), (179, 255, 255))

    cv2.imshow("frame", result)
    cv2.waitKey(1)
