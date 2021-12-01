import time
from pathlib import Path

from typing import Type
from common.prorgam import *
from common.experiment import Experiment, TestCase
from example_parser.pixel_parser import PixelParser
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
import common.tokens.pixel_tokens as pixel_tokens
import common.tokens.robot_tokens as robot_tokens
from search.abstract_search import Search
from search.brute.brute import Brute

import common.tokens.string_tokens as string_tokens


# MAX_TOKEN_FUNCTION_DEPTH = 3
# MAX_NUMBER_OF_ITERATIONS = 30
# MAX_EXECUTION_TIME_IN_SECONDS = 30

def extract_domain_from_environment(environment):
    domain_name = "unknown"
    if isinstance(environment, RobotEnvironment):
        domain_name = "robot"
    elif isinstance(environment, StringEnvironment):
        domain_name = "string"
    elif isinstance(environment, PixelEnvironment):
        domain_name = "pixel"
    return domain_name


def extract_bool_tokens_from_domain_name(domain_name):
    if domain_name == "robot":
        return robot_tokens.BoolTokens
    if domain_name == "string":
        return string_tokens.BoolTokens
    if domain_name == "pixel":
        return pixel_tokens.BoolTokens


def extract_trans_tokens_from_domain_name(domain_name):
    if domain_name == "robot":
        return robot_tokens.TransTokens
    if domain_name == "string":
        return string_tokens.TransTokens
    if domain_name == "pixel":
        return pixel_tokens.TransTokens


# a single case exists of several examples which should be solved by one single program
def test_performance_single_case_and_write_to_file(test_case: TestCase, trans_tokens, bool_tokens,
                                                   searchAlgorithm: Type[Search]):
    start_time = time.time()

    # # find program that satisfies training_examples
    program = searchAlgorithm.search(test_case, trans_tokens, bool_tokens)

    finish_time = time.time()

    path = Path(__file__).parent.joinpath(test_case.path_to_result_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w+") as file:

        file.writelines(["Program: "  + str(program.sequence) + "\n \n"])

        execution_time_in_seconds = finish_time - start_time
        successes = 0
        for e in test_case.test_examples:
            in_state = e.input_environment
            out_state = e.output_environment

            file.writelines([
                "input: " + str(in_state) + "\n",
                "wanted output: " + str(out_state) + "\n"
            ])

            try:
                result = program.interp(in_state)
            except:
                #print("interpreting the program threw an error")
                result = in_state

            file.writelines([
                "output: " + str(result) + "\n \n"
            ])


            if out_state.correct(result):
                successes += 1

        success_percentage = 100.0 * successes / len(test_case.test_examples)

        print(test_case.path_to_result_file, end=" \t")
        print(success_percentage)
        # print(program)


        # file = open(test_case.path_to_result_file, "a+")
        file.writelines([
            "succes_percentage: " + str(success_percentage) + "\n",
            "execution_time_in_seconds" + str(execution_time_in_seconds) + "\n"
        ])

    return success_percentage, execution_time_in_seconds


# An experiment exists of different cases in the same domain.
# For each experiment different, one program is generated per case.
def test_performance_single_experiment(experiment: Experiment, search: Type[Search]):
    sum_of_success_percentages = 0
    sum_of_execution_times_in_seconds = 0
    number_of_completely_successful_programs = 0

    # extract tokens from the experiment's domain name
    test_cases = experiment.test_cases
    bool_tokens = extract_bool_tokens_from_domain_name(experiment.domain_name)
    trans_tokens = extract_trans_tokens_from_domain_name(experiment.domain_name)

    for test_case in test_cases:
        success_percentage, execution_time_in_seconds = test_performance_single_case_and_write_to_file(test_case,
                                                                                                       trans_tokens,
                                                                                                       bool_tokens,
                                                                                                       search)
        sum_of_success_percentages += success_percentage
        sum_of_execution_times_in_seconds += execution_time_in_seconds
        if success_percentage == 100.0:
            number_of_completely_successful_programs += 1

    average_success_percentage = sum_of_success_percentages / len(test_cases)
    average_execution_time = sum_of_execution_times_in_seconds / len(test_cases)
    percentage_of_completely_successful_programs = number_of_completely_successful_programs / len(test_cases)

    return average_success_percentage, average_execution_time, percentage_of_completely_successful_programs


def write_performances_of_experiments_to_file(experiments: List[Experiment], output_file: str, search_algorithm: Search):
    lines_to_write = []

    for experiment in experiments:
        average_success_percentage, average_execution_time, percentage_of_completely_successful_programs = \
            test_performance_single_experiment(experiment, search=search_algorithm)
        lines_to_write.append("Experiment name: " + experiment.name + "\n")
        lines_to_write.append("Average_success_percentage: " + str(average_success_percentage) + "\n")
        lines_to_write.append("Average_execution_time: " + str(average_execution_time) + "\n")
        lines_to_write.append("Percentage_of_completely_successful_programs: "
                              + str(percentage_of_completely_successful_programs) + "\n")
        lines_to_write.append("\n")
        print("Experiment: {} finished with status: {}".format(experiment.name, average_success_percentage))
    path = Path(__file__).parent.joinpath(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as file:
        file.writelines(lines_to_write)


def get_all_experiments():
    experiments = []

    for i in range(2, 12, 2):
        robot_experiment = RobotParser().parse_all(experiment_name="Robot - starting with " + str(i),
                                                   file_prefix=str(i))
        experiments.append(robot_experiment)

    for i in range(6):
        pixel_experiment = PixelParser().parse_all(experiment_name="Pixel - starting with " + str(i),
                                                   file_prefix=str(i))
        experiments.append(pixel_experiment)

    for i in range(1, 10):
        string_experiment = StringParser().parse_all(experiment_name="String - starting with " + str(i),
                                                     file_prefix=str(i))
        experiments.append(string_experiment)

    return experiments


if __name__ == "__main__":
    print("Start reading in all experiments")
    experiments1 = get_all_experiments()

    print("Done reading in all experiments")
    write_performances_of_experiments_to_file(
        experiments1,
        "performance_results/results.txt",
        search_algorithm=Brute
    )
