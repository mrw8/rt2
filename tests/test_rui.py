from src.ids_codes.Rui import Rui, TempRef, RuiStatus
from uuid6 import uuid7
from datetime import datetime, timezone

def print_info(rui):
	print(rui)
	print("\tassigned? " + str(rui.is_assigned()))
	print("\treserved? " + str(rui.is_reserved()))
	print("\tuuid: " + str(rui.uuid))

def print_tr(tr):
	print(tr)
	print("uuid field=", tr.uuid)
	if (tr.cal != None):
		print("cal field=", tr.cal.isoformat('T'))
	else:
		print("cal field=", tr.cal)

x = Rui(RuiStatus.assigned)
y = Rui(RuiStatus.reserved)
z = Rui(RuiStatus.reserved)

print_info(x)
print_info(y)
print()
print("z before status change")
print_info(z)
z.update_status_assigned()
print("\nz after status change")
print_info(z)

j = TempRef(uuid7())
k = TempRef(datetime.now(timezone.utc))
m = TempRef(datetime.now())
n = TempRef(None,'U')
p = TempRef(None,'C')

print("\n### Temporal reference initialized with UUID ###")
print_tr(j)
print("##############\n")

print("### Temporal reference initialized with UTC now ###")
print_tr(k)
print("##############\n")

print("### Temporal reference initialized with local now ###")
print_tr(m)
print("##############\n")

print("### Temporal reference initialized with no id and instruction to create a new UUID ###")
print_tr(n)
print("##############\n")

print("### Temporal reference initialized with no id and instruction to create a UTC now datetime ###")
print_tr(p)
print("##############\n")
