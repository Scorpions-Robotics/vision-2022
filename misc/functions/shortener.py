import sys
from pathlib import Path
from configparser import ConfigParser

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import video


config = ConfigParser()
config.read("settings.ini")


def fancies(result, cv2, footage_socket, frame, mode, x, y, w, h, d, r, b):
    if config.getint("fancy", "SHOW_FRAME"):
        cv2.imshow("Result", video.crosshair(result))
        cv2.waitKey(1)

    if config.getint("fancy", "PRINT_VALUES"):
        print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b} Mode: {mode}")

    if config.getint("fancy", "STREAM_FRAME"):
        encoded, buffer = cv2.imencode(".jpg", video.crosshair(frame))
        if encoded:
            footage_socket.send(buffer)

    if config.getint("fancy", "SHOW_DISTANCE"):
        video.show_distance(result, d, mode)
