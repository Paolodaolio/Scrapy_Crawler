from classes.runner import Runner
from metrics import *
from database.manager import finished, random_name

def metrics_tab(runner1:Runner, runner2:Runner):
    print("jaccard : {} \t idf : {} \t adamic : {} \t psim_q : {}".format(
        jaccard_index(runner1.races, runner2.races),
        idf_similarity(runner1.races, runner2.races),
        adamic_similarity(runner1.races, runner2.races),
        psim_q(runner1.races, runner2.races)
    ))

def input_name():
    runner = None
    while runner is None:
        name = input("Input a runner name : ")
        try:
            runner = Runner(name)
        except NameError:
            print("Invalid name")
            runner = None
    return runner

def random_runner():
    return Runner(random_name())

def random_linked_runners(threshold):
    while True:
        runner1 = random_runner()
        runner2 = random_runner()
        if linked(jaccard_index, threshold, runner1, runner2):
            print("[+] Found Matching Couple :")
            print("--- {} from clubs {}".format(runner1.name, runner1.clubs))
            print("--- {} from clubs {}".format(runner2.name, runner2.clubs))


def main():
    threshold = float(input("Threshold : "))
    random_linked_runners(threshold)
    finished()


main()

