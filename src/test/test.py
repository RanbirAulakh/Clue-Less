import sys
sys.path.append("../")
import server.constants as constants
from server.player import Player
from server.room import *
from server.clue import Clue

roomTest = Room("Room", [])
first = Player("Mike", constants.SCARLET)
second = Player("Victoria", constants.PLUM)
roomTest.addPlayer(first)
roomTest.addPlayer(second)
assert(first in roomTest.getPlayers())
assert(second in roomTest.getPlayers())
roomTest.removePlayer(first)

assert(first not in roomTest.getPlayers())
assert(second in roomTest.getPlayers())