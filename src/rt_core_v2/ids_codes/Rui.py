from uuid6 import uuid7, UUID
from datetime import datetime, timezone
import logging
import enum


class TempRefType(enum.Enum):
	calendar = 'C'
	id = 'U'

class Rui:
	"""Referent Unique Identifier
	A unique identifier for referent tracking

	Attributes:
	status -- the current status of the Rui
	uuid -- the unique identifier of the Rui
	"""

	def __init__(self, uuid: UUID=None):
		self._uuid = uuid if uuid else uuid7()

	@property
	def uuid(self):
		return self._uuid
	
	@uuid.setter
	def uuid(self, uuid):
		self._uuid = uuid

	def __str__(self):
		return str(self._uuid)

#TODO Figure out if the option should be a uuid or an RUI. Probably RUI
class TempRef:
	"""Temporal Reference
	A tuple component that contains is either a calendar date or a unique identifier that represents a instance or interval of time

	Attributes:
	type -- The type of identifier
	ref -- Identifier for the temporal reference
	"""
	def __init__(self, tr, ref_type: TempRefType=TempRefType.id):
		self.type = ref_type
		primary_timezone = timezone.utc
		if ref_type == TempRefType.calendar:
			self.ref = tr.astimezone(primary_timezone) if tr else datetime.now(primary_timezone)
		elif ref_type == TempRefType.id:
			self.ref = tr if tr else uuid7()
		else:
			logging.error("don't understand " + ref_type)
			raise Exception(ref_type + " is not a valid option")
	
	def __str__(self):
		return str(self.ref)
