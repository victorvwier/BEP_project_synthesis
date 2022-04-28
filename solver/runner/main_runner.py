from solver.runner.algorithms import dicts
from solver.runner.runner import Runner

complexities = {
    "S": [1, 3, 5, 7, 9],
    "R": [2, 4, 8, 10],
    "P": [1, 2, 3, 4, 5]
}

complexity_name = {
    "S": "No. examples",
    "R": "Grid size",
    "P": "No. characters",
}

def run(time_limit, algo, domain, heuristic, number_of_trials):
    setting = "{}{}".format(domain, heuristic)

    dic = dicts(0)

    for complexity in complexities[domain]:
        dic["test_cases"]["all"][domain] = ([complexity], [], range(1, number_of_trials + 1))

        mean = Runner(dic, algo, setting, "all", time_limit, False, False).run()

        print("{} = {}".format(complexity_name[domain], complexity))
        print("Solved {}%".format((100*mean).__round__(1)))
        print("\n")
