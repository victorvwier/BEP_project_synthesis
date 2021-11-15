from experiment_procedure import test_performance_single_case_and_write_to_file
from parser.robot_parser import RobotParser
from parser.string_parser import StringParser
from robot_environment import robot_tokens
from string_environment import string_tokens

if __name__ == "__main__":
    testcase = StringParser().parse_file("1-1-1.pl")
    (succesper, time) = test_performance_single_case_and_write_to_file(testcase, string_tokens.TransTokens, string_tokens.BoolTokens)
    print("Test case worked for {}% of the time, running time: {}".format(succesper, time))
