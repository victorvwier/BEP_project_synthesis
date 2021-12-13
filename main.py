from evaluation.experiment_procedure import *
from example_parser.string_parser import StringParser
from search.MCTS.mcts import MCTS
from search.abstract_search import SearchAlgorithm
from search.gen_prog.vanilla_GP import VanillaGP
from search.metropolis_hastings.metropolis import MetropolisHasting

if __name__ == "__main__":
    """
    experiment = RobotParser().parse_all(file_prefix="2")
    (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
    print("Experiment had an average success rate of {}%, average running time: {}, and {}% of examples were "
        "completely successful".format(ave_suc, ave_time, com_suc))
    """

    """
      Use this to run groups of test case, experiments, defined by file prefix

      experiment = StringParser().parse_all(file_prefix="1-2-")
      (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
      print("Experiment had an average success rate of {}%, average running time: {}, and {}% of examples were "
          "completely successful".format(ave_suc, ave_time, com_suc))

      """

    """
      Use this to run groups of experiments defined by file prefix
    """
    searchAlgos : List[Type[SearchAlgorithm]] = [
        [MetropolisHasting, "metro"],
        [Brute, "brute"],
        [MCTS, "mcts"],
        [VanillaGP, "gp"]
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