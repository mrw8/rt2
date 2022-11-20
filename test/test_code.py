import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Concept
from ids_codes import Rui


def print_code(c):
	print("code for concept is", c.get_c_code())
	print("code system rui is", str(c.get_cs_rui().get_uuid()))
	x = c.get_name()
	if (x):
		print("concept name is", x)

def print_attribute(a):
	print("code for attribute is", a.get_r_code())
	print("code system rui is", str(a.get_cs_rui().get_uuid()))
	y = a.get_name()
	if (y):
		print("attribute name is", y)

csrui = Rui.Rui('A')
c1 = Concept.Concept("12345678", csrui)
c2 = Concept.Concept("98765432", csrui, "type 2 diabetes mellitus")

print("code 1")
print_code(c1)

print("code 2")
print_code(c2)

a1 = Concept.Attribute("456", csrui)
a2 = Concept.Attribute("101", csrui, "narrower than")
print("attribute 1")
print_attribute(a1)
print("attribute 2")
print_attribute(a2)