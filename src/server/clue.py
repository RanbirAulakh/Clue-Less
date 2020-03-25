class Clue:

	def __init__(self, name, type):
		self.name = name
		self.type = type
		
	"""
	Actual name (Ballroom/Prof. Plum/Lead Pipe)
	"""
	def getClueName(self):
		return self.name
	"""
	Weapon/Person/Location
	"""
	def getClueType(self):
		return self.type
		
# For target, add image to init?