import subprocess
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

exposure = config.get("camera", "LINUX_HOOP_EXPOSURE")


def hoop_exposure():
    subprocess.run(
        ["v4l2-ctl", "-c", "exposure_auto=1",
            "-c", f"exposure_absolute={exposure}"],
        shell=False,
    )


def ball_exposure():
    subprocess.run(
        ["v4l2-ctl", "-c", "exposure_auto=3"],
        shell=False,
    )


def set_format():
    subprocess.run(
        [
            "v4l2-ctl",
            "--set-fmt-video=width=800,height=600,pixelformat=0",
            "--set-parm=30",
            "-c",
            "exposure_auto=3",
        ],
        shell=False,
    )
