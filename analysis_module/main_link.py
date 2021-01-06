from os import fpathconf
import matplotlib.pyplot as plt
import numpy as np
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

def metric_evaluation(samples, metrics, threshold):
    true_positive = [0] * len(metrics)
    true_negative = [0] * len(metrics)
    false_positive = [0] * len(metrics)
    false_negative = [0] * len(metrics)
    for _ in range(samples):
        runner1 = random_runner()
        runner2 = random_runner()
        same_club = runner1.same_club(runner2)
        for i, metric in enumerate(metrics):
            if linked(metric, threshold, runner1, runner2):
                if same_club:
                    true_positive[i] += 1
                else:
                    false_positive[i] +=1
            else:
                if same_club:
                    false_negative[i] += 1
                else:
                    true_negative[i] += 1
    TPR = [tp / (tp + fn) if tp > 0 else 0 for tp, fn in zip(true_positive, false_negative)]
    FPR = [fp / (fp + tn) if fp > 0 else 0 for fp, tn in zip(false_positive, true_negative)]
    return TPR, FPR


def main():
    samples = 1000
    thresholds = np.linspace(0, 2, num=100)
    metrics = [jaccard_index, idf_similarity, adamic_similarity, psim_q]
    jaccard_TPR = []
    jaccard_FPR = []
    idf_TPR = []
    idf_FPR = []
    adamic_TPR = []
    adamic_FPR = []
    psim_TPR = []
    psim_FPR = []

    for threshold in thresholds:
        print("[+] Completed {}%".format(int(threshold*100/2)))
        TPR, FPR = metric_evaluation(samples, metrics, threshold)
        jaccard_TPR.append(TPR[0])
        jaccard_FPR.append(FPR[0])
        idf_TPR.append(TPR[1])
        idf_FPR.append(FPR[1])
        adamic_TPR.append(TPR[2])
        adamic_FPR.append(FPR[2])
        psim_TPR.append(TPR[3])
        psim_FPR.append(FPR[3])
    
    plt.plot(thresholds, jaccard_TPR, label = "jaccard TPR")
    plt.plot(thresholds, jaccard_FPR, label = "jaccard FPR")
    plt.plot(thresholds, idf_TPR, label = "idf TPR")
    plt.plot(thresholds, idf_FPR, label = "idf FPR")
    plt.plot(thresholds, adamic_TPR, label = "adamic TPR")
    plt.plot(thresholds, adamic_FPR, label = "adamic FPR")
    plt.plot(thresholds, psim_TPR, label = "psim TPR")
    plt.plot(thresholds, psim_FPR, label = "psim FPR")

    plt.legend()
    plt.show()

    finished()


main()

