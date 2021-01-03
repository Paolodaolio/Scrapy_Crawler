from Classes.runner import Runner
from metrics import *

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

def main():
    runner1 = input_name()
    runner2 = input_name()
    metrics_tab(runner1, runner2)

main()

