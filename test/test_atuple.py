import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Rui
from rtt.atuple import Atuple

def print_atuple(a):
	print("tuple information:")
	print("\truit: the rui that denotes tuple itself", str(a.get_ruit().get_uuid()))
	print("\truip: rui that was assigned to some PoR", str(a.get_ruip().get_uuid()))
	print("\tis ruip reserved? ", a.get_ruip().is_reserved())
	print('\tis ruip singularly unique vs. potentially non-singularly unique: ', a.get_su_status())
	print("\truia: rui that denotes person who assigned ruip to some PoR", str(a.get_ruia().get_uuid()))
	print("\tt: time that ruia assigned/reserved ruip to/for some PoR", str(a.get_t()))
	print()


a = Rui.Rui('A')

x = Rui.Rui('A')
y = Atuple(x)
print_atuple(y)

q = Rui.Rui('R')
z = Atuple(q, ruia=a, unique="+SU", ar='R')
print_atuple(z)

s = Rui.Rui('A')
w = Atuple(s, ruia=a, unique="+SU")
print_atuple(w)
