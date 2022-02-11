import sys
import argparse
from pathlib import Path

sys.path.append(str(Path("..").absolute().parent))
from misc.functions import network


parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--mode",
    help="NetworkTables sub table mode",
    required=True,
    choices=["ball", "hoop"],
)
args = parser.parse_args()

table = network.nt_listener_init()

sub_table = table.getSubTable(args.mode)


def try_get_string(key, nttable=table):
    return nttable.getString(key, "")


def try_get_number(key, nttable=table):
    return nttable.getNumber(key, 0)


while True:
    try:

        x = try_get_string(f"{args.mode}_X", sub_table)
        y = try_get_string(f"{args.mode}_Y", sub_table)
        w = try_get_string(f"{args.mode}_W", sub_table)
        h = try_get_string(f"{args.mode}_H", sub_table)
        d = try_get_string(f"{args.mode}_D", sub_table)
        r = try_get_string(f"{args.mode}_R", sub_table)
        b = try_get_string(f"{args.mode}_B", sub_table)
        alliance = try_get_string("alliance")
        period = try_get_string("period")
        position = try_get_number("position")

        print(
            f"X: {x} Y: {y} W: {w} H: {h} D: {d} R: {r} B: {b} alliance: {alliance} period: {period} position: {position}"
        )

    except KeyboardInterrupt:
        break
