# Checks internet connection.
def is_connected():
    try:
        request = requests.get("http://google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


# Initialize NetworkTables.
def nt_init():
    if int(config("NETWORKTABLES_TEST_MODE")):
        NetworkTables.initialize()
    else:
        NetworkTables.initialize(server=config("NETWORKTABLES_SERVER"))
    return NetworkTables.getTable(config("NETWORKTABLES_TABLE"))


# Initialize NetworkTables listener.
def nt_listener_init():
    NetworkTables.initialize(server=config("NETWORKTABLES_SERVER"))
    return NetworkTables.getTable(config("NETWORKTABLES_TABLE"))
