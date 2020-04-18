# team: The Plum Professors
# author: Ranbir Aulakh, Michael Knatz, Victoria Palaoro, Parth Jalundhwala
# description:

from .room import Room

from . import constants

class Map :
	def __init__(self):
		self.rooms = []
		setupRooms()

	def setupRooms():
		SLHallway = Hallway(S-Li)
		LiCHallway = Hallway(Li-C)
		CBaHallway = Hallway(C-Ba)
		BaKHallway = Hallway(Ba-K)
		DKHallway = Hallway(D-K)
		DLoHallway = Hallway(D-Lo)
		HLoHallway = Hallway(H-Lo)
		BaBiHallway = Hallway(Ba-Bi)
		LiBiHallway = Hallway(Li-Bi)
		BiDHallway = Hallway(Bi-D)
		HBiHallway = Hallway(H-Bi)
		SHHallway = Hallway(S-H)
		Study = Room(Study)
		Hall = Room(Hall)
		Library = Room(Library)
		Lounge = Room(Lounge)
		DiningRoom = Room(DiningRoom)
		Kitchen = Room(Kitchen)
		Ballroom = Room(Ballroom)
		Conservatory = Room(Conservatory)
		BilliardRoom = Room(BilliardRoom)
		SLHallway.setConnections(Study)
		SLHallway.setConnections(Library)
		LiCHallway.setConnections(Library)
		LiCHallway.setConnections(Conservatory)
		CBaHallway.setConnections(Conservatory)
		CBaHallway.setConnections(Ballroom)
		BaKHallway.setConnections(Ballroom)
		BaKHallway.setConnections(Kitchen)
		DKHallway.setConnections(Kitchen)
		DKHallway.setConnections(DiningRoom)
		DLoHallway.setConnections(DiningRoom)
		DLoHallway.setConnections(Lounge)
		HLoHallway.setConnections(Hall)
		HLoHallway.setConnections(Lounge)
		BaBiHallway.setConnections(Ballroom)
		BaBiHallway.setConnections(BilliardRoom)
		LiBiHallway.setConnections(Library)
		LiBiHallway.setConnections(BilliardRoom)
		BiDHallway.setConnections(BilliardRoom)
		BiDHallway.setConnections(DiningRoom)
		HBiHallway.setConnections(Hall)
		HBiHallway.setConnections(BilliardRoom)
		SHHallway.setConnections(Study)
		SHHallway.setConnections(Hall)
		Study.setConnections(SLHallway)
		Study.setConnections(SHHallway)
		Study.setConnections(BilliardRoom)
		Hall.setConnections(SHHallway)
		Hall.setConnections(HBiHallway)
		Hall.setConnections(HLoHallway)
		Lounge.setConnections(BilliardRoom)
		Lounge.setConnections(HLoHallway)
		Lounge.setConnections(DLoHallway)
		Library.setConnections(SLHallway)
		Library.setConnections(LiBiHallway)
		Library.setConnections(LiCHallway)
		BilliardRoom.setConnections(LiBiHallway)
		BilliardRoom.setConnections(BaBiHallway)
		BilliardRoom.setConnections(BiDHallway)
		BilliardRoom.setConnections(HBiHallway)
		DiningRoom.setConnections(BiDHallway)
		DiningRoom.setConnections(DKHallway)
		DiningRoom.setConnections(DLoHallway)
		Conservatory.setConnections(LiCHallway)
		Conservatory.setConnections(BilliardRoom)
		Conservatory.setConnections(CBaHallway)
		Ballroom.setConnections(CBaHallway)
		Ballroom.setConnections(BaBiHallway)
		Ballroom.setConnections(BaKHallway)
		Kitchen.setConnections(BaKHallway)
		Kitchen.setConnections(BilliardRoom)
		Kitchen.setConnections(DKHallway)
		self.rooms = [SLHallway, LiCHallway,CBaHallway, BaKHallway,DKHallway,DLoHallway,HLoHallway,BilliardRoom,BaBiHallway,LiBiHallway,BiDHallway,HBiHallway,SHHallway,Study,Hall,Kitchen,Ballroom,Conservatory,Library,Lounge,DiningRoom,]
