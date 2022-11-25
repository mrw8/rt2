import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Rui
from rtt.atuple import NtoXTuple, NtoXGenericTuple

class NtoN(NtoXTuple):

	"""Tuple type that relates two or more non-repeatable portions of reality to one another"""

	#NtoN#< ‘+’/‘-’, r, P, rT/‘-’, tr/‘-’>
	def __init__(self, ruit, ruin, polarity, r, p_list, tr):
		super().__init__(ruit, ruin, r, polarity)
		self.p_list = p_list.copy()
		self.tr = tr

class NtoR(NtoXTuple):

	"""Tuple type that relates a non-repeatable portion of reality to a repeatable portion of reality"""

	#NtoR#< ‘+’/‘-’, inst, RUIn, RUIr, rT/‘-’, tr/‘-’>
	def __init__(self, ruit, ruin, polarity, r, ruir, tr):
		super().__init__(ruit, ruin, r, polarity)
		self.tr = tr 
		self.ruir = ruir

class NtoC(NtoXTuple):

	#NtoC#< ‘+’/‘-’, r, RUIcs, RUIp, code, rT, tr>
	def __init__(self, ruit, ruin, polarity, r, ruics, code, tr):
		super().__init__(ruit, ruin, r, polarity)
		self.tr = tr 
		self.ruics = ruics
		self.code = code 

class NtoDE(NtoXTuple):
	#NtoDE#< '+/-', r, ruin, ruins, data, ruidt
	def __init__(self, ruit, ruin, polarity, r, ruins, data, ruidt):
		super().__init__(ruit, ruin, r, polarity)
		self.ruins = ruins
		self.data = data
		self.ruidt = ruidt

class NtoLackR(NtoXGenericTuple):

	#NtoR(-) -tuple NtoR(-)#< r, RUIp, RUIr, rT/‘-’, tr/‘-’>
	def __init__(self, ruit, ruin, r, ruir, tr):
		super()._init__(self, ruit, ruin, r)
		self.ruir = ruir
		self.tr = tr 


