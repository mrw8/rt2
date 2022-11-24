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


class NtoXGenericTuple(RtTuple):
	def __init__(self, ruit, ruin):
		super().__init__(ruit)
		if ruin is None:
			raise Exception("must provide a value for RUIn")
		else:
			self.ruin = ruin


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


