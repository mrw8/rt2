from uuid6 import uuid7, UUID
from datetime import datetime, timezone
import logging
import enum

class Rui:
	"""Referent Unique Identifier

	Attributes:
	status -- the current status of the Rui
	uuid -- the unique identifier of the Rui
	"""

	def __init__(self, uuid: UUID = uuid7()):
		self._uuid = uuid

	@property
	def uuid(self):
		return self._uuid
	
	@uuid.setter
	def uuid(self, uuid):
		self._uuid = uuid

	def __str__(self):
		return str(self._uuid)


# class TempRefStatus(enum.Enum):
# 	 = 'U'
# 	 = 'C'
# 	 = ''

class TempRef:
	"""Temporal Reference
	
	Attributes:
	cal -- 
	uuid -- 
	"""

	def __init__(self, tr, ref_type: str=''):
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
		return self.cal

	def isUuid(self):
		return self.uuid
