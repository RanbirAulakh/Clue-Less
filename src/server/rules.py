class Rules:
#Will fill out the rules as we set up more in the player and map classes to determine
#what needs to be passed in to the rule methods.
	def moveValid(startRoom, endRoom):
		connectionlist = startRoom.getConnections()
		for connection in connectionlist):
			if connection.name == endRoom.name:
				return True
		return False
		
	def rule2():
		return False
		
	def rule3():
		return 2 == 2 ** 1
