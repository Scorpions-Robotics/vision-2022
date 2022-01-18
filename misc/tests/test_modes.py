import sys
from pathlib import Path
from pynput import keyboard

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import network


table = network.nt_listener_init()


def on_press(key):
    if key == keyboard.Key.left:
        table.putString("alliance", "red")
        table.putString("mode", "ball")
    elif key == keyboard.Key.right:
        table.putString("alliance", "blue")
        table.putString("mode", "hoop")


listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
