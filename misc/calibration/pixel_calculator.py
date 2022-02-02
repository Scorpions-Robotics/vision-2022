import cv2
import sys
from glob import glob
from configparser import ConfigParser
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import process
from misc.functions import network


hoop_hsv_upper, hoop_hsv_lower = network.set_hoop_hsv()
red_ball_hsv_upper, red_ball_hsv_lower = network.set_alliance_hsv_upper(
    "red"
), network.set_alliance_hsv_lower("red")
blue_ball_hsv_upper, blue_ball_hsv_lower = network.set_alliance_hsv_upper(
    "blue"
), network.set_alliance_hsv_lower("blue")

config = ConfigParser()
config.read("settings.ini")


def func_replace(path):
    return path.replace("\\", "/")


hoop_images = list(map(func_replace, glob("images/raw/hoop/hoop-ref-pic-raw-*.jpeg")))
blue_ball_images = list(
    map(func_replace, glob("images/raw/b_ball/blue_ball-ref-pic-raw-*.jpeg"))
)
red_ball_images = list(
    map(func_replace, glob("images/raw/r_ball/red_ball-ref-pic-raw-*.jpeg"))
)

frame_width = config.getint("camera", "FRAME_WIDTH")
frame_height = config.getint("camera", "FRAME_HEIGHT")

h_f = int(frame_height - (frame_height / 8))
w_f = int(frame_width / 8)

font = cv2.FONT_HERSHEY_SIMPLEX
location = (w_f, h_f)
fontScale = 0.5
fontColor = (0, 0, 255)
thickness = 2
lineType = 2

hoop_classifier = cv2.CascadeClassifier("hoop_classifier.xml")
ball_classifier = cv2.CascadeClassifier("ball_classifier.xml")

for index, image in enumerate(hoop_images):
    result, x, y, w, h = process.vision(cv2.imread(image), hoop_classifier)

    cv2.putText(
        result,
        f"X: {x} Y: {y} W: {w} H: {h}",
        location,
        font,
        fontScale,
        fontColor,
        thickness,
        lineType,
    )

    print(image, f"X: {x} Y: {y} W: {w} H: {h}")
    cv2.imwrite(f"images/processed/hoop/hoop-ref-pic-processed-{index}.jpeg", result)

print("Processed hoop images are written under images/processed/hoop/ folder.")


for index, image in enumerate(blue_ball_images):
    result, x, y, w, h = process.vision(cv2.imread(image), ball_classifier)

    cv2.putText(
        result,
        f"X: {x} Y: {y} W: {w} H: {h}",
        location,
        font,
        fontScale,
        fontColor,
        thickness,
        lineType,
    )

    print(image, f"X: {x} Y: {y} W: {w} H: {h}")
    cv2.imwrite(
        f"images/processed/b_ball/blue_ball-ref-pic-processed-{index}.jpeg", result
    )

print("Processed blue ball images are written under images/processed/b_ball/ folder.")


for index, image in enumerate(red_ball_images):
    result, x, y, w, h = process.vision(cv2.imread(image), ball_classifier)

    cv2.putText(
        result,
        f"X: {x} Y: {y} W: {w} H: {h}",
        location,
        font,
        fontScale,
        fontColor,
        thickness,
        lineType,
    )

    print(image, f"X: {x} Y: {y} W: {w} H: {h}")
    cv2.imwrite(
        f"images/processed/r_ball/red_ball-ref-pic-processed-{index}.jpeg", result
    )

print("Processed red ball images are written under images/processed/r_ball/ folder.")
