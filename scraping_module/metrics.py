from classes import Race, Runner
from math import log, sqrt


# Main function to infer social link
def linked(metric, threshold, runner1:Runner, runner2:Runner):
    race_set1 = race_set(runner1)
    race_set2 = race_set(runner2)
    if metric(race_set1, race_set2) > threshold:
        return True
    else:
        return False

### Parameters ###

def race_set(runner:Runner):
    #TODO
    return

def intersection(race_set1, race_set2):
    return [race for race in race_set1 if race in race_set2]

def union(race_set1, race_set2):
    res = race_set1[:]
    for race in race_set2:
        if race not in res:
            res.append(race)
    return res

def rarity(race:Race):
    return race.partecipants

def idf(race:Race):
    return 1 / log(race.partecipants)

### Metrics ###

def jaccard_index(race_set1, race_set2):
    intersection_cardinal = len(intersection(race_set1, race_set2))
    union_cardinal = len(union(race_set1, race_set2))
    return intersection_cardinal / union_cardinal

def idf_similarity(race_set1, race_set2):
    idf_set1 = [idf(race) for race in race_set1]
    idf_set2 = [idf(race) for race in race_set2]
    idf_dict = dict(zip(race_set1 + race_set2, idf_set1 + idf_set2))
    intersection_sum = sum([idf_dict[race] ** 2 for race in intersection(race_set1, race_set2)])
    sum1 = sum([idf ** 2 for idf in idf_set1])
    sum2 = sum([idf ** 2 for idf in idf_set2])
    return intersection_sum / (sqrt(sum1) * sqrt(sum2))

def adamic_similarity(race_set1, race_set2):
    return sum([idf(race) for race in intersection(race_set1, race_set2)])

def psim_q(race_set1, race_set2, q=3):
    return sum([1 / rarity(race) ** q for race in intersection(race_set1, race_set2)])