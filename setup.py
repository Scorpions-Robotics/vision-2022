import os
import sys
import subprocess
import platform
import argparse
from misc.functions import network
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

if platform.system() != "Linux":
    sys.exit("error: This can only run on Linux.")

parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    "--service_name",
    help="Name of the service you want to create.",
    default="vision",
)
args = parser.parse_args()

if os.path.isfile(f"/lib/systemd/system/{args.service_name}"):
    os.remove(f"/lib/systemd/system/{args.service_name}")

try:

    if network.is_connected():
        while True:
            subprocess.run(
                [
                    "sudo",
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "-r",
                    "requirements.txt",
                ],
                shell=False,
                check=True,
            )
            break

        while True:
            subprocess.run(
                ["sudo", "chmod", "+x", "misc/bash/install_os_dependencies.sh"],
                shell=False,
                check=True,
            )
            break

        while True:
            subprocess.run(
                ["sudo", "./misc/bash/install_os_dependencies.sh"], shell=False
            )
            break
    else:
        print(
            "Internet is not connected. Skipping dependency installations. \
            This may cause problems."
        )

    while True:
        subprocess.run(
            ["sudo", "addgroup", "--system", f"{args.service_name}"], shell=False
        )
        break

    while True:
        subprocess.run(
            [
                "sudo",
                "adduser",
                "--system",
                "--no-create-home",
                "--disabled-login",
                "--disabled-password",
                "--ingroup",
                f"{args.service_name}",
                f"{args.service_name}",
            ],
            shell=False,
        )
        break

    while True:
        subprocess.run(
            ["sudo", "usermod", "-a", "-G", "sudo", f"{args.service_name}"], shell=False
        )
        break

    while True:
        subprocess.run(
            ["sudo", "usermod", "-a", "-G", "video", f"{args.service_name}"],
            shell=False,
        )
        break

    while True:
        subprocess.run(
            ["sudo", "touch", f"/lib/systemd/system/{args.service_name}.service"],
            shell=False,
            check=True,
        )
        break

    service = f"""[Unit]
Requires=network-online.target
After=network-online.target
Description="{args.service_name} Service"
[Service]
WorkingDirectory={config.get("system","WORKING_DIR")}
ExecStart=/usr/bin/python {config.get("system","WORKING_DIR")}vision.py
User={args.service_name}
[Install]
WantedBy=multi-user.target"""

    with open(f"/lib/systemd/system/{args.service_name}.service", "w") as f:
        f.write(service)

    while True:
        subprocess.run(["sudo", "systemctl", "daemon-reload"], shell=False, check=True)
        break

    while True:
        subprocess.run(
            ["sudo", "systemctl", "enable", f"{args.service_name}"],
            shell=False,
            check=True,
        )
        break

    if not os.path.isfile("settings.ini"):
        print("No settings.ini found. Creating one.")
        while True:
            subprocess.run(
                ["sudo", "cp", "settings.ini.template", "settings.ini"],
                shell=False,
                check=True,
            )
            break

    print("vision-2022 is installed and enabled. It will start automatically on boot.")

except Exception as e:
    print("error: Please run as root. (sudo python setup.py)")
    print(e)
