from misc.functions import process
from misc.functions import video
from misc.functions import network
from misc.functions import camera
import cv2
import sys
import time
from pynput import keyboard
from glob import glob
from pathlib import Path
from configparser import ConfigParser

sys.path.append(str(Path("..").absolute().parent))


hoop_hsv_upper, hoop_hsv_lower = network.set_hoop_hsv()
red_ball_hsv_upper, red_ball_hsv_lower = network.set_alliance_hsv_upper(
    "red"
), network.set_alliance_hsv_lower("red")
blue_ball_hsv_upper, blue_ball_hsv_lower = network.set_alliance_hsv_upper(
    "blue"
), network.set_alliance_hsv_lower("blue")

config = ConfigParser()
config.read("settings.ini")

table = network.nt_init()
cap = camera.camera_init()


def func_replace(x):
    return x.replace("\\", "/")


hoop_images = (
    len(list(map(func_replace, glob("images/raw/hoop-ref-pic-raw-*.jpeg")))) + 1
)
blue_ball_images = (
    len(list(map(func_replace, glob("images/raw/blue_ball-ref-pic-raw-*.jpeg")))) + 1
)
red_ball_images = (
    len(list(map(func_replace, glob("images/raw/red_ball-ref-pic-raw-*.jpeg")))) + 1
)

number = 0
h = 0
b = 0
r = 0
mode = "hoop"
alliance = "blue"


# Can't remove this for now :(
def on_press(key):  # sourcery skip: extract-duplicate-method
    global alliance
    global number
    global cap
    global mode
    global h, b, r
    if key == keyboard.Key.space:
        if number == 0:
            cap = camera.switch(cap, "hoop")
            mode = "hoop"
            print("Mode switched to hoop mode.")
            number += 1
        elif number == 1:
            cap = camera.switch(cap, "ball")
            mode = "ball"
            print("Mode switched to ball mode.")
            number -= 1

    elif key == keyboard.Key.left:
        alliance = "blue"
        print("Blue alliance")

    elif key == keyboard.Key.right:
        alliance = "red"
        print("Red alliance")

    elif key == keyboard.Key.ctrl_l:
        h = 1
        time.sleep(0.033)
        h = 0
    elif key == keyboard.Key.shift_l:
        b = 1
        time.sleep(0.033)
        b = 0
    elif key == keyboard.Key.alt_l:
        r = 1
        time.sleep(0.033)
        r = 0


listener = keyboard.Listener(on_press=on_press)
listener.start()


while True:
    try:

        grabbed, frame = cap.read()

        if grabbed:

            frame = camera.resolution_init(frame)

            if mode == "ball":
                frame = video.settings(frame)
                if alliance == "blue":
                    hsv_mask = process.mask_color(
                        frame, (blue_ball_hsv_lower), (blue_ball_hsv_upper)
                    )
                elif alliance == "red":
                    hsv_mask = process.mask_color(
                        frame, (red_ball_hsv_lower), (red_ball_hsv_upper)
                    )

            elif mode == "hoop":
                frame = video.settings(frame)
                hsv_mask = process.mask_color(frame, (hoop_hsv_lower), (hoop_hsv_upper))

            cv2.imshow("img", hsv_mask)

            if h:
                cv2.imwrite(
                    f"images/raw/hoop/hoop-ref-pic-raw-{hoop_images}.jpeg",
                    frame,
                )
                print("Taken hoop image is written under images/raw/hoop/ folder.")
                hoop_images += 1

            if b:
                cv2.imwrite(
                    f"images/raw/b_ball/blue_ball-ref-pic-raw-{blue_ball_images}.jpeg",
                    frame,
                )
                print(
                    "Taken blue_ball image is written under images/raw/b_ball/ folder."
                )
                blue_ball_images += 1

            if b:
                cv2.imwrite(
                    f"images/raw/r_ball/red_ball-ref-pic-raw-{red_ball_images}.jpeg",
                    frame,
                )
                print(
                    "Taken red_ball image is written under images/raw/r_ball/ folder."
                )
                red_ball_images += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        else:
            try:
                cap = camera.camera_init()
            except Exception:
                pass

    except (Exception, KeyboardInterrupt):
        break

camera.stop(cv2, cap)
