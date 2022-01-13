import cv2
import imutils
import zmq
import socket
from datetime import datetime
from configparser import ConfigParser
from misc.functions import network
from misc.functions import camera
from misc.functions import video
from misc.functions import process
from misc.functions import flask_func


config = ConfigParser()
config.read("settings.ini")

print(f"Starting vision-processing...\nTime (UTC): {datetime.utcnow()}")

hoop_hsv_upper = tuple(map(int, config.get("colors", "HOOP_HSV_UPPER").split("\n")))
hoop_hsv_lower = tuple(map(int, config.get("colors", "HOOP_HSV_LOWER").split("\n")))

kpw = int(config.get("calibration", "KNOWN_PIXEL_WIDTH"))
kd = int(config.get("calibration", "KNOWN_DISTANCE"))
kw = int(config.get("calibration", "KNOWN_WIDTH"))

table = network.nt_init()

cap = camera.os_action()

cascade_classifier = cv2.CascadeClassifier("cascade.xml")

hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f"tcp://{host_ip}:5555")

flask_popen = flask_func.run_flask()

count = 0

try:

    while True:
        try:

            grabbed, frame = cap.read()

            if grabbed == True:

                if count == 1:
                    camera.switch("ball")

                frame = imutils.resize(
                    frame,
                    width=int(config.get("camera", "FRAME_WIDTH")),
                    height=int(config.get("camera", "FRAME_HEIGHT")),
                )

                if int(config.get("fancy_stuff", "FLIP_FRAME")):
                    frame = cv2.flip(frame, 1)

                frame = imutils.rotate(
                    frame, int(config.get("fancy_stuff", "FRAME_ANGLE"))
                )

                if int(config.get("fancy_stuff", "WHITE_BALANCE")):
                    frame = camera.white_balance(frame)

                hsv_mask = process.mask_color(frame, (hoop_hsv_lower), (hoop_hsv_upper))
                result, x, y, w, h = process.vision(hsv_mask, cascade_classifier)

                d = video.current_distance(kpw, kd, kw, w)
                r = video.rotation(int(config.get("camera", "FRAME_WIDTH")), x, w)
                b = int(video.is_detected(d))

                try:
                    d = round(d, 2)
                    r = round(r, 2)
                except Exception:
                    pass

                table.putString("X", x)
                table.putString("Y", y)
                table.putString("W", w)
                table.putString("H", h)
                table.putString("D", d)
                table.putString("R", r)
                table.putString("B", b)

                if int(config.get("fancy_stuff", "PRINT_VALUES")):
                    print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b}")

                if int(config.get("fancy_stuff", "SHOW_FRAME")):
                    cv2.imshow("Result", video.crosshair(result))
                    cv2.waitKey(1)

                if int(config.get("fancy_stuff", "STREAM_FRAME")):
                    encoded, buffer = cv2.imencode(".jpg", video.crosshair(frame))
                    footage_socket.send(buffer)

                if count == 0:
                    count += 1

            else:
                try:
                    cap = camera.os_action()
                except Exception:
                    pass

        except KeyboardInterrupt:
            break

    try:
        flask_popen.kill()
    except AttributeError:
        pass

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(e)

    try:
        flask_popen.kill()
        cap.release()
        cv2.destroyAllWindows()
    except AttributeError:
        pass
