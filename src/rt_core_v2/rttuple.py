import enum
from abc import ABC, abstractmethod
from datetime import datetime, timezone
import logging

from rt_core_v2.ids_codes.Rui import Rui, TempRef

"""Takes an set of enums and converts them into a dict with mapping entry:value"""
def enum_to_dict(entries: set):
	return {entry: entry.value for entry in entries}

"""Enum for when the string representation of an enum instance is the value"""
class ValueEnum(enum.Enum):
	def __str__(self):
		return str(self.value)
	
"""Enum representing RUI statuses"""
class RuiStatus(ValueEnum):
	assigned = 'A'
	reserved = 'R'

"""Enum representing the tuple types"""
class TupleType(ValueEnum):
	A = 'A'
	D = 'D'
	F = 'F'
	NtoDE = 'NtoDE'
	NtoNTuple = 'NtoNTuple'
	NtoRTuple = 'NtoRTuple'
	NtoC = 'NtoC'
	NtoLackR = 'NtoRTuple(-)'

"""Enum representing portions of reality types"""
class PorType(ValueEnum):
	singular = '+SU'
	non_singular = '-SU'

#TODO Move this into the classes, as it is not a semantically sound placement here
class TupleComponents(enum.Enum):
	ruit = 'ruit'
	type = 'type'
	ar = 'ar'
	ruip = 'ruip'
	ruia = 'ruia'
	unique = 'unique'
	t = 't'
	ruid = 'ruid'
	event = 'event'
	event_reason = 'event_reason'
	td = 'td'
	replacements = 'replacements'
	ruitn = 'ruitn'
	ta = 'ta'
	C = 'C'
	polarity = 'polarity'
	r = 'r'
	p_list = 'p_list'
	rT = 'rT'
	tr = 'tr'
	inst = 'inst'
	ruin = 'ruin'
	ruir = 'ruir'
	ruics = 'ruics'
	code = 'code'
	ruins = 'ruins'
	data = 'data'
	ruidt = 'ruidt'

class RtTuple(ABC):
	tuple_type = None
	params = {**enum_to_dict({TupleComponents.ruit, TupleComponents.type})}
	def __init__(self, rui: Rui=None):
		self._rui = rui if rui else Rui()

	@property
	def ruit(self):
		"""Get the rui identifying this RtTuple"""
		return self._rui
	@ruit.setter
	def ruit(self, ruit):
		"""Set the rui identifying this RtTuple"""
		self._rui = ruit


	@abstractmethod
	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		return {self.params[TupleComponents.ruit]:str(self._rui), self.params[TupleComponents.type]:str(self.tuple_type)}

class ATuple(RtTuple):
	"""Referent Tracking assignment tuple that registers assignment of an RUI to a PoR
	
	Attributes:
	ar -- The status of ruip
	ruip -- The Rui that is being assigned for the first time
	ruia -- The Rui of the author of this ATuple
	unique -- Asserts whether this is a non-repeatable or repeatable portion of reality
	t -- The time of the creation of the ATuple
	"""
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.ar, TupleComponents.t, 
											 TupleComponents.ruia, TupleComponents.unique, TupleComponents.ruip})}
	tuple_type = TupleType.A

	def __init__(self, ruit: Rui=None, ruia: Rui=None, ruip: Rui=None, ar: RuiStatus=RuiStatus.assigned, unique: PorType=PorType.singular,
			  t=datetime.now(timezone.utc)):
		#TODO Change time to be a tempref
		super().__init__(ruit)
		self.ar = ar
		self.ruip = ruip if ruip else Rui()
		
		# If we don't get an author Rui for the tuple, then autogenerate one,
		#	unless we don't get a Ruip either, in which case set it to the
		#	autogenerated Ruip. 
		# This means that the default behavior is that if neither Ruia nor Ruip
		#	are provided, we are assuming some entity is assigning a Ruip to 
		#	itself, and thus should be equal
		self.ruia = ruia if ruia else Rui(self.ruip.uuid)
		self.unique = unique if type(unique) is PorType else PorType(unique)
		self._t = t
	@property
	def t(self):
		"""Get t"""
		return self._t
	@t.setter
	def t(self, t):
		"""Set t"""
		self._t = t

	def is_assigned(self):
		"""Returns whether this tuple is an assignment or not"""
		return self.ar is RuiStatus.assigned

	def is_reserved(self): 
		"""Returns whether this tuple is a reservation or not"""
		return self.ar is RuiStatus.reserved

	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.ruia]] = str(self.ruia)
		attributes[self.params[TupleComponents.ruip]] = str(self.ruip)
		attributes[self.params[TupleComponents.ar]] = str(self.ar)
		attributes[self.params[TupleComponents.unique]] = str(self.unique)
		attributes[self.params[TupleComponents.t]] = str(self._t)
		return attributes

	def create_assigned(self):
		"""Create an assignment A-tuple if this tuple is reserved"""
		if self.status is RuiStatus.assigned:
			logging.warning("status of Rui instance is already assigned. No change.")
			return self
		else:
			#TODO Figure out the process for creating d-tuples
			# return ATuple(self.ruip, self.ruia, self.ruit, self.unique, RuiStatus())
			pass

