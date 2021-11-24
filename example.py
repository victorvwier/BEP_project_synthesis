from typing import Type

from experiment_procedure import *
from parser.pixel_parser import PixelParser
from parser.robot_parser import RobotParser
from parser.string_parser import StringParser
from robot_environment import robot_tokens
from search.abstract_search import SearchAlgorithm
from search.metropolis_hastings.metropolis import MetropolisHasting
from string_environment import string_tokens

if __name__ == "__main__":
      """
      experiment = RobotParser().parse_all(file_prefix="2")
      (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
      print("Experiment had an average success rate of {}%, average running time: {}, and {}% of programs were "
          "completely successful".format(ave_suc, ave_time, com_suc))
      """

      """
      Use this to run groups of test case, experiments, defined by file prefix

      experiment = StringParser().parse_all(file_prefix="1-2-")
      (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
      print("Experiment had an average success rate of {}%, average running time: {}, and {}% of programs were "
          "completely successful".format(ave_suc, ave_time, com_suc))

      """

      """
      Use this to run groups of experiments defined by file prefix
    """
      com2, av2 = 0, 0
      metro: Type[SearchAlgorithm] = MetropolisHasting
      brute: Type[SearchAlgorithm] = Brute
      depth = 1
      for j in range(0, depth):
            for i in range(1, 10):
                  experiment: Experiment = StringParser().parse_all(file_prefix="4-{}-".format(i))
                  (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment, metro)
                  print('000000')
                  #(ave_suc2, ave_time2, com_suc) = test_performance_single_experiment(experiment, brute)
                  av2 += ave_suc
                  com2 += com_suc
      
      # """
      print(com2 / 9 * depth)
      print(av2 / 9 * depth)
