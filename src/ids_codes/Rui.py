from uuid6 import uuid7, UUID
from datetime import datetime, timezone
import logging

class Rui:
	"""Referent Unique Identifier"""
	
	def setAssignedOrReserved(self, a_or_r):
		if (a_or_r == 'A' or a_or_r == 'R'):
			self.a_or_r = a_or_r
		else:
			raise Exception("a_or_r must be set to A (assigned) or R (reserved)")

	def __init__(self, uuid, a_or_r):
		self.uuid = uuid
		self.setAssignedOrReserved(a_or_r)

	def __init__(self, a_or_r):
		self.uuid = uuid7()
		self.setAssignedOrReserved(a_or_r)

	def is_assigned(self):
		return (self.a_or_r == 'A')

	def is_reserved(self): 
		return (self.a_or_r == 'R')

	def update_status_assigned(self):
		if (self.a_or_r == 'A'):
			logging.warning("status of Rui instance is already assigned. No change.")
		else:
			self.a_or_r = 'A'

class TempRef:
	"""Temporal Reference"""

	def __init__(self, tr, ref_type = None):
		if (isinstance(tr, datetime)):
			if tr.tzinfo != timezone.utc:
				tr = tr.astimezone(timezone.utc)
			self.cal = tr
			self.uuid = None
		elif (isinstance(tr, UUID)):
			self.uuid = tr
			self.cal = None
		elif (tr == None):
			if ref_type == 'U':
				self.uuid = uuid7()
				self.cal = None
			elif ref_type == 'C':
				self.uuid = None
				self.cal = datetime.now(timezone.utc)
			else:
				logging.error("don't understand " + ref_type)
				raise Exception(ref_type + " is not a valid option")
		else:
			raise Exception("temporal reference must be datatime or uuid")

	def isCalendar():
		return (self.cal != None)

	def isUuid():
		return (self.uuid != None)
