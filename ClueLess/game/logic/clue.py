"""
Plum Professors
Ranbir, Victoria, Parth, Michael
"""
class Clue:

	def __init__(self, name, type):
		self.name = name
		self.type = type
		
	"""
	Actual name (Ballroom/Prof. Plum/Lead Pipe)
	"""
	def get_clue_name(self):
		return self.name
	"""
	Weapon/Person/Location
	"""
	def get_clue_type(self):
		return self.type
		
# For target, add image to init?