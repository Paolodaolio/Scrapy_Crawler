class Club:

    def __init__(self, id, name ):
        self.name = name
        self.id = id

    def __eq__(self, o):
        if type(self) == type(o):
            return self.id == o
        return False

