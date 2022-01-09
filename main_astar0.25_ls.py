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
    BatchRun(domain="string", files=([],range(50),[]), search_algorithm=AStar(60, weight=0.25, distance_override='levenshtein'), outfile_suffix="astar0.25_ls", print_results=True, multi_core=True).run()

