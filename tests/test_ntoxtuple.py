from rt_core_v2.ids_codes import rui
from rt_core_v2.rttuple import ATuple, NtoRTuple, NtoNTuple, RuiStatus


def print_ATuple(a):
    print("A tuple information:")
    print("\truit: the rui that denotes tuple itself", str(a.ruit.uuid))
    print("\truip: rui that was assigned to some PoR", str(a.ruip.uuid))
    print("\tis ruip reserved? ", a.is_reserved())
    print(
        "\tis ruip singularly unique vs. potentially non-singularly unique: ", a.unique
    )
    print(
        "\truia: rui that denotes person who assigned ruip to some PoR",
        str(a.ruia.uuid),
    )
    print("\tt: time that ruia assigned/reserved ruip to/for some PoR", str(a.t))
    print()


def print_NtoRTuple_tuple(NtoRTuple):
    print("NtoRTuple tuple information:")
    print(
        "\truit: the rui that the system assigned to the NtoRTuple tuple itself --",
        str(NtoRTuple.ruit.uuid),
    )
    print(
        "\truin: the rui that denotes the non-repeatable PoR that this tuple is about --",
        str(NtoRTuple.ruin.uuid),
    )
    print(
        "\truir: the rui that denotes the repeatable PoR to which the non-repeatable PoR (denoted by ruinI) is related --",
        NtoRTuple.ruir.uuid,
    )
    print(
        "\tr: the relationship between the non-repeatable PoR and the repeatable PoR --",
        str(NtoRTuple.inst),
    )
    print(
        "\ttr: the time at which the relationship between the non-repeatable PoR and the repeatable PoR holds --",
        str(NtoRTuple.time.ref.uuid),
    )
    print(
        "\tpolarity: the relationship holds (true) or does not hold (false) --",
        str(NtoRTuple.polarity),
    )
    print()


def print_NtoNTuple_tuple(NtoNTuple):
    print("NtoNTuple tuple information:")
    print(
        "\truit: the rui that the system assigned to the NtoRTuple tuple itself --",
        str(NtoNTuple.ruit.uuid),
    )
    print(
        "\tP: the list of ruis that denote the non-repeatable PoRs that are related by r:"
    )
    for i in NtoNTuple.p_list:
        print("\t\t", i.uuid)
    print(
        "\tr: the relationship between the non-repeatable PoR and the repeatable PoR --",
        str(NtoNTuple.relation),
    )
    print(
        "\ttr: the time at which the relationship between the non-repeatable PoR and the repeatable PoR holds --",
        str(NtoNTuple.time.ref.uuid),
    )
    print(
        "\tpolarity: the relationship holds (true) or does not hold (false) --",
        str(NtoNTuple.polarity),
    )
    print()


# Rui that represents the person authoring these tuples
a = rui.Rui()
# Rui that stands for the repeatable PoR called "human being"
h = rui.Rui()
# Rui that stands for interval over which author has been instance of human being
tr1 = rui.Rui()
k = ATuple(tr1, ruia=a)

NtoRTuple = NtoRTuple(None, True, "part of", a, h, "Part of", rui.TempRef())
print_NtoRTuple_tuple(NtoRTuple)

# let x be the RUI standing for Kuala Lumpur
x = rui.Rui()
y = ATuple(x)
print_ATuple(y)

q = rui.Rui()
z = ATuple(q, ruia=a, ar=RuiStatus.reserved)
print_ATuple(z)

# let s be the RUI standing for the territory of Malaysia
s = rui.Rui()
w = ATuple(s, ruia=a)
print_ATuple(w)

# let tr2 be interval over which kuala lumpur has been part of Malaysia
tr2 = rui.Rui()
j = ATuple(tr2, ruia=a)
NtoNTuple = NtoNTuple(None, True, "part of", [x, s], "part of", rui.TempRef())
print_NtoNTuple_tuple(NtoNTuple)
