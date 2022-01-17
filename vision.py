import cv2
from datetime import datetime
from misc import functions
from configparser import ConfigParser
from misc.functions import network
from misc.functions import camera
from misc.functions import video
from misc.functions import process
from misc.functions import flask_func

functions.warm_up()

config = ConfigParser()
config.read("settings.ini")

print(f"Starting vision-processing...\nTime (UTC): {datetime.utcnow()}")

hoop_hsv_upper, hoop_hsv_lower = network.set_hoop_hsv()

hoop_kpw = config.getint("calibration", "HOOP_KNOWN_PIXEL_WIDTH")
hoop_kd = config.getint("calibration", "HOOP_KNOWN_DISTANCE")
hoop_kw = config.getint("calibration", "HOOP_KNOWN_WIDTH")

ball_kpw = config.getint("calibration", "BALL_KNOWN_PIXEL_WIDTH")
ball_kd = config.getint("calibration", "BALL_KNOWN_DISTANCE")
ball_kw = config.getint("calibration", "BALL_KNOWN_WIDTH")

table = network.nt_init()
cap = camera.camera_init()

hoop_classifier = cv2.CascadeClassifier("hoop_classifier.xml")
# TODO: Add ball classifier.
# ball_classifier = cv2.CascadeClassifier("ball_classifier.xml")

footage_socket = network.zmq_init()
flask_popen = flask_func.run_flask()


while True:
    try:

        grabbed, frame = cap.read()
        mode, alliance = network.nt_get_info(table)
        cap = camera.switch(cap, mode)

        if grabbed:

            frame = camera.resolution_init(frame)

            ball_hsv_upper, ball_hsv_lower = (
                network.set_alliance_hsv_upper(alliance),
                network.set_alliance_hsv_lower(alliance),
            )

            if mode == "hoop":
                frame = video.settings(frame)

                hsv_mask = process.mask_color(frame, (hoop_hsv_lower), (hoop_hsv_upper))
                result, x, y, w, h = process.vision(hsv_mask, hoop_classifier)

                d = video.current_distance(hoop_kpw, hoop_kd, hoop_kw, w)
                r = video.rotation(config.get("camera", "FRAME_WIDTH"), x, w)
                b = int(video.is_detected(d))

                d = video.safe_round(d)
                r = video.safe_round(r)

                network.put(table, mode, x, y, w, h, d, r, b)

            elif mode == "ball":
                resolution_rate = 1
                frame = video.settings(frame, resolution_rate)

                hsv_mask = process.mask_color(frame, (ball_hsv_lower), (ball_hsv_upper))
                result, x, y, w, h = process.vision(
                    hsv_mask, hoop_classifier
                )  # TODO: Rename hoop_classifier to ball_classifier after it is defined.

                d = video.current_distance(ball_kpw, ball_kd, ball_kw, w)
                r = video.rotation(
                    config.getint("camera", "FRAME_WIDTH") * resolution_rate, x, w
                )
                b = int(video.is_detected(d))

                d = video.safe_round(d)
                r = video.safe_round(r)

                network.put(table, mode, x, y, w, h, d, r, b)

            if config.getint("fancy", "SHOW_FRAME"):
                cv2.imshow("Result", video.crosshair(result))
                cv2.waitKey(1)

            if config.getint("fancy", "PRINT_VALUES"):
                print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b} Mode: {mode}")

            if config.getint("fancy", "STREAM_FRAME"):
                encoded, buffer = cv2.imencode(".jpg", video.crosshair(frame))
                footage_socket.send(buffer)

        else:
            try:
                cap = camera.camera_init()
            except Exception:
                pass

    except (Exception, KeyboardInterrupt):
        break

camera.stop(cv2, cap, flask_popen)
