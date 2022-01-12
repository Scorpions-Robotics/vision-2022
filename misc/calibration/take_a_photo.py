import cv2
import imutils
import sys
from pathlib import Path
from configparser import ConfigParser

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import camera


config = ConfigParser()
config.read("settings.ini")

camera = camera.os_action()

while True:
    try:
        grabbed, frame = camera.read()

        if grabbed == True:

            frame = imutils.resize(
                frame,
                width=int(config.get("camera", "FRAME_WIDTH")),
                height=int(config.get("camera", "FRAME_HEIGHT")),
            )

            if int(config.get("fancy_stuff", "FLIP_FRAME")) == 1:
                frame = cv2.flip(frame, 1)

            frame = imutils.rotate(frame, int(config.get("fancy_stuff", "FRAME_ANGLE")))

            if int(config.get("fancy_stuff", "WHITE_BALANCE")) == 1:
                frame = camera.white_balance(frame)

            cv2.imshow("img", frame)
            if cv2.waitKey(1) & 0xFF == ord("y"):
                cv2.imwrite("images/ref-pic.jpeg", frame)
                print("Taken image is written under images folder.")
                break

        else:
            try:
                camera = camera.os_action()
            except Exception:
                pass

    except KeyboardInterrupt:
        break

camera.release()
cv2.destroyAllWindows()