class DTuple(RtTuple):
	# D#< RUId, RUIT, t, ‘I’/E, R, S >

	tuple_type = TupleType.D
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.ruid, TupleComponents.event, 
											 TupleComponents.event_reason, TupleComponents.td, 
											 TupleComponents.replacements})}

	def __init__(self, ruid: Rui, ruit: Rui, t, event, event_reason, replacements=None):
		super().__init__(ruid)
		#TODO Figure out the argument count discrepancy between the parameter count and the D-tuple outline
		self.ruit_ref = ruit
		self.event = event
		self.event_reason = event_reason
		self.td = t if t else datetime.now(timezone.utc)
		self.replacements = replacements.copy() if replacements else None

	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = {}
		attributes[self.params[TupleComponents.type]] = str(self.tuple_type)
		attributes[self.params[TupleComponents.ruid]] = str(self.ruid)
		attributes[self.params[TupleComponents.ruit]] = str(self.ruit_ref)
		attributes[self.params[TupleComponents.event]] = str(self.event)
		attributes[self.params[TupleComponents.event_reason]] = str(self.event_reason)
		attributes[self.params[TupleComponents.t]] = str(self.td)
		attributes[self.params[TupleComponents.replacements]] = str(self.replacements)
		return attributes
	
	@property
	def ruid(self):
		return self.ruit
	
	@ruid.setter
	def ruid(self, ruid):
		self.ruit = ruid

class FTuple(RtTuple):
	#F#< RUId, ta, RUIa, RUIT, C >

	tuple_type = TupleType.F
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.ruitn, TupleComponents.ruia, TupleComponents.ta, TupleComponents.C})}
	
	def __init__(self, ruit: Rui=None, ruid: Rui=None, ta: TempRef=None, ruia: Rui=None, ruitn: Rui=None, C: float=1.0):
		super().__init__(ruit)
		self.ruid = ruid
		self.ruia = ruia
		self.ruitn = ruitn
		self.ta = ta
		self.C = C

	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		#TODO Get the attributes set for ruid.
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.ruid]] = str(self.ruid)
		attributes[self.params[TupleComponents.ruia]] = str(self.ruia)
		attributes[self.params[TupleComponents.ruitn]] = str(self.ruitn)
		attributes[self.params[TupleComponents.ta]] = str(self.ta)
		attributes[self.params[TupleComponents.C]] = str(self.C)

		return attributes

class NtoNTuple(RtTuple):
	"""Tuple type that relates two or more non-repeatable portions of reality to one another"""
	#NtoNTuple#< ‘+’/‘-’, r, P, rT/‘-’, tr/‘-’ >
	tuple_type = TupleType.NtoNTuple
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.polarity, TupleComponents.r, 
											 TupleComponents.p_list, TupleComponents.rT, TupleComponents.tr})}

	def __init__(self, ruit: Rui, polarity: bool, r: str, p: list[Rui], rT, tr: str):
		#TODO Add rt
		super().__init__(ruit)
		self.polarity = polarity
		self.reason = r
		self.p_list = p.copy()
		self.time_relation = rT
		self.time = tr
	
	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.polarity]] = str(self.polarity)
		attributes[self.params[TupleComponents.r]] = str(self.reason)
		attributes[self.params[TupleComponents.p_list]] = str(self.p_list)
		attributes[self.params[TupleComponents.rT]] = str(self.time_relation)
		attributes[self.params[TupleComponents.tr]] = str(self.time)
		return attributes
	
class NtoRTuple(RtTuple):
	"""Tuple type that relates a non-repeatable portion of reality to a repeatable portion of reality"""
	#NtoRTuple#< ‘+’/‘-’, inst, RUIn, RUIr, rT/‘-’, tr/‘-’ >

	tuple_type = TupleType.NtoRTuple
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.polarity, TupleComponents.inst, TupleComponents.ruin, 
											   TupleComponents.ruir, TupleComponents.rT, TupleComponents.tr})}

	def __init__(self, ruit: Rui, polarity: bool, inst: str, ruin: Rui, ruir: Rui, rT, tr: str):
		super().__init__(ruit)
		self.polarity = polarity
		self.inst = inst
		self.ruin = ruin
		self.ruir = ruir
		self.time_relation = rT
		self.time = tr 

	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.polarity]] = str(self.polarity)
		attributes[self.params[TupleComponents.inst]] = str(self.inst)
		attributes[self.params[TupleComponents.ruin]] = str(self.ruin)
		attributes[self.params[TupleComponents.ruir]] = str(self.ruir)
		attributes[self.params[TupleComponents.rT]] = str(self.time_relation)
		attributes[self.params[TupleComponents.tr]] = str(self.time)
		return attributes

