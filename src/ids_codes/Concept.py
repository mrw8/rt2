class Concept:
	
	"""concept based system concept code"""
	def __init__(self, code, cs_rui, any_name=""):
		self.code = code
		self.cs_rui = cs_rui
		self.name = any_name


class Attribute:

	"""concept based system attribute or relationship"""
	def __init__(self, r, cs_rui, any_name=""):
		self.r = r 
		self.cs_rui = cs_rui
		self.name = any_name
