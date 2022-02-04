from pathlib import Path
import sys

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import network


table = network.nt_listener_init()
ball_table = table.getSubTable("ball")
hoop_table = table.getSubTable("hoop")


def try_get_string(table, key):
    return table.getString(key, "")


def try_get_number(table, key):
    return table.getNumber(key, 0)


while True:
    try:
        x = try_get_string(ball_table, "X")
        y = try_get_string(ball_table, "Y")
        w = try_get_string(ball_table, "W")
        h = try_get_string(ball_table, "H")
        d = try_get_string(ball_table, "D")
        r = try_get_string(ball_table, "R")
        b = try_get_string(ball_table, "B")
        alliance = try_get_string(ball_table, "alliance")
        period = try_get_string(ball_table, "period")
        position = try_get_number(ball_table, "position")

        print(
            f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b} alliance: {alliance} period: {period} position: {position}"
        )

    except KeyboardInterrupt:
        break
