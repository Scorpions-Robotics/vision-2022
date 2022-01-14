from pathlib import Path
import sys

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import network


table = network.nt_listener_init()


from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.left:
        table.putString("alliance", "blue")
        table.putString("mode", "ball")
    elif key == keyboard.Key.right:
        table.putString("alliance","red") 
        table.putString("mode", "hoop")


listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()