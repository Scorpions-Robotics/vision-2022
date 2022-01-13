import requests
from networktables import NetworkTables
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

nt_server = config.get("network", "NETWORKTABLES_SERVER")
nt_table = config.get("network", "NETWORKTABLES_TABLE")


# Checks internet connection.
def is_connected():
    try:
        request = requests.get("http://google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


# Initialize NetworkTables.
def nt_init():
    if int(config.get("network", "NETWORKTABLES_SERVER_MODE")):
        NetworkTables.initialize()
    else:
        NetworkTables.initialize(server=nt_server)
    return NetworkTables.getTable(nt_table)


# Initialize NetworkTables listener.
def nt_listener_init():
    NetworkTables.initialize(server=nt_server)
    return NetworkTables.getTable(nt_table)


def nt_get_info():
    table = NetworkTables.getTable(nt_table)
    return table.getString("mode", "hoop"), table.getString("alliance", "blue")


def alliance(alliance):
    if alliance == "red":
        return tuple(
            map(int, config.get("colors", "RED_BALL_HSV_UPPER").split("\n"))
        ), tuple(map(int, config.get("colors", "RED_BALL_HSV_LOWER").split("\n")))
    elif alliance == "blue":
        return tuple(
            map(int, config.get("colors", "BLUE_BALL_HSV_UPPER").split("\n"))
        ), tuple(map(int, config.get("colors", "BLUE_BALL_HSV_LOWER").split("\n")))
