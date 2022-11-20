from uuid6 import uuid7
from datetime import datetime, timezone

import sys
  
# append the path of the
# parent directory
sys.path.append(".")

from ids_codes import Rui

class Atuple:
	
	def __init__(self, ruip, ruia=Rui.Rui('A'), ruit=Rui.Rui('A'), unique="+SU", ar='A', t=datetime.now(timezone.utc)):
		self.ruit = ruit
		self.ruip = ruip
		self.ruia = ruia
		self.unique = unique
		self.ar = 'A'
		self.t = t

	def get_ruit(self):
		return self.ruit

	def get_ruip(self):
		return self.ruip 

	def get_ruia(self):
		return self.ruia 

	def get_t(self):
		return self.t
