import csv
from Database.manager import fetch_races_by_runner, fetch_runner_by_name

class Runner:

    def __init__(self,name):
        self.name = name.upper()
        self.id = fetch_runner_by_name(self.name)
        if self.id is not None:
            self.races = fetch_races_by_runner(self.id)
        else:
            raise NameError("No runner with name " + self.name)


    def to_csv(self):
        with open(str(self.name)+'.csv', 'a', newline='', encoding='utf-8') as file:
            for race in self.races:
                write = csv.writer(file)
                write.writerow(race.to_csv())

    def __str__(self):
        return self.name