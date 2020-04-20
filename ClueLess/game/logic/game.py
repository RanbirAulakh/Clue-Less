# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
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
		self.current_turn = None
		self.available_characters = ["Professor Plum", "Colonel Mustard", "Mr. Green", "Mrs. White", "Ms. Scarlet", "Mrs. Peacock"]

		self.players = []
		self.murder = []

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
		random.shuffle(suspects)
		self.clue_deck_suspects = suspects
		random.shuffle(rooms)
		self.clue_deck_rooms = rooms
		random.shuffle(weapons)
		self.clue_deck_weapons = weapons

		self.map = Map()

		# self.turn_order = self.make_turn_order(players) # TODO move to another function

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
					self.players[i].current_location = "HOLA"  # TODO default character location

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
			locations[i.name] = i.current_location

		return locations

	def get_cards(self, player_name):
		for i in self.players:
			if i.name == player_name:
				return i.hand

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

	# create individual decks for the creation of the muder
	def create_suspect_deck(self, suspects):
		clues=[]
		for i in suspects :
			clues.append(Clue(i, "Suspect"))
		return clues 
		
	def create_weapons_deck(self, weapons):
		clues=[]
		for i in weapons :
			clues.append(Clue(i, "Weapon"))
		return clues 
		
	def create_rooms_deck(self, rooms):
		clues=[]
		for i in rooms :
			clues.append(Clue(i, "Room"))
		return clues 
		
	# Shuffle and use the individual decks to put together the murder to be solved.
	def create_murder(self, suspect_clues, room_clues, weapon_clues):
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

	def deal_hands(self, player_name):
		"""
		Deal initial hands, and if a player leaves, place their hand in the "clue_deck" var
		and pass it to remaining players.
		"""
		for i in range(len(self.players)):
			if self.players[i].name == player_name:
				print(self.clue_deck_suspects)
				murder_card = self.clue_deck_suspects.pop()
				room_card = self.clue_deck_rooms.pop()
				weapon_card = self.clue_deck_weapons.pop()
				self.players[i].hand = {"suspect_card": murder_card.name, "room_card": room_card.name, "weapon_card": weapon_card.name}
				print("cards: {0}".format(self.players[i].hand))
				return self.players[i].hand

	def get_map(self):
		return self.map
	
	def make_turn_order(self, players) :
		turn_order = []
		for i in constants.SUSPECTS :
			for ii in players :
				if ii.get_character().lower() == i.lower() :
					turn_order.append(ii)
		return turn_order
		
	def get_turn_order(self) :
		return self.turn_order
		
	def move_player(self, player, target_room):
		start_room = player.get_room()
		if(target_room in start_room.get_connections()):
			if(target_room.can_move()):
				start_room.remove_player(player)
				target_room.add_player(player)
				return True
			else:
				return False
		return False
		
	#assuming the the clues are strings in this case. could make a map of the clues
	#and pull them by name to do exact compares.
	def make_guess(self, guessing_player, clues):
		for player in self.players :
			if(guessing_player != player):
				for c in player.get_hand() :
					if (c.get_clue_name().lower() in clues) :
						return c
		#No clues found in other players hands	
		return None
	
	def make_accusation(self, clues):
		murder = self.get_murder()
		clue_names = []
		for m in murder:
			clue_names.append(m.get_clue_name().lower())
		
		for c in clues :
			#if even one of the clues is not in the murder clues, player loses
			if(c.get_clue_name().lower() not in clue_names):
				return False
		#if all of the passed in clues are in the murder clues, they win
		return True
