import requests
import zmq
import socket
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


# Initialize zmq server.
def zmq_init():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.connect(f"tcp://{host_ip}:5555")

    return footage_socket


# Get information from Java side.
def nt_get_info(table):
    return table.getString("mode", "hoop"), table.getString("alliance", "none")


# Assign tuples for alliance upper hsv values.
def set_alliance_hsv_upper(alliance):
    if alliance == "red":
        return tuple(map(int, config.get("colors", "RED_BALL_HSV_UPPER").split("\n")))
    elif alliance == "blue":
        return tuple(map(int, config.get("colors", "BLUE_BALL_HSV_UPPER").split("\n")))
    else:
        raise ValueError("Invalid alliance.")


# Assign tuples for alliance lower hsv values.
def set_alliance_hsv_lower(alliance):
    if alliance == "red":
        return tuple(map(int, config.get("colors", "RED_BALL_HSV_LOWER").split("\n")))
    elif alliance == "blue":
        return tuple(map(int, config.get("colors", "BLUE_BALL_HSV_LOWER").split("\n")))
    else:
        raise ValueError("Invalid alliance.")


# Assign tuples for hoop hsv values.
def set_hoop_hsv():
    tuple(map(int, config.get("colors", "HOOP_HSV_UPPER").split("\n"))), tuple(
        map(int, config.get("colors", "HOOP_HSV_LOWER").split("\n"))
    )


# Put NetworkTables variables.
def put(table, mode, x, y, w, h, d, r, b):
    table.putString(f"{mode}_X", x)
    table.putString(f"{mode}_Y", y)
    table.putString(f"{mode}_W", w)
    table.putString(f"{mode}_H", h)
    table.putString(f"{mode}_D", d)
    table.putString(f"{mode}_R", r)
    table.putString(f"{mode}_B", b)
