import os
import sys
import time

from solver.runner.algorithms import dicts
from solver.runner.runner import Runner


def run(alg, dom, dis):
    suffix = "-HPC"

    time_limit_sec = 60

    algorithm = ["Brute", "AS", "MCTS", "LNS", "MH", "GP"][alg]
    domain = ["S", "R", "P"][dom]
    distance = ["E", "G", "O"][dis]

    #run_time = time.time()
    Runner(dicts(0), algorithm, "{}{}".format(domain, distance), "eval", time_limit_sec, False, True, suffix).run()
    #run_time = time.time() - run_time

    #print("{}: {} (±{}) in {}s".format(algorithm, (mean*100).__round__(1), (std*100).__round__(1), run_time.__round__(1)))


if __name__ == "__main__":
    algorithm = int(sys.argv[1])
    domain = int(sys.argv[2])
    distance = int(sys.argv[3])

    run(algorithm, domain, distance)
