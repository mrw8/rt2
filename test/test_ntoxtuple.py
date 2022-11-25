import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Rui
from rtt.atuple import Atuple
from rtt.ntoxtuple import NtoR, NtoN, NtoDE, NtoC, NtoLackR

def print_atuple(a):
	print("A tuple information:")
	print("\truit: the rui that denotes tuple itself", str(a.ruit.uuid))
	print("\truip: rui that was assigned to some PoR", str(a.ruip.uuid))
	print("\tis ruip reserved? ", a.ruip.is_reserved())
	print('\tis ruip singularly unique vs. potentially non-singularly unique: ', a.unique)
	print("\truia: rui that denotes person who assigned ruip to some PoR", str(a.ruia.uuid))
	print("\tt: time that ruia assigned/reserved ruip to/for some PoR", str(a.t))
	print()

def print_ntor_tuple(ntor):
	print("NtoR tuple information:")
	print("\truit: the rui that the system assigned to the NtoR tuple itself --", str(ntor.ruit.uuid))
	print("\truin: the rui that denotes the non-repeatable PoR that this tuple is about --", str(ntor.ruin.uuid))
	print("\truir: the rui that denotes the repeatable PoR to which the non-repeatable PoR (denoted by ruinI) is related --", ntor.ruir.uuid)
	print("\tr: the relationship between the non-repeatable PoR and the repeatable PoR --", str(ntor.r))
	print("\ttr: the time at which the relationship between the non-repeatable PoR and the repeatable PoR holds --", str(ntor.tr.uuid))
	print("\tpolarity: the relationship holds (true) or does not hold (false) --", str(ntor.polarity))
	print()

# Rui that represents the person authoring these tuples
a = Rui.Rui('A')
# Rui that stands for the repeatable PoR called "human being"
h = Rui.Rui('A')
# Rui that stands for interval over which author has been instance of human being
tr = Rui.Rui('A')

ntor = NtoR(None, a, True, "instance of", h, tr)
print_ntor_tuple(ntor)

x = Rui.Rui('A')
y = Atuple(x)
print_atuple(y)

q = Rui.Rui('R')
z = Atuple(q, ruia=a, unique="+SU", ar='R')
print_atuple(z)

s = Rui.Rui('A')
w = Atuple(s, ruia=a, unique="+SU")
print_atuple(w)
