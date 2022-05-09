import contextlib
import cv2
from datetime import datetime
from misc import functions
from configparser import ConfigParser
from misc.functions import network
from misc.functions import camera
from misc.functions import video
from misc.functions import process
from misc.functions import flask_func
from misc.functions import shortener

functions.warm_up()

config = ConfigParser()
config.read("settings.ini")

print(f"Starting vision-processing...\nTime (UTC): {datetime.utcnow()}")

hoop_hsv_upper, hoop_hsv_lower = network.set_hoop_hsv()

table = network.nt_init()
ball_table = table.getSubTable("ball")
hoop_table = table.getSubTable("hoop")

cap = camera.camera_init()

hoop_classifier = cv2.CascadeClassifier("hoop_classifier.xml")
ball_classifier = cv2.CascadeClassifier("ball_classifier.xml")

window_length = config.getint("calibration", "WINDOW_LENGTH")

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

                target_center_y = video.dimension_center(y, h)
                d = video.distance(target_center_y, mode)
                r = video.rotation(config.getint("camera", "FRAME_WIDTH"), x, w)
                b = int(video.is_detected(d))

                d = process.reduce_noise(window_length, d, "distance_lst")
                r = process.reduce_noise(window_length, r, "rotation_lst")

                d = video.safe_round(d)
                r = video.safe_round(r)

                result = video.show_distance(result, d, mode)

                network.put(hoop_table, mode, x, y, w, h, d, r, b)

            elif mode == "ball":
                resolution_rate = 1
                frame = video.settings(frame, resolution_rate)

                hsv_mask = process.mask_color(frame, (ball_hsv_lower), (ball_hsv_upper))
                result, x, y, w, h = process.vision(hsv_mask, ball_classifier)

                target_center_y = video.dimension_center(y, h)
                d = video.distance(target_center_y, mode)
                r = video.rotation(
                    config.getint("camera", "FRAME_WIDTH") * resolution_rate, x, w
                )
                b = int(video.is_detected(d))

                d = process.reduce_noise(window_length, d, "distance_lst")
                r = process.reduce_noise(window_length, r, "rotation_lst")

                d = video.safe_round(d)
                r = video.safe_round(r)

                result = video.show_distance(result, d, mode)

                network.put(ball_table, mode, x, y, w, h, d, r, b)

            shortener.fancies(
                result, cv2, footage_socket, result, mode, x, y, w, h, d, r, b
            )

        else:
            with contextlib.suppress(Exception):
                cap = camera.camera_init()

    except (Exception, KeyboardInterrupt) as e:
        print(e)
        break

camera.stop(cv2, cap, flask_popen)
