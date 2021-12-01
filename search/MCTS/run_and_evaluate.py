from evaluation.experiment_procedure import write_performances_of_experiments_to_file
from example_parser.pixel_parser import PixelParser
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
from search.MCTS.mcts import MCTS
from search.brute.brute import Brute


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


if __name__ == "__main__":

    print("Start reading in all experiments...")
    debug_experiments = parse_debugging_and_basic_performance_experiments()
    print("Done reading in all experiments!")
    write_performances_of_experiments_to_file(
        debug_experiments,
        "evaluation/results/Brute_debug_results1.txt",
        search_algorithm=MCTS
    )

    print("done!")