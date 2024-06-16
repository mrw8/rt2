from ids_codes import Rui


def print_info(rui):
	print(rui)
	print("\tassigned? " + str(rui.is_assigned()))
	print("\treserved? " + str(rui.is_reserved()))
	print("\tuuid: " + str(rui.uuid))

x = Rui.Rui('A')
y = Rui.Rui('R')
z = Rui.Rui('R')

print_info(x)
print_info(y)
print()
print("z before status change")
print_info(z)
z.update_status_assigned()
print("\nz after status change")
print_info(z)