#TODO Figure out the type of code
class NtoCTuple(RtTuple):
	"""Tuple type that annotates a non-repeatable portion of reality with a "concept" code from a
		concept-based system"""
	#NtoC#< ‘+’/‘-’, r, RUIcs, RUIp, code, rT, tr >

	tuple_type = TupleType.NtoC
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.polarity, TupleComponents.r, TupleComponents.ruics, 
											   TupleComponents.ruip, TupleComponents.code, TupleComponents.rT, TupleComponents.tr})}
	
	def __init__(self, ruit: Rui, polarity: bool, r: str, ruics: Rui, ruip: Rui, code, rT, tr: str):
		#TODO Add rT
		super().__init__(ruit)
		self.polarity = polarity
		self.reason = r
		self.ruics = ruics
		self.ruip = ruip
		self.code = code
		self.time_relation = rT
		self.time = tr

	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.polarity]] = str(self.polarity)
		attributes[self.params[TupleComponents.r]] = str(self.reason)
		attributes[self.params[TupleComponents.ruics]] = str(self.ruics)
		attributes[self.params[TupleComponents.ruip]] = str(self.ruip)
		attributes[self.params[TupleComponents.code]] = str(self.code)
		attributes[self.params[TupleComponents.tr]] = str(self.time_relation)
		attributes[self.params[TupleComponents.t]] = str(self.time)
		return attributes

# We use NtoDE instead of NtoI, and we use an instance for the identifying descriptor
# or IdD associated with:
#	(1) and NtoRTuple tuple that says what type of IdD it is, 
#	(2) an NtoNTuple tuple to relate the name to what the IdD denotes, and 
#	(3) an NtoDE tuple to hold the actual written (or "string") form of the IdD. 
# Note that an IdD can be a name, identifier, etc.
#TODO Figure out if data should be a string or generic data
class NtoDETuple(RtTuple):
	#NtoDE#< '+/-', r, ruin, ruins, data, ruidt >

	tuple_type = TupleType.NtoDE
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.polarity, TupleComponents.ruin, 
											   TupleComponents.ruins, TupleComponents.data, TupleComponents.ruidt})}

	def __init__(self, ruit: Rui, polarity: bool, ruin: Rui, ruins: Rui, data, ruidt: Rui):
		super().__init__(ruit)
		self.polarity = polarity
		self.ruin = ruin
		self.ruins = ruins
		self.data = data
		self.ruidt = ruidt
	0
	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.polarity]] = str(self.polarity)
		attributes[self.params[TupleComponents.ruin]] = str(self.ruin)
		attributes[self.params[TupleComponents.ruins]] = str(self.ruins)
		attributes[self.params[TupleComponents.data]] = str(self.data)
		attributes[self.params[TupleComponents.ruidt]] = str(self.ruidt)
		return attributes

class NtoLackRTuple(RtTuple):
	"""Tuple type that asserts that for all instances of a given type, a specific
		non-repeatable portion of reality is not related to any of them by a 
		given relation"""
	#NtoRTuple(-) -tuple NtoRTuple(-)#< r, RUIp, RUIr, rT/‘-’, tr/‘-’ >

	tuple_type = TupleType.NtoLackR
	params = {**RtTuple.params, **enum_to_dict({TupleComponents.r, TupleComponents.ruip, 
													  TupleComponents.ruir, TupleComponents.rT, TupleComponents.tr})}
	

	def __init__(self, ruit: Rui, r: str, ruip: Rui, ruir: Rui, rT, tr: str):
		super()._init__(self, ruit)
		#TODO Add rT
		self.relation = r
		self.ruip = ruip
		self.ruir = ruir
		self.time_relation = rT
		self.time = tr 

	def get_str_attributes(self):
		"""Get the attributes of this tuple as a string"""
		attributes = super().get_str_attributes()
		attributes[self.params[TupleComponents.r]] = str(self.relation)
		attributes[self.params[TupleComponents.ruip]] = str(self.ruip)
		attributes[self.params[TupleComponents.ruir]] = str(self.ruir)
		attributes[self.params[TupleComponents.rT]] = str(self.time_relation)
		attributes[self.params[TupleComponents.tr]] = str(self.time)
		return attributes
	
"""Mapping from tuple id to the corresponding tuple class"""
type_to_class = {
	TupleType.A: ATuple,
	TupleType.D: DTuple,
	TupleType.F: FTuple,
	TupleType.NtoDE: NtoDETuple,
	TupleType.NtoNTuple: NtoNTuple,
	TupleType.NtoRTuple: NtoRTuple,
	TupleType.NtoC: NtoCTuple,
	TupleType.NtoLackR: NtoLackRTuple,
}
