import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Rui
from rtt.atuple import Atuple

def print_atuple(a):
	print("rui that denotes tuple itself", str(a.get_ruit().get_uuid()))
	print("rui that denotes rui assigned to some PoR", str(a.get_ruip().get_uuid()))
	print("rui that denotes rui of person who assigned ruip to some PoR", str(a.get_ruia().get_uuid()))
	print("time that ruia assigned ruip to some PoR", str(a.get_t()))

x = Rui.Rui('A')
y = Atuple(x)
print_atuple(y)
