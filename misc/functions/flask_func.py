import subprocess
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")


# Run Flask
def run_flask():
    if config.getint("fancy", "STREAM_FRAME"):
        return subprocess.Popen(["python", "misc/flask/flask_server.py"], shell=False)
