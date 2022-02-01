from misc.functions import network
from pathlib import Path
import sys

sys.path.append(str(Path("..").absolute().parent))


table = network.nt_listener_init()


def try_get_string(key):
    return table.getString(key, "")


def try_get_number(key):
    return table.getNumber(key, 0)


while True:
    try:
        x = try_get_string("X")
        y = try_get_string("Y")
        w = try_get_string("W")
        h = try_get_string("H")
        d = try_get_string("D")
        r = try_get_string("R")
        b = try_get_string("B")
        alliance = try_get_string("alliance")
        period = try_get_string("period")
        position = try_get_number("position")

        print(
            f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b} alliance: {alliance} period: {period} position: {position}"
        )

    except KeyboardInterrupt:
        break
