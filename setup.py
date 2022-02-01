import os
import subprocess
import platform
import argparse
from misc.functions import network
from configparser import ConfigParser


config = ConfigParser()
config.read("settings.ini")

if platform.system() != "Linux":
    exit("error: This can only run on Linux.")

try:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--service_name", help="Name of the service you want to create."
    )
    args = parser.parse_args()

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
            )
            break
    else:
        print(
            "Internet is not connected. Skipping dependency installations. This may cause problems."
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
        subprocess.run(["sudo", "systemctl", "daemon-reload"], shell=False)
        break

    while True:
        subprocess.run(
            ["sudo", "systemctl", "enable", f"{args.service_name}"], shell=False
        )
        break

    if not os.path.isfile("settings.ini"):
        print("No settings.ini found. Creating one.")
        while True:
            subprocess.run(
                ["sudo", "cp", "settings.ini.template", "settings.ini"], shell=False
            )
            break

    print("vision-2022 is installed and enabled. It will start automatically on boot.")

except Exception as e:
    print("error: Please run as root. (sudo python setup.py)")
    print(e)
