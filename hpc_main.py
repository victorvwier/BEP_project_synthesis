import os
import sys
import time

from solver.runner.algorithms import dicts
from solver.runner.runner import Runner


def run(alg, dom, dis):
    suffix = "-PC"

    time_limit_sec = 60

    algorithm = ["Brute", "AS", "MCTS", "LNS", "MH", "GP"][alg]
    domain = ["S", "R", "P"][dom]
    distance = ["E", "G", "O"][dis]

    #run_time = time.time()
    Runner(dicts(0), algorithm, "{}{}".format(domain, distance), "eval", time_limit_sec, False, True, suffix).run()
    #run_time = time.time() - run_time

    #print("{}: {} (±{}) in {}s".format(algorithm, (mean*100).__round__(1), (std*100).__round__(1), run_time.__round__(1)))


if __name__ == "__main__":
    # Setting test cases:
    #   1. Open solver/runner/algorithms.py
    #   2. In the dictionary in the function dicts find "test_cases".
    #   3. Under "test_cases" find "eval"
    #   4. There is a tuple for every domain; (complexities, tasks, trials)
    #   5. Every combination of items in the lists are run
    #   6. Complexities and tasks can be an empty list [], to run all

    algorithm = int(sys.argv[1])
    domain = int(sys.argv[2])
    distance = int(sys.argv[3])

    run(algorithm, domain, distance)
