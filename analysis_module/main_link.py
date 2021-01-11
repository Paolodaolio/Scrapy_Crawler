from classes.runner import Runner
from metrics import *
from database.manager import finished, potentially_linked_to_runner

def input_name():
    runner = None
    while runner is None:
        name = input("Input a runner name:\n >>> ")
        try:
            runner = Runner(name)
        except NameError:
            print("Invalid name")
            runner = None
    return runner

def metrics_vector(runner1:Runner, runner2:Runner):
    number_of_metrics = 4
    vector = [jaccard_index(runner1.races, runner2.races),
            idf_similarity(runner1.races, runner2.races),
            adamic_similarity(runner1.races, runner2.races),
            psim_q(runner1.races, runner2.races)]
    return  [sum(vector)/number_of_metrics] + vector

def metrics_matrix(runner:Runner):
    matrix = []
    names = potentially_linked_to_runner(runner.id)
    for name in names:
        current_runner = Runner(name)
        matrix.append(metrics_vector(runner, current_runner))
    return names, matrix

def display_metrics(names, matrix):
    loop = True
    while loop:
        print("Found {} potential linked runners.".format(len(matrix)))
        used_metric = int(input("Metric: Mean (0), Jaccard Index (1), IDF Similarity (2), Adamic Similarity (3), Psim-q (4)\n >>> "))
        number_of_entries = int(input("Number of entries:\n >>> "))
        current_names = sorted(names, key = lambda x : matrix[names.index(x)][used_metric], reverse=True)[:number_of_entries]
        current_values = sorted(matrix, key = lambda x : x[used_metric], reverse=True)[:number_of_entries]
        for name, values in zip(current_names, current_values):
            print("{:^30} || {:^.5f} | {:^.5f} {:^.5f} {:^.5f} {:^.5f}".format(name, values[0], values[1], values[2], values[3], values[4]))
        loop = input("Continue? (y/[n])\n >>>") == 'y'

def main():
    runner = input_name()
    names, matrix = metrics_matrix(runner)
    display_metrics(names, matrix)
    finished()

main()

