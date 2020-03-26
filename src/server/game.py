class Game:
    id = ""
    visibility = True
    created_by = ""
    private_key = ""

    def __init__(self, id, visibility, created_by, private_key=""):
        self.id = id
        self.visibility = visibility
        self.created_by = created_by
        self.private_key = private_key
    
    def game_model(self):
        # responible for handling PLAYERS, RULES, ETC
        pass
    
