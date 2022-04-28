from typing import List

from common.experiment import Experiment
from evaluation.experiment_procedure import write_performances_of_experiments_to_file
from example_parser.pixel_parser import PixelParser
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
from solver.search.implementations.MCTS.mcts import MCTS


def parse_debugging_and_basic_performance_experiments():
    experiments = []

    # get String experiments [1,3,5,7,9]-[51->60]-[1]
    for number_of_examples in range(1, 10, 2):
        for task_number in range(51, 61):
            string_experiment = StringParser().parse_all(
                experiment_name="String - "
                                "number_of_examples: %s, "
                                "task_number: %s "
                                "trial_number: 1" % (number_of_examples, task_number),
                file_prefix="%s-%s-1.pl" % (number_of_examples, task_number)
            )
            experiments.append(string_experiment)

    # get Robot experiments [2,4,6,8,10]-[5->9]-[0]
    for size in range(2, 11, 2):
        for task_number in range(5, 10):
            robot_experiment = RobotParser().parse_all(
                experiment_name="Robot - "
                                "size: %s, "
                                "task_number: %s "
                                "trial_number: 0" % (size, task_number),
                file_prefix="%s-%s-0.pl" % (size, task_number)
            )
            experiments.append(robot_experiment)

    # get Pixel experiments [1->5]-[5->9]-[1]
    for size in range(1, 6, 1):
        for task_number in range(5, 10):
            pixel_experiment = PixelParser().parse_all(
                experiment_name="Pixel - "
                                "size: %s, "
                                "task_number: %s "
                                "trial_number: 1" % (size, task_number),
                file_prefix="%s-%s-1.pl" % (size, task_number)
            )
            experiments.append(pixel_experiment)

    return experiments


def parse_experiments_string_fine_tuning() -> List[Experiment]:
    experiments = []

    for complexity in range(1, 10, 4):  # get experiments with complexity 1, 5 and 9
        test_cases = []
        for task in range(100, 126, 1):  # get tasks 100 until 125
            test_case = StringParser().parse_file("%s-%s-1.pl" % (complexity, task))
            test_cases.append(test_case)
        experiment = Experiment(
            name="String fine tune experiment - Complexity: %s, task: 100-125, trial: 1" % complexity,
            domain_name="string",
            test_cases=test_cases
        )
        experiments.append(experiment)

    return experiments


def parse_experiments_robot_fine_tuning() -> List[Experiment]:
    experiments = []

    for complexity in range(2, 11, 2):  # get experiments with complexity 2, 4, 6, 8, 10
        test_cases = []
        for task in range(5, 10):  # get tasks 5 until 9
            test_case = RobotParser().parse_file("%s-%s-1.pl" % (complexity, task))
            test_cases.append(test_case)
        experiment = Experiment(
            name="Robot fine tune experiment - Complexity: %s, task: 5-9, trial: 1" % complexity,
            domain_name="robot",
            test_cases=test_cases
        )
        experiments.append(experiment)

    return experiments


def parse_experiments_pixel_fine_tuning() -> List[Experiment]:
    experiments = []

    for complexity in range(1, 6):  # get experiments with complexity 1 until 5
        test_cases = []
        for task in range(5, 10):  # get tasks 5 until 9
            test_case = PixelParser().parse_file("%s-%s-2.pl" % (complexity, task))
            test_cases.append(test_case)
        experiment = Experiment(
            name="Pixel fine tune experiment - Complexity: %s, task: 5-9, trial: 2" % complexity,
            domain_name="pixel",
            test_cases=test_cases
        )
        experiments.append(experiment)

    return experiments


def parse_single_string_experiment(filename: str):
    string_experiment = StringParser().parse_all(
        experiment_name="String experiment: %s" % filename,
        file_prefix=filename,
    )
    return string_experiment


if __name__ == "__main__":
    # # running debug experiments
    # print("Start reading in all experiments...")
    # debug_experiments = parse_debugging_and_basic_performance_experiments()
    # print("Done reading in all experiments!")
    # write_performances_of_experiments_to_file(
    #     debug_experiments,
    #     "evaluation/results/MCTS_debug_results_final_execution_time_10_seconds.txt",
    #     search_algorithm=MCTS
    # )

    # # run single string experiment
    print("Start reading in single string experiment...")
    string_experiment = parse_single_string_experiment("9-81-1.pl")
    print("Done reading in string experiment!")
    write_performances_of_experiments_to_file(
        [string_experiment],
        "evaluation/results/MCTS_string_9_81_1_version_1_1_improved_levenstein_distance.txt",
        search_algorithm=MCTS
    )

    # # running string fine tuning experiments
    # print("Start reading in all experiments...")
    # string_experiments = parse_experiments_string_fine_tuning()
    # print("Done reading in all experiments!")
    # write_performances_of_experiments_to_file(
    #     string_experiments,
    #     "evaluation/results/MCTS_string_fine_tuning_rerun_v_2_0_execution_time_10_seconds___%s__%s.txt"
    #     % (MAX_TOKEN_TRY, round(EXPLORATION_CONSTANT, 2)),
    #     search_algorithm=MCTS
    # )

    # # running robot fine tuning experiments
    # print("Start reading in all experiments...")
    # robot_experiments = parse_experiments_robot_fine_tuning()
    # print("Done reading in all experiments!")
    # write_performances_of_experiments_to_file(
    #     robot_experiments,
    #     "evaluation/results/MCTS_robot_fine_tuning_6_v_2_0_execution_time_10_seconds___%s__%s.txt"
    #     % (MAX_TOKEN_TRY, round(EXPLORATION_CONSTANT, 2)),
    #     search_algorithm=MCTS
    # )

    # # running string fine tuning experiments
    # print("Start reading in all experiments...")
    # pixel_experiments = parse_experiments_pixel_fine_tuning()
    # print("Done reading in all experiments!")
    # write_performances_of_experiments_to_file(
    #     pixel_experiments,
    #     "evaluation/results/MCTS_pixel_fine_tuning_15_v_2_0_execution_time_10_seconds___%s__%s.txt"
    #     % (MAX_TOKEN_TRY, round(EXPLORATION_CONSTANT, 2)),
    #     search_algorithm=MCTS
    # )

    # parent1 = Node("parent1")
    # parent2 = Node("parent2")
    # child1 = Node("kim", parent=parent1)
    # child2 = Node("harm", parent=parent1)
    # for pre, fill, node in RenderTree(parent1):
    #     print("%s%s" % (pre, node.name))
    #
    # parent2.children = [child1, child2]
    #
    # for pre, fill, node in RenderTree(parent2):
    #     print("%s%s" % (pre, node.name))
    #
    # for pre, fill, node in RenderTree(parent1):
    #     print("%s%s" % (pre, node.name))

    print("done!")
