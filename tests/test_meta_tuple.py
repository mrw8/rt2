from datetime import datetime, timezone
from rt_core_v2.ids_codes import Rui
from rt_core_v2.rttuple import DTuple, FTuple, ATuple
from rt_core_v2.metadata_accessory import TupleEventType, RtChangeReason


# print functions 
def print_d_tuple(dt):
	print("<", dt.ruit.uuid, "> did a(n) ", dt.event, " to tuple <", dt.ruit_ref.uuid, "> because of ", dt.event_reason, " at ", str(dt.td))
	print("\tany replacement tuples: ", dt.replacements) 
	print()

def print_f_tuple(ft):
	print("<", ft.ruia.uuid, "> has confidence level '", ft.C, "' in tuple <", ft.ruit.uuid, "> at ", ft.ta)
	print("\ttuple rui: ", ft.ruit.uuid)

# create two ATuples with a = rui of person assigning rui to things
a = Rui.Rui()
s = Rui.Rui()
w = ATuple(a, ruia=a, unique="+SU")
x = ATuple(s, ruia=a, unique="+SU")

# create two D tuples for each ATuple
# the entity registering the tuples in the RTS
dr = Rui.Rui()
# metadata or D tuple for w (ATuple)
dt1 = DTuple(w.ruit, dr, Rui.TempRef(), TupleEventType.INSERT, RtChangeReason.RELEVANCE)
# metadata or D tuple for x (ATuple)
dt2 = DTuple(x.ruit, dr, Rui.TempRef(), TupleEventType.INSERT, RtChangeReason.REALITY)

print_d_tuple(dt1)
print_d_tuple(dt2)

# now create an FTuple for each ATuple.  ruitn, ruia, ta, C, ruit=None):
# actually at the moment this is a mistake. ATuples won't have associated FTuples. We just need to build the other template types first.
ft1 = FTuple(w.ruit, a, Rui.TempRef(), Rui.Rui(), Rui.Rui())
ft2 = FTuple(x.ruit, a, Rui.TempRef(), Rui.Rui(), Rui.Rui())
print_f_tuple(ft1)
print_f_tuple(ft2)
