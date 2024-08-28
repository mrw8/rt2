from rt_core_v2.rttuple import ANTuple

from rt_core_v2.ids_codes.rui import Rui
from datetime import datetime, timezone


def print_ANTuple(a):
    print("tuple information:")
    print("\trui: the rui that denotes tuple itself", str(a.rui.uuid))
    print("\truin: rui that was assigned to some PoR", str(a.ruin.uuid))
    print("\tis ruin reserved? ", a.ar)
    print(
        "\tis ruin singularly unique vs. potentially non-singularly unique: ", a.unique
    )
    print()


a = Rui()

x = Rui()
y = ANTuple(x)
print_ANTuple(y)

q = Rui()
z = ANTuple(q, unique="+SU", ar="R")
print_ANTuple(z)

s = Rui()
w = ANTuple(s, unique="+SU")
print_ANTuple(w)

print(type(datetime.now(timezone.utc)))
