from ids_codes import Rui
from rttuple import Atuple, NtoR, NtoN, RuiStatus, NtoDE, NtoC, NtoLackR

def print_atuple(a):
	print("A tuple information:")
	print("\truit: the rui that denotes tuple itself", str(a.ruit.uuid))
	print("\truip: rui that was assigned to some PoR", str(a.ruip.uuid))
	print("\tis ruip reserved? ", a.is_reserved())
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

def print_nton_tuple(nton):
	print("NtoN tuple information:")
	print("\truit: the rui that the system assigned to the NtoR tuple itself --", str(nton.ruit.uuid))
	print("\truin: the rui that denotes the non-repeatable PoR that this tuple is about --", str(nton.ruin.uuid))
	print("\tP: the list of ruis that denote the non-repeatable PoRs that are related by r:")
	for i in nton.p_list:
		print("\t\t", i.uuid)
	print("\tr: the relationship between the non-repeatable PoR and the repeatable PoR --", str(nton.r))
	print("\ttr: the time at which the relationship between the non-repeatable PoR and the repeatable PoR holds --", str(nton.tr.uuid))
	print("\tpolarity: the relationship holds (true) or does not hold (false) --", str(nton.polarity))
	print()

# Rui that represents the person authoring these tuples
a = Rui.Rui()
# Rui that stands for the repeatable PoR called "human being"
h = Rui.Rui()
# Rui that stands for interval over which author has been instance of human being
tr1 = Rui.Rui()
k = Atuple(tr1, ruia=a)

ntor = NtoR(None, a, True, "instance of", h, tr1)
print_ntor_tuple(ntor)

#let x be the RUI standing for Kuala Lumpur
x = Rui.Rui()
y = Atuple(x)
print_atuple(y)

q = Rui.Rui()
z = Atuple(q, ruia=a, unique="+SU", ar=RuiStatus.reserved)
print_atuple(z)

#let s be the RUI standing for the territory of Malaysia
s = Rui.Rui()
w = Atuple(s, ruia=a, unique="+SU")
print_atuple(w)

#let tr2 be interval over which kuala lumpur has been part of Malaysia
tr2 = Rui.Rui()
j = Atuple(tr2, ruia=a)
nton = NtoN(None, x, True, "part of", [x, s], tr2)
print_nton_tuple(nton)
