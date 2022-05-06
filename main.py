from solver.runner.main_runner import run

if __name__ == "__main__":

    # Time limit per test case (in seconds).
    time_limit = 0.5

    # Search algorithm to be used:
    # All search algorithms will use the same set of invented tokens
    #   - Brute     Brute
    #   - AS        AStar
    #   - MH        Metropolis Hasting
    #   - LNS       Large Neighborhood Search
    #   - MCTS      Monte Carlo Tree Search
    #   - GP        Genetic Programming
    algorithm = "MCTS"

    # Problem domain:
    #   - R         Robot planning
    #   - S         String transformations
    #   - P         Drawing ASCII pixel art
    domain = "S"

    # Search heuristic/distance:
    # A cost measure used by the search algorithm to guide its search.
    #   - E         Entailment          cost = 0 if case solved else 1
    #   - G         Greedy              domain specific greedy heuristic
    #   - O         Optimized           domain specific optimized heuristic
    heuristic = "O"

    # Runs all test cases for this number of trials.
    # The more trials, the longer it takes to run.
    # Note: robots and pixels run way faster than strings
    number_of_trials = 1

    run(time_limit, algorithm, domain, heuristic, number_of_trials)
