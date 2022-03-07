import cv2
import numpy as np
import zmq
import waitress
from flask import Flask, render_template, Response
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind(f"tcp://{config.get('network', 'FLASK_SERVER')}:5802")
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.compat.unicode(""))

app = Flask(__name__)


def gen_frames():
    while True:
        source = footage_socket.recv()
        npimg = np.frombuffer(source, dtype=np.uint8)
        stream = cv2.imdecode(npimg, 1)
        buffer = cv2.imencode(".jpg", stream)[1]
        frame = buffer.tobytes()
        yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host=config.get("network", "FLASK_SERVER"), port=5801)
