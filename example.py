from experiment_procedure import *
from parser.pixel_parser import PixelParser
from parser.robot_parser import RobotParser
from parser.string_parser import StringParser
from robot_environment import robot_tokens
from string_environment import string_tokens

if __name__ == "__main__":
    experiment = StringParser().parse_all()#file_prefix="1-4-")
    (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
    print("Experiment had an average success rate of {}%, average running time: {}, and {}% of programs were "
          "completely successful".format(ave_suc, ave_time, com_suc))

    """
    Use this to run groups of test case defined by file prefix
    
    experiment = StringParser().parse_all(file_prefix="1-2-")
    (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
    print("Experiment had an average success rate of {}%, average running time: {}, and {}% of programs were "
          "completely successful".format(ave_suc, ave_time, com_suc))
        
    """