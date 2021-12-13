import json
import time
import os
from pathlib import Path
from multiprocessing import Pool

from typing import Type
from common.prorgam import *
from common.experiment import Experiment, TestCase
from example_parser.pixel_parser import PixelParser
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
import common.tokens.pixel_tokens as pixel_tokens
import common.tokens.robot_tokens as robot_tokens
from search.a_star.a_star import AStar
from search.abstract_search import SearchAlgorithm
from search.brute.brute import Brute

import common.tokens.string_tokens as string_tokens
from search.search_result import SearchResult

MAX_EXECUTION_TIME_IN_SECONDS = 60
MULTI_PROCESS = True
NO_PROCESSES = os.cpu_count() - 1

max_iterations = 0

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
                                                   search_algorithm: type[SearchAlgorithm], weight=False):
    start_time = time.time()

    # # find program that satisfies training_examples
    search_result: SearchResult = search_algorithm(MAX_EXECUTION_TIME_IN_SECONDS, weight=weight).run(test_case.training_examples, trans_tokens, bool_tokens)
    program: Program = search_result.dictionary["program"]

    finish_time = time.time()

    search_result.dictionary['training_examples'] = [{'input': str(e.input_environment), 'output': str(e.output_environment)} for e in test_case.training_examples]
    test_examples = []

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

            test_examples.append({
                'input': str(e.input_environment),
                'output': str(e.output_environment),
                'success': e.output_environment.correct(result)
            })

        success_percentage = 100.0 * successes / len(test_case.test_examples)

        print(test_case.path_to_result_file, end=" \t")
        print(success_percentage)

        search_result.dictionary['test_examples'] = test_examples
        search_result.dictionary['success_percentage'] = 100.0 * successes / len(test_case.test_examples)
        search_result.dictionary['execution_time_in_seconds'] = execution_time_in_seconds
        search_result.dictionary['result_file'] = test_case.path_to_result_file
        search_result.dictionary['program'] = str(search_result.dictionary['program'])
        json.dumps(search_result.dictionary)
        stats = {'name': Path(test_case.path_to_result_file).stem}
        stats.update(search_result.dictionary)

        # file = open(test_case.path_to_result_file, "a+")
        file.writelines([
            "succes_percentage: " + str(success_percentage) + "\n",
            "execution_time_in_seconds" + str(execution_time_in_seconds) + "\n"
        ])

    return success_percentage, execution_time_in_seconds, stats


# An experiment exists of different cases in the same domain.
# For each experiment different, one program is generated per case.
def test_performance_single_experiment(experiment: Experiment, search: type[SearchAlgorithm], weight=False):
    sum_of_success_percentages = 0
    sum_of_execution_times_in_seconds = 0
    number_of_completely_successful_programs = 0
    cases_stats = []

    # extract tokens from the experiment's domain name
    test_cases = experiment.test_cases
    bool_tokens = extract_bool_tokens_from_domain_name(experiment.domain_name)
    trans_tokens = extract_trans_tokens_from_domain_name(experiment.domain_name)

    results = []
    if MULTI_PROCESS:
        with Pool(processes=NO_PROCESSES) as pool:
            for tc in test_cases:
                result = pool.apply_async(test_performance_single_case_and_write_to_file, (tc, trans_tokens, bool_tokens, search, weight))
                results.append(result)

            results = [r.get() for r in results]
    else:
        for tc in test_cases:
            result = test_performance_single_case_and_write_to_file(tc, trans_tokens, bool_tokens, search, weight)
            results.append(result)

    for result in results:
        success_percentage, execution_time_in_seconds, case_stats = result
        sum_of_success_percentages += success_percentage
        sum_of_execution_times_in_seconds += execution_time_in_seconds
        if success_percentage == 100.0:
            number_of_completely_successful_programs += 1
        cases_stats.append(case_stats)

    average_success_percentage = sum_of_success_percentages / len(test_cases)
    average_execution_time = sum_of_execution_times_in_seconds / len(test_cases)
    percentage_of_completely_successful_programs = number_of_completely_successful_programs / len(test_cases) * 100

    experiment_stats = {
        'average_success_percentage': average_success_percentage,
        'average_execution_time': average_execution_time,
        'percentage_of_completely_successful_programs': percentage_of_completely_successful_programs,
        'cases': cases_stats
    }

    return average_success_percentage, average_execution_time, percentage_of_completely_successful_programs, experiment_stats

    #

