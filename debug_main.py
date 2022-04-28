import time

from solver.runner.algorithms import dicts
from solver.runner.runner import Runner

if __name__ == "__main__":
    # Time limit per test case (in seconds).
    time_limit = 1

    # Search algorithm to be used:
    # All search algorithms will use the same set of invented tokens
    #   - Brute     Brute
    #   - AS        AStar
    #   - MH        Metropolis Hasting
    #   - LNS       Large Neighborhood Search
    #   - MCTS      Monte Carlo Tree Search
    #   - GP        Genetic Programming
    algorithm = "AS"

    # Problem domain:
    #   - R         Robot planning
    #   - S         String transformations
    #   - P         Drawing ASCII pixel art
    domain = "P"

    # Search heuristic/distance:
    # A cost measure used by the search algorithm to guide its search.
    #   - E         Entailment          cost = 0 if case solved else 1
    #   - G         Greedy              domain specific greedy heuristic
    #   - O         Optimized           domain specific optimized heuristic
    heuristic = "O"

    # Setting test cases:
    #   1. Open solver/runner/algorithms.py
    #   2. In the dictionary in the function dicts find "test_cases".
    #   3. Under "test_cases" find "debug"
    #   4. There is a tuple for every domain; (complexities, tasks, trials)
    #   5. Every combination of items in the lists are run
    #   6. Complexities and tasks can be an empty list [], to run all


    run_time = time.time()
    mean = Runner(dicts(0), algorithm, "{}{}".format(domain, heuristic), "debug", time_limit, True, False).run()
    run_time = time.time() - run_time

    print("{}: {} in {}s".format(algorithm, (mean * 100).__round__(1), run_time.__round__(1)))
