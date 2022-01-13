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

hoop_kpw = int(config.get("calibration", "HOOP_KNOWN_PIXEL_WIDTH"))
hoop_kd = int(config.get("calibration", "HOOP_DISTANCE"))
hoop_kw = int(config.get("calibration", "HOOP_KNOWN_WIDTH"))

ball_kpw = int(config.get("calibration", "BALL_KNOWN_PIXEL_WIDTH"))
ball_kd = int(config.get("calibration", "BALL_DISTANCE"))
ball_kw = int(config.get("calibration", "BALL_KNOWN_WIDTH"))

table = network.nt_init()

cap = camera.os_action()


hoop_classifier = cv2.CascadeClassifier("hoop_classifier.xml")
ball_classifier = cv2.CascadeClassifier("ball_classifier.xml")

hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect(f"tcp://{host_ip}:5555")

flask_popen = flask_func.run_flask()


try:

    while True:
        try:

            grabbed, frame = cap.read()

            if grabbed == True:

                mode, alliance = network.nt_get_info()
                camera.switch(mode)

                if int(config.get("fancy_stuff", "FLIP_FRAME")):
                    frame = cv2.flip(frame, 1)

                frame = imutils.rotate(
                    frame, int(config.get("fancy_stuff", "FRAME_ANGLE"))
                )

                if int(config.get("fancy_stuff", "WHITE_BALANCE")):
                    frame = camera.white_balance(frame)

                if mode == "hoop":
                    frame = imutils.resize(
                        frame,
                        width=int(config.get("camera", "FRAME_WIDTH")),
                        height=int(config.get("camera", "FRAME_HEIGHT")),
                    )

                    mask = process.mask_color(frame, (hoop_hsv_lower), (hoop_hsv_upper))

                    result, hoop_x, hoop_y, hoop_w, hoop_h = process.hoop_vision(
                        mask, hoop_classifier
                    )

                    hoop_d = video.current_distance(hoop_kpw, hoop_kd, hoop_kw, hoop_w)
                    hoop_r = video.rotation(
                        int(config.get("camera", "FRAME_WIDTH")), hoop_x, hoop_w
                    )
                    hoop_b = int(video.is_detected(hoop_d))

                    try:
                        hoop_d = round(hoop_d, 2)
                        hoop_r = round(hoop_r, 2)
                    except Exception:
                        pass

                    if int(config.get("fancy_stuff", "PRINT_VALUES")):
                        print(
                            f"X: {hoop_x} Y: {hoop_y} W: {hoop_w} H: {hoop_h} D: {hoop_d} R: {hoop_r} B: {hoop_b} Mode: {mode}"
                        )

                if mode == "ball":
                    ball_hsv_upper, ball_hsv_lower = network.alliance(alliance)

                    frame = imutils.resize(
                        frame,
                        width=int(config.get("camera", "FRAME_WIDTH")),
                        height=int(config.get("camera", "FRAME_HEIGHT")),
                    )

                    mask = process.mask_color(frame, (ball_hsv_lower), (ball_hsv_upper))

                    result, ball_x, ball_y, ball_w, ball_h = process.ballz_vision(
                        mask, ball_classifier
                    )

                    ball_d = video.current_distance(ball_kpw, ball_kd, ball_kw, ball_w)
                    ball_r = video.rotation(
                        int(config.get("camera", "FRAME_WIDTH")), ball_x, ball_w
                    )
                    ball_b = int(video.is_detected(ball_d))

                    try:
                        ball_d = round(ball_d, 2)
                        ball_r = round(ball_r, 2)
                    except Exception:
                        pass

                    if int(config.get("fancy_stuff", "PRINT_VALUES")):
                        print(
                            f"X: {ball_x} Y: {ball_y} W: {ball_w} H: {ball_h} D: {ball_d} R: {ball_r} B: {ball_b} Mode: {mode}"
                        )

                table.putString("X", hoop_x)
                table.putString("Y", hoop_y)
                table.putString("W", hoop_w)
                table.putString("H", hoop_h)
                table.putString("D", hoop_d)
                table.putString("R", hoop_r)
                table.putString("B", hoop_b)

                if int(config.get("fancy_stuff", "SHOW_FRAME")):
                    cv2.imshow("Result", video.crosshair(result))
                    cv2.waitKey(1)

                if int(config.get("fancy_stuff", "STREAM_FRAME")):
                    encoded, buffer = cv2.imencode(".jpg", video.crosshair(frame))
                    footage_socket.send(buffer)

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
