from pathlib import Path
import sys

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import functions


table = functions.nt_listener_init()


def try_get_value(key):
    return table.getString(key, "")


while True:
    try:
        x = try_get_value("X")
        y = try_get_value("Y")
        w = try_get_value("W")
        h = try_get_value("H")
        d = try_get_value("D")
        r = try_get_value("R")
        b = try_get_value("B")
        alliance = try_get_value("alliance")
        period = try_get_value("period")
        position = table.getNumber("position",0)

        print(f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b} alliance: {alliance} period: {period} position: {position}")

    except KeyboardInterrupt:
        break
