# Experiment procedure:
# Input: Token, Examples,
# P <- synth()
# apply(P, TestExamples)
# Output -> Perf

import copy
import time
from brute_search import search

from invent import invent2
from typing import List 
from common_environment.environment import *
from interpreter.interpreter import *
from parser.experiment import Experiment, TestCase
import pixel_environment.pixel_tokens as pixel_tokens
import robot_environment.robot_tokens as robot_tokens
import string_environment.string_tokens as string_tokens

MAX_TOKEN_FUNCTION_DEPTH = 3
MAX_NUMBER_OF_ITERATIONS = 20
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
def test_performance_single_case_and_write_to_file(test_case: TestCase, trans_tokens, bool_tokens):
    
    start_time = time.time()

    # generate different token combinations
    token_functions = invent2(trans_tokens, bool_tokens, MAX_TOKEN_FUNCTION_DEPTH)
    # find program that satisfies training_examples
    program: Program
    program, best_loss, solved = search(token_functions, test_case.training_examples, MAX_NUMBER_OF_ITERATIONS)
    finish_time = time.time()

    file = open(test_case.path_to_result_file, "w+")

    execution_time_in_seconds = finish_time - start_time
    successes = 0
    for e in test_case.test_examples:
        in_state = e.input_environment
        out_state = e.output_environment
        try:
            result = program.interp(in_state)
        except:
            result = in_state

    	# TODO write results to file for Pixel and Robot environments
        if isinstance(result, StringEnvironment):
            file.writelines(["output: " + result.to_string() + "\n"])
        
        if out_state.correct(result):
            successes += 1

    success_percentage = 100.0 * successes / len(test_case.test_examples)

    print(test_case.path_to_result_file, end="  ")
    print(success_percentage)


    # file = open(test_case.path_to_result_file, "a+")
    file.writelines([
        "succes_percentage: " + str(success_percentage) + "\n",
        "execution_time_in_seconds" + str(execution_time_in_seconds) + "\n"
    ])
    file.close()

    return success_percentage, execution_time_in_seconds


# An experiment exists of different cases in the same domain.
# For each experiment different, one program is generated per case.
def test_performance_single_experiment(experiment: Experiment):
    sum_of_success_percentages = 0
    sum_of_execution_times_in_seconds = 0
    number_of_completely_successful_programs = 0
    
    # extract tokens from the experiment's domain name
    test_cases = experiment.test_cases
    bool_tokens = extract_bool_tokens_from_domain_name(experiment.domain_name)
    trans_tokens = extract_trans_tokens_from_domain_name(experiment.domain_name)

    for test_case in test_cases:
        success_percentage, execution_time_in_seconds = test_performance_single_case_and_write_to_file(test_case, trans_tokens, bool_tokens)
        sum_of_success_percentages += success_percentage
        sum_of_execution_times_in_seconds += execution_time_in_seconds
        if success_percentage == 100.0:
            number_of_completely_successful_programs += 1

    average_success_percentage = sum_of_success_percentages / len(test_cases)
    average_execution_time = sum_of_execution_times_in_seconds / len(test_cases)
    percentage_of_completely_successful_programs = number_of_completely_successful_programs / len(test_cases)

    return average_success_percentage, average_execution_time, percentage_of_completely_successful_programs


def write_performances_of_experiments_to_file(experiments: List[Experiment], output_file: str):
    lines_to_write = []
    
    for experiment in experiments:
        average_success_percentage, average_execution_time, percentage_of_completely_successful_programs = \
            test_performance_single_experiment(experiment)
        lines_to_write.append("Experiment name: " + experiment.name + "\n")
        lines_to_write.append("Average_success_percentage: " + str(average_success_percentage) + "\n")
        lines_to_write.append("Average_execution_time: " + str(average_execution_time) + "\n")
        lines_to_write.append("Percentage_of_completely_successful_programs: "
                              + str(percentage_of_completely_successful_programs) + "\n")
        lines_to_write.append("\n")
        print("Experiment: {} finished with status: {}".format(experiment.name, average_success_percentage))
    file = open(output_file, "w")
    file.writelines(lines_to_write)
    file.close()


def get_all_experiments():
    experiments = []
    string_experiments = StringParser.get_all_string_experiments()
    # TODO get parser for robot
    # TODO get parser for pixel
    experiments.extend(string_experiments)
    return experiments

if __name__ == "__main__":
    
    print("Start reading in all experiments")
    experiments = get_all_experiments()

    print("Done reading in all experiments")
    write_performances_of_experiments_to_file(
        experiments,
        "performance_results/results.txt"
    )
