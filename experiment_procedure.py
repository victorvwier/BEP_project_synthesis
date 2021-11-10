# Experiment procedure:
# Input: Token, Examples,
# P <- synth()
# apply(P, TestExamples)
# Output -> Perf

import time

# TODO check if i still call the correct invent method (invent vs invent2)
from invent import invent2
from typing import List

MAX_TOKEN_FUNCTION_DEPTH = 3
MAX_NUMBER_OF_ITERATIONS = 120


class Example

class TestCase:
    def __init__(self, training_examples, test_examples, distance_function, tokens, boolean_tokens):
        self.training_examples = training_examples # tuple consisting of input environment and wanted output environment
        self.test_examples = test_examples  # tuple consisting of input environment and wanted output environment
        self.tokens = tokens
        self.boolean_tokens = boolean_tokens


class Experiment:
    def __init__(self, name: str, test_cases: List[TestCase]):
        self.name = name
        self.test_cases = test_cases


# a single case exists of several examples which should be solved by one single program
def test_performance_single_case(test_case: TestCase):
    # generate different token combinations
    start_time = time.time()
    token_functions = invent2(test_case.tokens, test_case.boolean_tokens, MAX_TOKEN_FUNCTION_DEPTH)
    # find program that satisfies training_examples
    program = search(token_functions, test_case.training_examples, MAX_NUMBER_OF_ITERATIONS)
    finish_time = time.time()
    execution_time_in_seconds = start_time - finish_time
    successes = 0
    for (in_state, out_state) in test_case.test_examples:
        result = program.interp(program, in_state)
        if test_case.distance_function(result, out_state) == 0:
            successes += 1
    success_percentage = 100.0 * successes / len(test_case.test_examples)
    return success_percentage, execution_time_in_seconds


# An experiment exists of different cases in the same domain.
# For each experiment different, one program is generated per case.
def test_performance_single_experiment(test_cases: List[TestCase]):
    sum_of_success_percentages = 0
    sum_of_execution_times_in_seconds = 0
    number_of_completely_successful_programs = 0

    for test_case in test_cases:
        success_percentage, execution_time_in_seconds = test_performance_single_case(test_case)
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
            test_performance_single_experiment(experiment.test_cases)
        lines_to_write.append("Experiment name: " + experiment.name + "\n")
        lines_to_write.append("Average_success_percentage: " + str(average_success_percentage) + "\n")
        lines_to_write.append("Average_execution_time: " + str(average_execution_time) + "\n")
        lines_to_write.append("Percentage_of_completely_successful_programs: "
                              + str(percentage_of_completely_successful_programs) + "\n")
        lines_to_write.append("\n")

    file = open(output_file, "w")
    file.writelines(lines_to_write)
    file.close()


def get_experiments():
    # TODO get experiments from correct files
    experiment = ()

if __name__ == "__main__":
    write_performances_of_experiments_to_file(
        get_experiments(),
        "performance_results/results.txt"
    )
