from collections import defaultdict

from common.settings.pixel_entailment import PixelEntailment
from common.settings.pixel_hamming import PixelHamming
from common.settings.pixel_hamming_pointer_distance import PixelHammingPointerDistance
from common.settings.robot_entailment import RobotEntailment
from common.settings.robot_greedy import RobotGreedy
from common.settings.robot_optimized_steps import RobotOptimizedSteps
from common.settings.string_entailment import StringEntailment
from common.settings.string_levenshtein import StringLevenshtein
from common.settings.string_optimized_alignment import StringOptimizedAlignment
from solver.search.implementations.my_mcts.mcts import MCTS
from solver.search.implementations.a_star import AStar
from solver.search.implementations.brute import Brute
from solver.search.implementations.genetic_programming import GeneticProgramming
from solver.search.implementations.large_neighborhood_search import LNS
from solver.search.implementations.metropolis import MetropolisHasting


def dicts(param):
    return {
        "algorithms": {
            "Brute": defaultdict(Brute),
            "AS": {
                "SG": AStar(0.01),
                "SO": AStar(0.06),
                "SE": AStar(0.1),
                "RG": AStar(0.8),
                "RO": AStar(0),
                "RE": AStar(0.1),
                "PG": AStar(0),
                "PO": AStar(0),
                "PE": AStar(0.1),
            },
            "MCTS": {
                "SG": MCTS(c_exploration=param, rollout_depth=0),
                "SO": MCTS(c_exploration=param, rollout_depth=0),
                "SE": MCTS(c_exploration=param, rollout_depth=0),

                "RG": MCTS(c_exploration=param, rollout_depth=0),
                "RO": MCTS(c_exploration=param, rollout_depth=0),
                "RE": MCTS(c_exploration=param, rollout_depth=0),

                "PG": MCTS(c_exploration=param, rollout_depth=0),
                "PO": MCTS(c_exploration=param, rollout_depth=0),
                "PE": MCTS(c_exploration=param, rollout_depth=0),

                #"SG": MCTS(c_exploration=0, max_token_try=9),
                #"SO": MCTS(c_exploration=0, max_token_try=5),
                #"SE": MCTS(c_exploration=0, max_token_try=10),
                #"RG": MCTS(c_exploration=0, max_token_try=30),
                #"RO": MCTS(c_exploration=0, max_token_try=10),
                #"RE": MCTS(c_exploration=0, max_token_try=10),
                #"PH": MCTS(c_exploration=0, max_token_try=10),
                #"PO": MCTS(c_exploration=0, max_token_try=10),
                #"PE": MCTS(c_exploration=0, max_token_try=10),
            },
            "LNS": {
                "SG": LNS(max_destroy_n=4, max_repair_n=4),
                "SO": LNS(max_destroy_n=4, max_repair_n=4),
                "SE": LNS(max_destroy_n=4, max_repair_n=4),
                "RG": LNS(max_destroy_n=8, max_repair_n=8),
                "RO": LNS(max_destroy_n=2, max_repair_n=2),
                "RE": LNS(max_destroy_n=8, max_repair_n=8),
                "PG": LNS(max_destroy_n=3, max_repair_n=3),
                "PO": LNS(max_destroy_n=2, max_repair_n=2),
                "PE": LNS(max_destroy_n=3, max_repair_n=3),
            },
            "MH": {
                "SG": MetropolisHasting(alpha=4),
                "SO": MetropolisHasting(alpha=4),
                "SE": MetropolisHasting(alpha=4),
                "RG": MetropolisHasting(alpha=2),
                "RO": MetropolisHasting(alpha=10),
                "RE": MetropolisHasting(alpha=4),
                "PG": MetropolisHasting(alpha=4),
                "PO": MetropolisHasting(alpha=4),
                "PE": MetropolisHasting(alpha=4),
            },
            "GP": {
                "SG": GeneticProgramming(population_size=60, p_mutation=0.1),
                "SO": GeneticProgramming(population_size=45, p_mutation=0.2),
                "SE": GeneticProgramming(population_size=60, p_mutation=0.1),
                "RG": GeneticProgramming(population_size=30, p_mutation=0.8),
                "RO": GeneticProgramming(population_size=45, p_mutation=0.4),
                "RE": GeneticProgramming(population_size=45, p_mutation=0.4),
                "PG": GeneticProgramming(population_size=30, p_mutation=0.8),
                "PO": GeneticProgramming(population_size=60, p_mutation=0.8),
                "PE": GeneticProgramming(population_size=60, p_mutation=0.8),
            },
        },

        "settings": {
            "SG": StringLevenshtein(),
            "SO": StringOptimizedAlignment(),
            "SE": StringEntailment(),
            "RG": RobotGreedy(),
            "RO": RobotOptimizedSteps(),
            "RE": RobotEntailment(),
            "PG": PixelHamming(),
            "PO": PixelHammingPointerDistance(),
            "PE": PixelEntailment(),
        },

        "test_cases": {
            "param": {
                "S": (
                    [1,3,5],
                    range(1, 327, 20),
                    [1, 2, 3]
                ),

                "R": (
                    [],
                    [],
                    [1]
                ),

                "P": (
                    [],
                    [],
                    [1],
                )
            },

            "eval": {
                "S": (
                    range(1, 10, 2),
                    [t for t in range(1, 327) if t not in range(1, 327, 20)],
                    range(1, 11)
                ),

                "R": (
                    [],
                    [],
                    range(2, 11)
                ),

                "P": (
                    [],
                    [],
                    range(2, 11),
                )
            },

            "debug": {
                "S": (
                    # Runs all string tasks with 3 given input/output pairs
                    [3],
                    range(1, 327, 20),
                    [1],
                ),

                "R": (
                    # Runs all robot tasks
                    [],
                    [],
                    range(1, 10),
                ),

                "P": (
                    # Runs all pixel tasks except the first trial
                    [],
                    [],
                    range(2, 11),
                )
            },
            "all": defaultdict(lambda: ([], [], []))
        }
    }
