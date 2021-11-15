from experiment_procedure import test_performance_single_case
from parser.robot_parser import RobotParser
from parser.string_parser import StringParser
from robot_environment import robot_tokens
from string_environment import string_tokens

if __name__ == "__main__":
    testcase = StringParser().parse_file("1-1-1.pl")
    (succesper, time, program) = test_performance_single_case(testcase, string_tokens.TransTokens, string_tokens.BoolTokens)
    print("Test case worked for {}% of the time, running time: {}".format(succesper, time))
    print(program.sequence[0].tokens)
