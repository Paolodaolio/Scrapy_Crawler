class Race:

    def __init__(self, id, name, length, date, elevation, partecipants):
        self.id = int(id)
        self.name = str(name)
        self.elevation = float(elevation)
        self.date = str(date)
        self.partecipants = int(partecipants)
        self.length = float(length)

    def to_csv(self):
        list = []
        list.append(self.elevation)
        list.append(self.date)
        list.append(self.runner)
        list.append(self.name)
        list.append(self.lenght)
        return list
    
    def __str__(self):
        return "{} on {}".format(self.name, self.date)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else:
            return self.id == other.id
    
    def __hash__(self):
        return self.id