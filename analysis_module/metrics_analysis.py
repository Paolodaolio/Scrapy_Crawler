import matplotlib.pyplot as plt
import numpy as np
from classes.runner import Runner
from metrics import *
from database.manager import finished, random_name, random_linked_names

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

def random_linked_runners():
    names = random_linked_names()
    return Runner(names[0]), Runner(names[1])

def metric_evaluation(samples, metrics, threshold):
    true_positive = [0] * len(metrics)
    true_negative = [0] * len(metrics)
    false_positive = [0] * len(metrics)
    false_negative = [0] * len(metrics)

    for _ in range(samples // 2): # Unlinked runners
        runner1 = random_runner()
        runner2 = random_runner()
        while runner1.same_club(runner2):
            runner1 = random_runner()
            runner2 = random_runner()
        for i, metric in enumerate(metrics):
            if linked(metric, threshold, runner1, runner2):
                    false_positive[i] += 1
            else:
                    true_negative[i] += 1

    for _ in range(samples // 2): # Linked runners
        runner1, runner2 = random_linked_runners()
        for i, metric in enumerate(metrics):
            if linked(metric, threshold, runner1, runner2):
                    true_positive[i] += 1
            else:
                    false_negative[i] += 1

    print("Threshold = {}".format(threshold))
    print(true_positive)
    print(true_negative)
    print(false_positive)
    print(false_negative)
    TPR = [tp / (tp + fn) if tp > 0 else 0 for tp, fn in zip(true_positive, false_negative)]
    FPR = [fp / (fp + tn) if fp > 0 else 0 for fp, tn in zip(false_positive, true_negative)]
    return TPR, FPR


def threshold_analysis():
    samples = 1000
    max_threshold = 1.5
    thresholds = np.linspace(0, max_threshold, num=300)
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
        print("[+] Completed {}%".format(int(threshold*100/max_threshold)))
        TPR, FPR = metric_evaluation(samples, metrics, threshold)
        jaccard_TPR.append(TPR[0])
        jaccard_FPR.append(FPR[0])
        idf_TPR.append(TPR[1])
        idf_FPR.append(FPR[1])
        adamic_TPR.append(TPR[2])
        adamic_FPR.append(FPR[2])
        psim_TPR.append(TPR[3])
        psim_FPR.append(FPR[3])
    
    plt.plot(thresholds, jaccard_TPR, label = "Jaccard TPR")
    plt.plot(thresholds, jaccard_FPR, label = "Jaccard FPR")
    plt.plot(thresholds, idf_TPR, label = "IDF TPR")
    plt.plot(thresholds, idf_FPR, label = "IDF FPR")
    plt.plot(thresholds, adamic_TPR, label = "Adamic TPR")
    plt.plot(thresholds, adamic_FPR, label = "Adamic FPR")
    plt.plot(thresholds, psim_TPR, label = "Psim-3 TPR")
    plt.plot(thresholds, psim_FPR, label = "Psim-3 FPR")

    plt.xlabel("threshold")
    plt.ylabel("probability")
    plt.legend()
    plt.show()

def main():
    threshold_analysis()
    finished()

main()

