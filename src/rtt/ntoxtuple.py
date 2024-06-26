from src.ids_codes import Rui
from src.rtt.atuple import RtTuple

# This class is the superclass of all Nto* tuples. They all relate some
#	non-repeatable portion of reality to some portion of reality (in 
#	some cases a repeatable PoR, and in others non-repeatable ones) or
#	in the case of NtoC, it is asserting that the N is "annotated by"
#	the "concept" from some concept system.
# We require the NtoXGenericTuple to accomodate NtoLackR
#	All the other Nto* tuples extend NtoXTuple
# 
class NtoXGenericTuple(RtTuple):
	def __init__(self, ruit, ruin, r):
		super().__init__(ruit)
		if ruin is None:
			raise Exception("must provide a value for RUIn")
		if r is None:
			raise Exception("must provide a value for r")
		
		self.ruin = ruin
		self.r = r 

# Except for NtoLackR, Nto* tuples can be asserted as being
#  true or false (i.e., "it is not the case that...")
class NtoXTuple(NtoXGenericTuple):
	def __init__(self, ruit, ruin, r, polarity: bool):
		super().__init__(ruit, ruin, r)
		self.polarity = polarity

	def isPositive(self):
		return self.polarity

	def isNegated(self):
		return not self.polarity


class NtoN(NtoXTuple):

	"""Tuple type that relates two or more non-repeatable portions of reality to one another"""

	#NtoN#< ‘+’/‘-’, r, P, rT/‘-’, tr/‘-’ >
	def __init__(self, ruit, ruin, polarity, r, p_list, tr):
		super().__init__(ruit, ruin, r, polarity)
		self.p_list = p_list.copy()
		self.tr = tr

class NtoR(NtoXTuple):

	"""Tuple type that relates a non-repeatable portion of reality to a repeatable portion of reality"""

	#NtoR#< ‘+’/‘-’, inst, RUIn, RUIr, rT/‘-’, tr/‘-’ >
	def __init__(self, ruit, ruin, polarity, r, ruir, tr):
		super().__init__(ruit, ruin, r, polarity)
		self.tr = tr 
		self.ruir = ruir

class NtoC(NtoXTuple):

	"""Tuple type that annotates a non-repeatable portion of reality with a "concept" code from a
		concept-based system"""

	#NtoC#< ‘+’/‘-’, r, RUIcs, RUIp, code, rT, tr >
	def __init__(self, ruit, ruin, polarity, r, ruics, code, tr):
		super().__init__(ruit, ruin, r, polarity)
		self.tr = tr 
		self.ruics = ruics
		self.code = code 

# We use NtoDE instead of NtoI, and we use an instance for the identifying descriptor
# or IdD associated with:
#	(1) and NtoR tuple that says what type of IdD it is, 
#	(2) an NtoN tuple to relate the name to what the IdD denotes, and 
#	(3) an NtoDE tuple to hold the actual written (or "string") form of the IdD. 
# Note that an IdD can be a name, identifier, etc.
class NtoDE(NtoXTuple):
	#NtoDE#< '+/-', r, ruin, ruins, data, ruidt >
	def __init__(self, ruit, ruin, polarity, r, ruins, data, ruidt):
		super().__init__(ruit, ruin, r, polarity)
		self.ruins = ruins
		self.data = data
		self.ruidt = ruidt

class NtoLackR(NtoXGenericTuple):

	"""Tuple type that asserts that for all instances of a given type, a specific
		non-repeatable portion of reality is not related to any of them by a 
		given relation"""

	#NtoR(-) -tuple NtoR(-)#< r, RUIp, RUIr, rT/‘-’, tr/‘-’ >
	def __init__(self, ruit, ruin, r, ruir, tr):
		super()._init__(self, ruit, ruin, r)
		self.ruir = ruir
		self.tr = tr 