def write_performances_of_experiments_to_file(experiments: List[Experiment], output_file: str, search_algorithm: type[SearchAlgorithm], weight=False):
    lines_to_write = []

    for experiment in experiments:
        average_success_percentage, average_execution_time, percentage_of_completely_successful_programs, experiment_stats = \
            test_performance_single_experiment(experiment, search=search_algorithm, weight=weight)
        lines_to_write.append("Experiment name: " + experiment.name + "\n")
        lines_to_write.append("Average_success_percentage: " + str(average_success_percentage) + "\n")
        lines_to_write.append("Average_execution_time: " + str(average_execution_time) + "\n")
        lines_to_write.append("Percentage_of_completely_successful_programs: "
                              + str(percentage_of_completely_successful_programs) + "\n")
        lines_to_write.append("\n")
        print("Experiment: {} finished with status: {}".format(experiment.name, average_success_percentage))

        experiment_stats['name'] = experiment.name
        experiment_stats['domain'] = experiment.domain_name
        if weight is not False:
            json_path = Path(__file__).parent.joinpath(
                f"results/{experiment.name}-{search_algorithm.__name__}{weight}-{MAX_EXECUTION_TIME_IN_SECONDS}s.json")
        else:
            json_path = Path(__file__).parent.joinpath(
                f"results/{experiment.name}-{search_algorithm.__name__}-{MAX_EXECUTION_TIME_IN_SECONDS}s.json")
        print(json_path)
        with open(json_path, "w") as file:
            json.dump(experiment_stats, file, indent=2)

    path = Path(__file__).parent.joinpath(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as file:
        file.writelines(lines_to_write)


def get_all_experiments():
    experiments = []

    # for i in range(2, 12, 2):
    #     robot_experiment = RobotParser().parse_all(experiment_name="Robot - starting with " + str(i),
    #                                                file_prefix=str(i))
    #     experiments.append(robot_experiment)
    #
    # for i in range(6):
    #     pixel_experiment = PixelParser().parse_all(experiment_name="Pixel - starting with " + str(i),
    #                                                file_prefix=str(i))
    #     experiments.append(pixel_experiment)

    # for i in range(1, 10):
    #     string_experiment = StringParser().parse_all(experiment_name="String - starting with " + str(i),
    #                                                  file_prefix=str(i))
    #     experiments.append(string_experiment)

    # pixel_experiment = PixelParser().parse_all(experiment_name="pixels-hmod")
    # experiments.append(pixel_experiment)

    # robot_experiment = RobotParser().parse_all(experiment_name="robots-manhattan")
    # experiments.append(robot_experiment)

    size = "|".join([str(i) for i in range(1, 10)])
    task = "|".join([str(i) for i in range(1, 40)])
    string_experiment = StringParser().parse_all(experiment_name="strings_1-40_trial1_alignment_c1", regex=f'^({size})-({task})-1.pl$')
    experiments.append(string_experiment)

    return experiments


if __name__ == "__main__":
    # print("Start reading in all experiments")
    # experiments1 = get_all_experiments()
    # print("Done reading in all experiments")
    # write_performances_of_experiments_to_file(
    #     experiments1,
    #     "performance_results/results.txt",
    #     search_algorithm=AStar,
    #     weight=1
    # )

    print("Start reading in all experiments")
    experiments1 = get_all_experiments()
    print("Done reading in all experiments")
    write_performances_of_experiments_to_file(
        experiments1,
        "performance_results/results.txt",
        search_algorithm=AStar,
        weight=0.5
    )

    # print("Start reading in all experiments")
    # experiments1 = get_all_experiments()
    # print("Done reading in all experiments")
    # write_performances_of_experiments_to_file(
    #     experiments1,
    #     "performance_results/results.txt",
    #     search_algorithm=AStar,
    #     weight=0
    # )
