class Race:

    def __init__(self, id, name, length, date, elevation, partecipants):
        self.id = int(id)
        self.name = str(name)
        self.elevation = elevation
        self.date = date
        self.partecipants = int(partecipants)
        self.length = length
    
    def __str__(self):
        return "{} on {}".format(self.name, self.date)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else:
            return self.id == other.id
    
    def __hash__(self):
        return self.id