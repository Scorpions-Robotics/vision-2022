# Scorpions Robotics #7672

## FRC Rapid React Vision Processing

[![GitHub](https://img.shields.io/github/license/Scorpions-Robotics/vision-2022?color=blue&label=License&logo=apache-license)](https://raw.githubusercontent.com/Scorpions-Robotics/vision-2022/HEAD/LICENSE) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/opencv-contrib-python?label=Python&logo=python&logoColor=white)](https://python.org) [![Code Style: Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black) [![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=flat&logo=OpenCV&logoColor=white)](https://opencv.org)

[![CodeFactor](https://www.codefactor.io/repository/github/scorpions-robotics/vision-2022/badge)](https://www.codefactor.io/repository/github/scorpions-robotics/vision-2022) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cb4eea74001046a98d167e3d0210d2ac)](https://www.codacy.com/gh/Scorpions-Robotics/vision-2022/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Scorpions-Robotics/vision-2022&amp;utm_campaign=Badge_Grade) [![CodeQL](https://github.com/Scorpions-Robotics/vision-2022/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Scorpions-Robotics/vision-2022/actions/workflows/codeql-analysis.yml)

## Runs on:

[![NVIDIA Jetson Nano 4Gb](https://img.shields.io/badge/NVIDIA-Jetson%20Nano%204GB-76B900?style=flat&logo=nvidia&logoColor=white)](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)

## How do we process the vision?

We use the Open Source Computer Vision Library [OpenCV](https://opencv.org/) with Cascade Classifier features to detect and track the target.

### Details:

1. Detect the host computer's OS, hostname and IP address.

2. Initialize NetworkTables client and stream server, then connect to the "vision" table.

3. Define the camera according to the OS and parameters.

4. Define the cascade classifier path. (**The classifier we used is trained to detect FRC Power Ports, and can be downloaded from [here](https://github.com/Scorpions-Robotics/cascade-2022/releases)**)

5. while True:
    - Read the image from the camera.
    - Detect the target using the cascade_classifier.detectMultiScale() method.
    - If the target is detected, draw a rectangle around it.
    - Display the image.
    - Send the target's position to the NetworkTables.
    - Wait for the next frame.

&nbsp;

## Compatible Operating Systems:

- [![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/en-us/windows/) &emsp; Windows 7 or newer

- [![macOS](https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white)](https://www.apple.com/) &emsp; macOS 10.6 or newer

- [![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)](https://www.linuxfoundation.org/) &emsp; Most linux distros

&nbsp;

## Installation:

1. Clone the repository.&emsp;```git clone https://github.com/Scorpions-Robotics/vision-2022.git```

2. Install the required dependencies.&emsp;```pip install --upgrade -r requirements.txt```

3. On Linux you have to install extra dependencies.
   - ```cd misc/bash/```
   - ```chmod +x *```
   - ```./install_os_dependencies.sh```

&nbsp;

## Usage:

1. Copy ``settings.ini.template`` and rename it to ``settings.ini``. Then edit it to your needs.

2. Run the ``vision.py`` file to start the vision processing.

&nbsp;

## ***Important Note:***

- **Always make sure to run the file from the root directory of the project.**

- Always keep the dependencies up to date.

- Always use the latest stable version of this project.

&nbsp;

## Our Social Media Accounts and Discord Server

[![Instagram](https://img.shields.io/badge/scorpions7672-E1306C?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/scorpions7672) [![YouTube](https://img.shields.io/badge/Scorpions%207672-FF0000?style=flat&logo=youtube)](https://www.youtube.com/channel/UCLsK3acedtyaD6dABW39g2Q) [![Discord](https://img.shields.io/discord/854741003700666388.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/MqvbYPecgt)

- Instagram: <https://instagram.com/scorpions7672>

- YouTube: <https://www.youtube.com/channel/UCLsK3acedtyaD6dABW39g2Q>

- Discord Server: <https://discord.gg/MqvbYPecgt>

&nbsp;

## Contact

- E-mail: scorpions7672@gmail.com

- Address: [Molla Yusuf Mah. Hürriyet Cad. No: 25 Konyaaltı/Antalya, Türkiye](https://goo.gl/maps/5YjF16fynHth8VVB9)

&nbsp;

## Contributing:

1. If you have any suggestions, or found any bugs, please open an issue or create a pull request.

2. Don't hesitate to open an issue if you have any questions about the code.

&nbsp;

## Authors

- **[@egeakman](https://github.com/egeakman)**

- **[@ardasak](https://github.com/ardasak)**

&nbsp;

## License

*This project is licensed under the [Apache-2.0](https://raw.githubusercontent.com/Scorpions-Robotics/vision-2022/HEAD/LICENSE) license. All rights reserved.*
