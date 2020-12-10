import csv

class Race:
    def __init__(self, position,time,runner,level,club,race,date):
        self.position = position
        self.time = time
        self.runner = runner
        self.level = level
        self.club = club
        self.race = race
        self.date = date

    def to_csv(self):
        list = []
        list.append(self.position)
        list.append(self.time)
        list.append(self.runner)
        list.append(self.level)
        list.append(self.club)
        list.append(self.race)
        list.append(self.date)
        return list



class Runner:
    races = []
    def __init__(self,name):
        self.name = name.upper()

    def append_races(self, races):
        for race in races:
            if race.runner == self.name:
                self.races.append(race)

    def to_csv(self):
        with open(str(self.name)+'.csv', 'a', newline='') as file:
            for race in self.races:
                write = csv.writer(file)
                write.writerow(race.to_csv())
