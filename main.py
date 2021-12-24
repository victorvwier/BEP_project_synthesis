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
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n_vdi import RemoveNInsertNVDI

if __name__ == "__main__":
    searchAlgos : List[Type[SearchAlgorithm]] = [
        #[MetropolisHasting, "metro"],
        #[Brute, "brute"],
        #[MCTS, "mcts"],
        #[VanillaGP, "gp"],
        [RemoveNInsertN, "VLNS"],
        [lambda t: RemoveNInsertNVDI(1000, t), "VLNS_vdi1000"],
        [lambda t: RemoveNInsertNVDI(3000, t), "VLNS_vdi3000"],
        [lambda t: RemoveNInsertNVDI(5000, t), "VLNS_vdi5000"],
        [lambda t: RemoveNInsertNVDI(10000, t), "VLNS_vdi10000"],
        [lambda t: RemoveNInsertNVDI(15000, t), "VLNS_vdi15000"],
        #[AStar, "Astar"]
    ]

    file_names : list[str] = [
        "brute-20211222-204643.txt",
        "VLNS-20211222-205850.txt",
        "VLNS_vdi-20211223-111324.txt",
    ]
    file_names = ["","","","","",""]

    ranges = [
        #range(1, 51),
        #range(51, 101),
        range(1, 101),
        #range(101, 151),
        #range(151, 201),
        range(101, 201),
        range(201, 251),
        range(251, 301),
        range(301, 328),
    ]
    
    print(os.cpu_count())

    results = []
    for range in ranges:
        for alg, file_name in zip(searchAlgos, file_names):
            result = BatchRun(
            # Task domain
            domain="string",

            # Iterables for files name. Use [] to use all values.
            # This runs all files adhering to format "2-*-[0 -> 10]"
            # Thus, ([], [], []) runs all files for a domain.
            files=([], range, []),

            # Search algorithm to be used
            search_algorithm=alg[0](10),

            # Prints out result when a test case is finished
            print_results=True,

            # Use multi core processing
            multi_core=True,
            available_cores=128,

            # Use file_name= to append to a file whenever a run got terminated
            # Comment out argument to create new file.
            #file_name=file_name,
            file_name="",
        ).run()

    # for res in results:
    #     print(res[0], res[1])