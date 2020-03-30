
# TODO implement Property (python3)
# https://www.datacamp.com/community/tutorials/property-getters-setters

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
    
    def convert_to_json(self):
        return { "id": self.id, "visibility": self.visibility, "created_by": self.created_by, "key": self.private_key}
