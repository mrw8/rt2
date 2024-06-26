from datetime import datetime, timezone
from src.ids_codes import Rui
from src import rttuple

class Dtuple(atuple.RtTuple):

	# D#< RUId, RUIT, t, ‘I’/E, R, S >
	def __init__(self, ruit, ruid, event, event_reason, error, td=None, replacements=None):
		super().__init__(ruit)
		self.ruid = ruid
		self.event = event
		self.event_reason = event_reason
		self.error = error
		if td is None:
			self.td = datetime.now(timezone.utc)
		else:
			self.td = td
		if replacements is None:
			self.replacements = replacements
		else:
			self.replacements = replacements.copy()

class Ftuple(atuple.RtTuple):
	#F#< RUId, ta, RUIa, RUIT, C >
	def __init__(self, ruitn, ruia, ta, C, ruit=None):
		super().__init__(ruit)
		# ruitn denotes the tuple that this Ftuple is about
		self.ruitn = ruitn
		self.ruia = ruia
		#TO DO - we need to figure out how to do time parameters
		self.ta = ta
		self.C = C

