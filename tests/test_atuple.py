from src.ids_codes import Rui
from src.rtt.atuple import Atuple
from datetime import datetime, timezone

def print_atuple(a):
	print("tuple information:")
	print("\truit: the rui that denotes tuple itself", str(a.ruit.uuid))
	print("\truip: rui that was assigned to some PoR", str(a.ruip.uuid))
	print("\tis ruip reserved? ", a.ruip.is_reserved())
	print('\tis ruip singularly unique vs. potentially non-singularly unique: ', a.unique)
	print("\truia: rui that denotes person who assigned ruip to some PoR", str(a.ruia.uuid))
	print("\tt: time that ruia assigned/reserved ruip to/for some PoR", str(a.t))
	print()


a = Rui.Rui(Rui.RuiStatus.assigned)

x = Rui.Rui(Rui.RuiStatus.assigned)
y = Atuple(x)
print_atuple(y)

q = Rui.Rui(Rui.RuiStatus.reserved)
z = Atuple(q, ruia=a, unique="+SU", ar='R')
print_atuple(z)

s = Rui.Rui(Rui.RuiStatus.assigned)
w = Atuple(s, ruia=a, unique="+SU")
print_atuple(w)

print(type(datetime.now(timezone.utc)))
