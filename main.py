from typing import List
from evaluation.experiment_procedure import *
from example_parser.string_parser import StringParser
from search.MCTS.mcts import MCTS
from search.a_star.a_star import AStar
from search.abstract_search import SearchAlgorithm
from search.gen_prog.vanilla_GP import VanillaGP
from search.metropolis_hastings.metropolis import MetropolisHasting
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN
from search.batch_run import BatchRun
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN

if __name__ == "__main__":
    result = BatchRun(
        # Task domain
        domain="robot",

        # Iterables for files name. Use [] to use all values.
        # This runs all files adhering to format "2-*-[0 -> 10]"
        # Thus, ([], [], []) runs all files for a domain.
        files=([], [], []),

        # Search algorithm to be used
        search_algorithm=RemoveNInsertN(),

        # Prints out result when a test case is finished
        print_results=True,

        # Use multi core processing
        multi_core=True,
    ).run()

    """
    searchAlgos : List[Type[SearchAlgorithm]] = [
        [MetropolisHasting, "metro"],
        [Brute, "brute"],
        [MCTS, "mcts"],
        [VanillaGP, "gp"],
        [RemoveNInsertN, "VLNS"],
        [AStar, "Astar"]
    ]

    results = []
    for alg in searchAlgos:
        experiment: Experiment = RobotParser().parse_specific_range(
            range(1, 3), range(0, 10), range(0, 10))
        (ave_suc, ave_time, com_suc) = test_performance_single_experiment(
            experiment, alg[0])
        results.append((alg[1], com_suc))

    for res in results:
        print(res[0], res[1])
    """