from evaluation.experiment_procedure import *
from example_parser.string_parser import StringParser
from search.abstract_search import SearchAlgorithm
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
      com, av = 0, 0
      com2, av2 = 0, 0
      metro: Type[SearchAlgorithm] = MetropolisHasting
      brute: Type[SearchAlgorithm] = Brute
      depth = 1
      for j in range(0, depth):
            for i in range(1, 10):
                  experiment: Experiment = StringParser().parse_all(file_prefix="4-{}-".format(i))
                  (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment, metro)
                  print('000000')
                  # (ave_suc2, ave_time2, com_suc2) = test_performance_single_experiment(experiment, brute)
                  # com2 += com_suc2
                  com += com_suc
      
      # """
      print(com2 / 9 * depth)
      print(com / 9 * depth)
