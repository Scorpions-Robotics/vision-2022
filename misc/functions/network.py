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
def is_connected() -> bool:
    try:
        requests.get("http://google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


# Initialize NetworkTables.
def nt_init() -> NetworkTables.getTable:
    if config.getint("network", "NETWORKTABLES_SERVER_MODE"):
        NetworkTables.initialize()
    else:
        NetworkTables.initialize(server=nt_server)
    return NetworkTables.getTable(nt_table)


# Initialize NetworkTables listener.
def nt_listener_init() -> NetworkTables.getTable:
    NetworkTables.initialize(server=nt_server)
    return NetworkTables.getTable(nt_table)


# Initialize zmq server.
def zmq_init() -> zmq.Context:
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.connect(f"tcp://{config.get('network', 'FLASK_SERVER')}:5802")

    return footage_socket


# Get information from Java side.
def nt_get_info(table) -> tuple:
    return table.getString("mode", "hoop"), table.getString("alliance", "blue")


# Assign tuples for alliance upper hsv values.
def set_alliance_hsv_upper(alliance) -> tuple:
    if alliance == "red":
        return tuple(map(int, config.get("colors", "RED_BALL_HSV_UPPER").split("\n")))
    return tuple(map(int, config.get("colors", "BLUE_BALL_HSV_UPPER").split("\n")))


# Assign tuples for alliance lower hsv values.
def set_alliance_hsv_lower(alliance) -> tuple or None:
    if alliance == "red":
        return tuple(map(int, config.get("colors", "RED_BALL_HSV_LOWER").split("\n")))
    return tuple(map(int, config.get("colors", "BLUE_BALL_HSV_LOWER").split("\n")))


# Assign tuples for hoop hsv values.
def set_hoop_hsv() -> tuple:
    return tuple(map(int, config.get("colors", "HOOP_HSV_UPPER").split("\n"))), tuple(
        map(int, config.get("colors", "HOOP_HSV_LOWER").split("\n"))
    )


# Put NetworkTables variables.
def put(sub_table, mode, x, y, w, h, d, r, b):
    sub_table.putString(f"{mode}_X", x)
    sub_table.putString(f"{mode}_Y", y)
    sub_table.putString(f"{mode}_W", w)
    sub_table.putString(f"{mode}_H", h)
    sub_table.putString(f"{mode}_D", d)
    sub_table.putString(f"{mode}_R", r)
    sub_table.putString(f"{mode}_B", b)
