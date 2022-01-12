from configparser import ConfigParser

config = ConfigParser()
config.read("settings.ini")

for item, item_result in config.items("colors"):
    print(item, tuple(map(int, item_result.split("\n"))))
