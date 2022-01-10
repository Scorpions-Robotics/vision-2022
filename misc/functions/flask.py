# Run Flask
def run_flask():
    if int(config("STREAM_FRAME")):
        return subprocess.Popen(["python", "misc/flask/flask_server.py"], shell=False)
