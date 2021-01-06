import csv
from database.manager import fetch_runner_by_name, fetch_races_by_runner, fetch_club_by_runner

class Runner:

    def __init__(self,name):
        self.name = name.upper()
        self.id = fetch_runner_by_name(self.name)
        if self.id is not None:
            self.races = fetch_races_by_runner(self.id)
            self.clubs = fetch_club_by_runner(self.id)
        else:
            raise NameError("No runner with name " + self.name)


    def to_csv(self):
        with open(str(self.name)+'.csv', 'a', newline='', encoding='utf-8') as file:
            for race in self.races:
                write = csv.writer(file)
                write.writerow(race.to_csv())

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)