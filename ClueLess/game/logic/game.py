# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro
# description:

# import constants
import logging
from . import constants
import random
from .player import Player
from .room import *
from .clue import Clue
from .map import Map


class Game:
	def __init__(self):
		self.turn_order = []
		self.current_turn = None
		self.dead_players = []

		self.available_characters = ["Professor Plum", "Colonel Mustard", "Mr. Green", "Mrs. White", "Ms. Scarlet", "Mrs. Peacock"]

		self.players = []
		self.inactive_players = []  # inactive characters
		self.murder = []

		self.status = "Not Started"

		"""
		TODO Random characters for each player or initialize the players out of initial game?
		"""
		# create decks of the different clue types
		suspects = self.create_suspect_deck(constants.SUSPECTS)
		weapons = self.create_weapons_deck(constants.WEAPONS)
		rooms = self.create_rooms_deck(constants.ROOMS)

		# draw 1 from each and store it as the murder you are solving
		self.create_murder(suspects, rooms, weapons)

		# combine the decks then deal to the players)
		self.clue_deck = suspects + weapons + rooms
		random.shuffle(self.clue_deck)

		self.map = Map()
		self.is_move_made = False
		self.original_turn_order = []  # useful for suggestion

	def start_game(self):
		"""
		1. Change status to "Started"
		2. Deal Hands
		2. Adjust who goes first? Assuming if Scarlet wasn't selected
		3. If Users turn, unlock Users Buttons (Consumers.py)
		4. Check if Player.length is 4
		"""
		print("Game officially started!!")
		self.status = "Started"
		self.deal_hands()

		for i in self.available_characters:
			p = Player(i, None)
			p.character = i
			self.inactive_players.append(p)

		self.place_players()
		self.make_turn_order()

		for i in self.turn_order:
			self.original_turn_order.append(i.name)

	def add_player(self, player_name):
		"""
		Add player to the Game List
		:param player_name:
		:return:
		"""
		for i in self.players:
			if i.name == player_name:
				print("Player {0} already exist!".format(player_name))
				return

		p = Player(player_name, None)
		print("Adding {0} to the game.".format(p.name))
		self.players.append(p)

	def remove_player(self, player_name):
		"""
		Remove player from the list
		- If player hasn't choose the character
		-- Remove
		- If player has choose the character
		-- Do not remove
		-- TODO implement show cards to other members if PLAYER choose the card and LEFT.
		:param player_name:
		:return:
		"""
		for i in self.players:
			# if player left and haven't picked their character
			# then, we do not need to hold their spot (or cards)
			if i.name == player_name and i.character is None:
				print("Removing {0} from the game.".format(i.name))
				self.players.remove(i)
				break

	def player_select_character(self, player_name, chosen_character):
		"""
		Assign chosen character to player object
		- if chosen character has already been selected, alert user
		- once a player choose a character, remove character from available list
		:param player_name:
		:param chosen_character:
		:return: true if succeed
		"""
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				if chosen_character in self.available_characters:
					self.players[i].character = chosen_character
					self.available_characters.remove(chosen_character)
					return True
				else:
					return False

	def get_player_current_location(self, player_name):
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				return self.players[i].current_location

	def update_player_current_location(self, player_name, new_location):
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				self.players[i].current_location = new_location
				return self.players[i].current_location

	def get_locations(self):
		locations = {}

		for i in self.players:
			locations[i.name] = i.get_current_location()

		return locations

	def get_character_game_pieces(self):
		players_details = {}
		for i in self.players:
			players_details[i.name] = {"location": i.current_location, "character": i.character}

		return players_details

	def get_cards(self, player_name):
		for i in self.players:
			if i.name == player_name:
				return i.get_hand_str()

	def already_chosen(self, player_name):
		"""
		Check if player already choose a character
		:param player_name: username
		:return: true if succeed
		"""
		for i in self.players:
			if i.name == player_name:
				if i.character is not None:
					return True
				else:
					return False

	def get_chosen_character(self, player_name):
		for i in self.players:
			if i.name == player_name:
				if i.character is not None:
					return i.character
				else:
					print("Shouldn't reach here...")

	def create_suspect_deck(self, suspects):
		"""
		Create individual decks for the creation of the muder
		:param suspects:
		:return:
		"""
		clues = []
		for i in suspects:
			clues.append(Clue(i, "Suspect"))
		return clues 
		
	def create_weapons_deck(self, weapons):
		clues = []
		for i in weapons:
			clues.append(Clue(i, "Weapon"))
		return clues 
		
	def create_rooms_deck(self, rooms):
		clues = []
		for i in rooms:
			clues.append(Clue(i, "Room"))
		return clues

	def create_murder(self, suspect_clues, room_clues, weapon_clues):
		"""
		Shuffle and use the individual decks to put together the murder to be solved.
		:param suspect_clues:
		:param room_clues:
		:param weapon_clues:
		:return:
		"""
		self.murder = []
		random.shuffle(suspect_clues)
		random.shuffle(room_clues)
		random.shuffle(weapon_clues)
		self.murder.append(suspect_clues.pop())
		self.murder.append(room_clues.pop())
		self.murder.append(weapon_clues.pop())

		print("MURDER SUSPECT: {0} / ROOM: {1} / WEAPON: {2}".format(self.murder[0].name, self.murder[1].name, self.murder[2].name))
		
	def get_murder(self):
		return self.murder

	def deal_hands(self):
		"""
		Deal initial hands, and if a player leaves, place their hand in the "clue_deck" var
		and pass it to remaining players.
		"""
		num_players = len(self.players)
		rounds = 0
		while len(self.clue_deck) != 0:
			self.players[rounds % num_players].hand.append(self.clue_deck.pop())
			rounds += 1

	def get_map(self):
		return self.map
	
	def make_turn_order(self):
		chosen_characters = {}
		for player in self.players:
			chosen_characters[player.character] = player

		for i in constants.SUSPECTS:
			if i in chosen_characters.keys():
				print("Adding {0} to turn lst".format(chosen_characters[i]))
				self.turn_order.append(chosen_characters[i])

		self.current_turn = self.turn_order[0]

	def next_turn(self):
		self.is_move_made = False

		current_index = self.turn_order.index(self.current_turn)
		if current_index >= len(self.turn_order) - 1:
			current_index = 0
			self.current_turn = self.turn_order[current_index]
		else:
			current_index += 1
			self.current_turn = self.turn_order[current_index]

		for i in self.dead_players:
			if i in self.turn_order:
				self.turn_order.remove(i)

	def move_player(self, player_name, next_move):
		target_room = self.map.rooms[next_move]
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				start_room = self.players[i].get_room()

				if target_room in start_room.get_connections():
					print("Yes is in connections")
					if target_room.can_move():
						print("Uh yes?")
						start_room.remove_player(self.players[i])
						target_room.add_player(self.players[i])

						self.players[i].set_room(target_room)
						self.players[i].set_current_location(target_room.get_name())
						self.is_move_made = True
						return True
					else:
						print("nah")
						return False
				print("nah2")
				return False

	def make_guess(self, guessing_player, clues):
		data = {}  # this is a data that will be sent to Client (User)

		print("Guessing Player {0}".format(guessing_player))
		print("Clues Suggestion {0}".format(clues))

		player_suggesting = None
		for i in self.players:
			if i.name == guessing_player:
				player_suggesting = i
				break

		# Player is responsible for disapproving or disapproving cards
		player_approve = None

		# If Player received approved, it means player can show ONLY 1 card to a player that is making a suggestion
		player_show_one_card = None

		# determine if this player own this suspect (character) game piece
		is_inactive_character = True
		for player in self.players:
			if player.get_character() in clues['suspect']:
				is_inactive_character = False  # it means one of the active player owns this character

				print("Yes, {0} owns this character, {1}, and is in {2}.".format(player.name, player.character, player.current_location))

				# update room
				print("Removing {0} from {1}".format(player.name, player.current_location))
				self.map.rooms[player.current_location].remove_player(player)

				# move suggesting player to suggesting room
				print("Moving {0} to {1}".format(player.name, clues['room']))
				self.map.rooms[clues['room']].add_player(player)

				player.set_room(self.map.rooms[clues['room']])
				player.set_current_location(clues['room'])
				
				break

		# get next player to approve/disapprove
		current_index = self.original_turn_order.index(player_suggesting.name)
		while True:
			print("original_turn_order {0}".format(self.original_turn_order))
			if current_index >= len(self.original_turn_order) - 1:
				current_index = 0
				player_approve = self.original_turn_order[current_index]
			else:
				current_index += 1
				player_approve = self.original_turn_order[current_index]

			if player_approve != guessing_player:
				break

		data['player_suggester'] = guessing_player
		data['player_to_approve_disapprove'] = player_approve
		data['player_owner_cards'] = player_approve
		data['cards'] = self.get_cards(player_approve)

		return data
		
	def next_disapprover(self, guessing_player, current_disapprover):
		data={}
		player_approve = None
		current_index = self.original_turn_order.index(current_disapprover)
		while True:
			print("original_turn_order {0}".format(self.original_turn_order))
			if current_index >= len(self.original_turn_order) - 1:
				current_index = 0
				player_approve = self.original_turn_order[current_index]
			else:
				current_index += 1
				player_approve = self.original_turn_order[current_index]

			if player_approve != guessing_player:
				break
		data['player_suggester'] = guessing_player
		data['player_to_approve_disapprove'] = player_approve
		data['player_owner_cards'] = player_approve
		data['cards'] = self.get_cards(player_approve)
		
		return data

	def show_one_card_to_suggester(self):
		pass
	
	def make_accusation(self, player_name, accused_clues):
		clue_names = []

		p = None
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				p = self.players[i]

		for m in self.murder:
			clue_names.append(m.get_clue_name().lower().replace(" ", ""))

		for c in accused_clues:
			# if even one of the clues is not in the murder clues, player loses
			if c.lower() not in clue_names:
				self.dead_players.append(p)
				return False

		# if all of the passed in clues are in the murder clues, they win
		self.status = "Finished!"
		return True

	def place_players(self):
		"""
		At start, place the players in a starting hallway based on their character.
		:return:
		"""
		rooms = self.map.get_rooms()
		for player in self.players:
			character = player.get_character()
			
			if character == constants.SCARLET:
				rooms[constants.HALL_LOUNGE].add_player(player)
				player.set_room(rooms[constants.HALL_LOUNGE])
				player.set_current_location(constants.HALL_LOUNGE)
				
			elif character == constants.MUSTARD:
				rooms[constants.LOUNGE_DINING].add_player(player)
				player.set_room(rooms[constants.LOUNGE_DINING])
				player.set_current_location(constants.LOUNGE_DINING)
				
			elif character == constants.WHITE:
				rooms[constants.BALLROOM_KITCHEN].add_player(player)
				player.set_room(rooms[constants.BALLROOM_KITCHEN])
				player.set_current_location(constants.BALLROOM_KITCHEN)
				
			elif character == constants.GREEN:
				rooms[constants.CONSERVATORY_BALLROOM].add_player(player)
				player.set_room(rooms[constants.CONSERVATORY_BALLROOM])
				player.set_current_location(constants.CONSERVATORY_BALLROOM)
				
			elif character == constants.PEACOCK:
				rooms[constants.LIBRARY_CONSERVATORY].add_player(player)
				player.set_room(rooms[constants.LIBRARY_CONSERVATORY])
				player.set_current_location(constants.LIBRARY_CONSERVATORY)
				
			elif character == constants.PLUM:
				rooms[constants.STUDY_LIBRARY].add_player(player)
				player.set_room(rooms[constants.STUDY_LIBRARY])
				player.set_current_location(constants.STUDY_LIBRARY)

	def get_available_moves(self):
		"""
		Get connections of where player current sitting
		- Then check if connections are available for user to move
		:return:
		"""
		connections = self.current_turn.get_room().get_connections()
		lst = connections

		for p in self.players:
			print("Player sitting in {0}".format(p.get_room().name))
			if p.get_room() in lst:
				lst.remove(p.get_room())

		return_list_string = []

		for i in lst:
			return_list_string.append(i.get_name())

		return return_list_string

	def is_in_room(self, player_name):
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				if self.players[i].room.name in constants.ROOMS:
					return True
				else:
					return False
