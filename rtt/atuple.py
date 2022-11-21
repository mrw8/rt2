from uuid6 import uuid7
from datetime import datetime, timezone

import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Rui

class RtTuple:
	def __init__(self, ruit):
		if ruit is None:
			self.ruit = Rui.Rui('A')
		else:	
			self.ruit = ruit

	def get_ruit(self):
		return self.ruit 

class Atuple(RtTuple):
	"""Referent Tracking assignment tuple that registers assignment of an RUI to a PoR"""
	def __init__(self, ruip=None, ruia=None, ruit=None, unique=None, ar=None, t=None):
		super().__init__(ruit)

		if ar is None:
			self.ar = 'A'
		else:
			self.ar = ar

		if ruip is None: 
			self.ruip = Rui.Rui(self.ar)
		else:
			self.ruip = ruip 
		
		if ruia is None:
			self.ruia = Rui.Rui('A')
		else:
			self.ruia = ruia

		if unique is None:
			self.unique = "-SU"
		else:
			self.unique = unique
		
		if t is None:
			self.t = datetime.now(timezone.utc)
		else:
			self.t = t

	def get_ruit(self):
		return self.ruit

	def get_ruip(self):
		return self.ruip 

	def get_ruia(self):
		return self.ruia 

	def get_t(self):
		return self.t

	def get_su_status(self):
		return self.unique

class NtoXGenericTuple(RtTuple):
	def __init__(self, ruit, ruin):
		super().__init__(ruit)
		if ruin is None:
			raise Exception("must provide a value for RUIn")
		else:
			self.ruin = ruin

	def get_rui_n(self):
		return self.ruin 

class NtoXTuple(NtoXGenericTuple):
	def __init(self, ruit, ruin, polarity):
		super().__init__(ruit, ruin)
		if (polarity):
			self.polarity = True
		else:
			self.polarity = False

	def isPositive(self):
		return self.polarity

	def isNegated(self):
		return not self.polarity


