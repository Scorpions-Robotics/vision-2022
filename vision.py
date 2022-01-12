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
from misc.functions import flask


config = ConfigParser()
config.read("settings.ini")

print(f"Starting vision-processing...\nTime (UTC): {datetime.utcnow()}")

hoop_hsv_upper = tuple(config.get("colors", "HOOP_HSV_{UPPER}}").split("\n"))
hoop_hsv_lower = tuple(config.get("colors", "HOOP_HSV_{LOWER}").split("\n"))

kpw = int(config.get("calibration", "KNOWN_PIXEL_WIDTH"))
kd = int(config.get("calibration", "KNOWN_DISTANCE"))
kw = int(config.get("calibration", "KNOWN_WIDTH"))

table = network.nt_init()

camera = camera.os_action()

cascade_classifier = cv2.CascadeClassifier("cascade.xml")

hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f"tcp://{host_ip}:5555")

flask_popen = flask.run_flask()


try:

    while True:
        try:

            grabbed, frame = camera.read()

            if grabbed == True:

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
                r = video.rotation(int(config("FRAME_WIDTH")), x, w)
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

                if int(config("PRINT_VALUES")):
                    print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b}")

                if int(config("SHOW_FRAME")):
                    cv2.imshow("Result", video.crosshair(result))
                    cv2.waitKey(1)

                if int(config("STREAM_FRAME")):
                    encoded, buffer = cv2.imencode(".jpg", video.crosshair(frame))
                    footage_socket.send(buffer)

            else:
                try:
                    camera = camera.os_action()
                except Exception:
                    pass

        except KeyboardInterrupt:
            break

    try:
        flask_popen.kill()
    except AttributeError:
        pass

    camera.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(e)

    try:
        flask_popen.kill()
        camera.release()
        cv2.destroyAllWindows()
    except AttributeError:
        pass
