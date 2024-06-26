from uuid6 import uuid7, UUID
from datetime import datetime, timezone
import logging
import enum


"""Enum representing RUI statuses"""
class RuiStatus(enum.Enum):
	assigned = 'A'
	reserved = 'R'

class Rui:
	"""Referent Unique Identifier

	Attributes:
	uuid -- the unique identifier of the RUI
	status -- The current status of the RUI
	"""

	def __init__(self, status: RuiStatus, uuid: UUID = uuid7()):
		self.uuid = uuid
		self.status = status

	def is_assigned(self):
		return self.status is RuiStatus.assigned

	def is_reserved(self): 
		return self.status is RuiStatus.reserved

	def update_status_assigned(self):
		if self.status is RuiStatus.assigned:
			logging.warning("status of Rui instance is already assigned. No change.")
		else:
			self.status = RuiStatus(RuiStatus.assigned)


# class TempRefStatus(enum.Enum):
# 	 = 'U'
# 	 = 'C'
# 	 = ''

class TempRef:
	"""Temporal Reference"""

	def __init__(self, tr, ref_type:str=''):
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

	def isCalendar(self):
		return (self.cal != None)

	def isUuid(self):
		return (self.uuid != None)
