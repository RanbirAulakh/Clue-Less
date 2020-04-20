#Will fill out the rules as we set up more in the player and map classes to determine
#what needs to be passed in to the rule methods.
def move_valid(start_room, end_room):
	connection_list = start_room.get_connections()
	for connection in connection_list):
		if connection.name == end_room.name:
			return True
	return False
		
def rule2():
	return False
		
def rule3():
	return 2 == 2 ** 1
