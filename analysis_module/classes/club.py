class Club:

    def __init__(self, id, name):
        self.name = name
        self.id = id

    def __eq__(self, o):
        if type(self) != type(o):
            return False
        return self.id == o.id
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

