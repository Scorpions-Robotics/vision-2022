import cv2
import imutils
from decouple import config
import sys
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import functions


camera = functions.os_action()

while True:
    try:
        grabbed, frame = camera.read()

        if grabbed == True:

            frame = imutils.resize(
                frame,
                width=int(config("FRAME_WIDTH")),
                height=int(config("FRAME_HEIGHT")),
            )

            if int(config("FLIP_FRAME")) == 1:
                frame = cv2.flip(frame, 1)

            frame = imutils.rotate(frame, int(config("FRAME_ANGLE")))

            if int(config("WHITE_BALANCE")) == 1:
                frame = functions.white_balance(frame)

            cv2.imshow("img", frame)
            if cv2.waitKey(1) & 0xFF == ord("y"):
                cv2.imwrite("images/ref-pic.jpeg", frame)
                print("Taken image is written under images folder.")
                break

        else:
            try:
                camera = functions.os_action()
            except Exception:
                pass

    except KeyboardInterrupt:
        break

camera.release()
cv2.destroyAllWindows()
