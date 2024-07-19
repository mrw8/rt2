from rt_core_v2.rttuple import ATuple

from rt_core_v2.ids_codes.Rui import Rui
from datetime import datetime, timezone

def print_ATuple(a):
	print("tuple information:")
	print("\truit: the rui that denotes tuple itself", str(a.ruit.uuid))
	print("\truip: rui that was assigned to some PoR", str(a.ruip.uuid))
	print("\tis ruip reserved? ", a.is_reserved())
	print('\tis ruip singularly unique vs. potentially non-singularly unique: ', a.unique)
	print("\truia: rui that denotes person who assigned ruip to some PoR", str(a.ruia.uuid))
	print("\tt: time that ruia assigned/reserved ruip to/for some PoR", str(a.t))
	print()


a = Rui()

x = Rui()
y = ATuple(x)
print_ATuple(y)

q = Rui()
z = ATuple(q, ruia=a, unique="+SU", ar='R')
print_ATuple(z)

s = Rui()
w = ATuple(s, ruia=a, unique="+SU")
print_ATuple(w)

print(type(datetime.now(timezone.utc)))
