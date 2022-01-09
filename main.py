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

# if __name__ == '__main__':
#     search = AStar(1000)
#     env1 = StringEnvironment("abcdefgh", pos=1)
#     # env1 = StringEnvironment("ABCDefgh", pos=3)
#     env2 = StringEnvironment("ABCDEFGH")
#
#     result = search.quick_run((env1, env2))
#     print()
#     print(result.dictionary['program'].to_formatted_string())
#     # program = result.dictionary['program']
#     # program.interp(env1, debug=True, env2=env2)
#
#     # from common.tokens.string_tokens import *
#     # from common.tokens.control_tokens import *
#     # p2 = Program([MoveLeft(), MakeUppercase(), LoopWhile(NotAtEnd(), [MoveRight(), MakeUppercase()])])
#     # p2.interp(env1, debug=True, env2=env2)




if __name__ == "__main__":
    BatchRun(domain="string", files=([],range(30),[1]), search_algorithm=Brute(60), outfile_suffix="brecht-desktop", print_results=True, multi_core=True).run()

    # searchAlgos : List[Type[SearchAlgorithm]] = [
    #     # [MetropolisHasting, "metro"],
    #     # [Brute, "brute"],
    #     # [MCTS, "mcts"],
    #     # [VanillaGP, "gp"],
    #     # [RemoveNInsertN, "VLNS"],
    #     [AStar, "Astar"]
    # ]
    #
    # results = []
    # for alg in searchAlgos:
    #     result = BatchRun(
    #     # Task domain
    #     domain="pixel",
    #
    #     # Iterables for files name. Use [] to use all values.
    #     # This runs all files adhering to format "2-*-[0 -> 10]"
    #     # Thus, ([], [], []) runs all files for a domain.
    #     # files=([], range(0, 300, 15), [1,3,8]),
    #     files=([], [], []),
    #
    #     # Search algorithm to be used
    #     search_algorithm=alg[0](60, weight=0),
    #
    #     # Prints out result when a test case is finished
    #     print_results=True,
    #
    #     # Use multi core processing
    #     multi_core=True,
    #
    #     # Use file_name= to append to a file whenever a run got terminated
    #     # Comment out argument to create new file.
    #     #file_name="VLNS-20211213-162128.txt"
    # ).run()
    #
    # for res in results:
    #     print(res[0], res[1])