import csv

class Race:
    def __init__(self, elevation,date,partecipants,level,club,name,lenght):
        self.elevation = elevation
        self.date = date
        self.partecipants = partecipants
        self.name = name
        self.lenght = lenght

    def to_csv(self):
        list = []
        list.append(self.elevation)
        list.append(self.date)
        list.append(self.runner)
        list.append(self.name)
        list.append(self.lenght)
        return list


class Runner:
    races = []
    id = None
    def __init__(self,name):
        self.name = name.upper()

    def append_races(self, races):
        for race in races:
            if race.runner == self.name:
                self.races.append(race)

    def to_csv(self):
        with open(str(self.name)+'.csv', 'a', newline='', encoding='utf-8') as file:
            for race in self.races:
                write = csv.writer(file)
                write.writerow(race.to_csv())

    def set_id(self, id):
        self.id = id

class Club:
    members=[]
    def __init__(self, name ):
        self.name = name

    def add_member(self, member):
        memeber.append(member)

    def fetch_members(self):
        return self.members

    def insert_list(self):
        output = ""
        for mem in self.members:
            output = str(output+","+mem)
        return output

