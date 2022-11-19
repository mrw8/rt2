from rui import Rui


def print_info(rui):
	print(rui)
	print("assigned? " + str(rui.is_assigned()))
	print("reserved? " + str(rui.is_reserved()))
	print("uuid: " + str(rui.get_uuid()))

x = Rui.Rui('A')
y = Rui.Rui('R')

print_info(x)
print_info(y)
