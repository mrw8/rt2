from rt_core_v2.rttuple import ATuple

from rt_core_v2.ids_codes.rui import Rui
from datetime import datetime, timezone


def print_ATuple(a):
    print("tuple information:")
    print("\trui: the rui that denotes tuple itself", str(a.rui.uuid))
    print("\truin: rui that was assigned to some PoR", str(a.ruin.uuid))
    print("\tis ruin reserved? ", a.ar)
    print(
        "\tis ruin singularly unique vs. potentially non-singularly unique: ", a.unique
    )
    print(
        "\truia: rui that denotes person who assigned ruin to some PoR",
        str(a.ruia.uuid),
    )
    print("\tt: time that ruia assigned/reserved ruin to/for some PoR", str(a.t))
    print()


a = Rui()

x = Rui()
y = ATuple(x)
print_ATuple(y)

q = Rui()
z = ATuple(q, ruia=a, unique="+SU", ar="R")
print_ATuple(z)

s = Rui()
w = ATuple(s, ruia=a, unique="+SU")
print_ATuple(w)

print(type(datetime.now(timezone.utc)))
