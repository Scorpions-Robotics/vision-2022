import subprocess
import platform
import argparse
from misc.functions import functions
from decouple import config


if platform.system() != "Linux":
    exit("error: This can only run on Linux.")

functions.systemctl_log()

try:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--service_name", help="Name of the service you want to create."
    )
    args = parser.parse_args()

    if functions.is_connected():
        while True:
            subprocess.call(
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
        subprocess.call(
            ["sudo", "addgroup", "--system", f"{args.service_name}"], shell=False
        )
        break

    while True:
        subprocess.call(
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
        subprocess.call(
            ["sudo", "usermod", "-a", "-G", "sudo", f"{args.service_name}"], shell=False
        )
        break

    while True:
        subprocess.call(
            ["sudo", "usermod", "-a", "-G", "video", f"{args.service_name}"],
            shell=False,
        )
        break

    while True:
        subprocess.call(
            ["sudo", "touch", f"/lib/systemd/system/{args.service_name}.service"],
            shell=False,
        )
        break

    service = f"""[Unit]
Requires=network-online.target
After=network-online.target
Description="{args.service_name} Service"
[Service]
WorkingDirectory={config("WORKING_DIR")}
ExecStart=/usr/bin/python {config("WORKING_DIR")}vision.py
StandardOutput=append:{config("WORKING_DIR")}/log/stdout.log
StandardError=append:{config("WORKING_DIR")}/log/stderr.log
User={args.service_name}
[Install]
WantedBy=multi-user.target"""

    with open(f"/lib/systemd/system/{args.service_name}.service", "w") as f:
        f.write(service)

    while True:
        subprocess.call(["sudo", "systemctl", "daemon-reload"], shell=False)
        break

    while True:
        subprocess.call(
            ["sudo", "systemctl", "enable", f"{args.service_name}"], shell=False
        )
        break

    print("vision-2022 is installed and enabled. It will start automatically on boot.")

except Exception as e:
    print("error: Please run as root. (sudo python setup.py)")
    print(e)
