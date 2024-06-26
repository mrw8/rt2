from datetime import datetime, timezone
from src.ids_codes import Rui
from src.rttuple import Dtuple, Ftuple, Atuple
from src.rtt_meta.metadata_accessory import TupleEventType, RtChangeReason, RtErrorCode


# print functions 
def print_d_tuple(dt):
	print("<", dt.ruid.uuid, "> did a(n) ", dt.event, " to tuple <", dt.get_ruit().uuid, "> because of ", dt.event_reason, " at ", str(dt.td))
	print("\tany associated error code: ", dt.error)
	print("\tany replacement tuples: ", dt.replacements) 
	print()

def print_f_tuple(ft):
	print("<", ft.ruia.uuid, "> has confidence level '", ft.C, "' in tuple <", ft.ruitn.uuid, "> at ", ft.ta)
	print("\ttuple rui: ", ft.get_ruit().uuid)
	print("\tta: ", ft.ta.isoformat().replace('+00:00', 'Z'))

# create two Atuples with a = rui of person assigning rui to things
a = Rui.Rui(Rui.RuiStatus.assigned)
s = Rui.Rui(Rui.RuiStatus.assigned)
w = Atuple(a, ruia=a, unique="+SU")
x = Atuple(s, ruia=a, unique="+SU")

# create two D tuples for each Atuple
# the entity registering the tuples in the RTS
dr = Rui.Rui(Rui.RuiStatus.assigned)
# metadata or D tuple for w (Atuple)
dt1 = Dtuple(w.ruit, dr, TupleEventType.INSERT, RtChangeReason.RELEVANCE, None, datetime.now(timezone.utc), None)
# metadata or D tuple for x (Atuple)
dt2 = Dtuple(x.ruit, dr, TupleEventType.INSERT, RtChangeReason.REALITY, None, datetime.now(timezone.utc), None)

print_d_tuple(dt1)
print_d_tuple(dt2)

# trying out some datetime stuff in Python
utc_dttm = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
print(utc_dttm)
dttm = datetime.fromisoformat(utc_dttm)
print(dttm)

# now create an Ftuple for each Atuple.  ruitn, ruia, ta, C, ruit=None):
# actually at the moment this is a mistake. Atuples won't have associated Ftuples. We just need to build the other template types first.
ft1 = Ftuple(w.ruit, a, dttm, 'certain')
ft2 = Ftuple(x.ruit, a, dttm, 'certain')
print_f_tuple(ft1)
print_f_tuple(ft2)
