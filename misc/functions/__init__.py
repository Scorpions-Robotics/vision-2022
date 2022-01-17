import time
from configparser import ConfigParser

config = ConfigParser()
config.read("settings.ini")


def warm_up():
    if config.getint("system", "WAIT_FOR_JETSON"):
        time.sleep(10)
