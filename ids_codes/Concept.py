class Concept:
	
	"""concept based system concept code"""
	def __init__(self, code, cs_rui, any_name=""):
		self.code = code
		self.cs_rui = cs_rui
		self.name = any_name

	def get_c_code(self):
		return self.code

	def get_cs_rui(self):
		return self.cs_rui

	def get_name(self):
		return self.name


class Attribute:

	"""concept based system attribute or relationship"""
	def __init__(self, r, cs_rui, any_name=""):
		self.r = r 
		self.cs_rui = cs_rui
		self.name = any_name

	def get_r_code(self):
		return self.r 

	def get_cs_rui(self):
		return self.cs_rui

	def get_name(self):
		return self.name