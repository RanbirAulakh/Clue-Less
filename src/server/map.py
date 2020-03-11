class Map:
    mapGrid = [][]
    def __init__(self, players):
        self.players = players
		self.setupMap()

    def movePlayer(self, player, move):
        room = self.mapGrid[player.x][player.y]
        self.checkRules(player, room, move)

    def checkRules(player, room, move):
        Rules.rule1()

	def setupMap():
		mapGrid.append("")