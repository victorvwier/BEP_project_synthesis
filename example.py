import itertools

from experiment_procedure import *
from parser.pixel_parser import PixelParser
from parser.robot_parser import RobotParser
from parser.string_parser import StringParser
from total_performance.evaluate import ProgramSearchEvaluator
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.optional_repair_expanding_sequences import \
    OptionalRepairExpandingSequences

if __name__ == "__main__":

    """
    measure = Measure(
        prefix="2",
        iterator=("-{}-{}".format(a, b) for a in range(0,10) for b in range(1,11)),
        parser=RobotParser(),
        id=lambda x, y : x + ", " + y.split("-")[1]
    )
    measure.measure("results/aggregations/robot-{0,5}-{1,11}.txt")
    """

    evaluator = ProgramSearchEvaluator(
        searcher=OptionalRepairExpandingSequences(
            domain="robot",
            max_iterations=1000,
            max_token_function_depth=3,
        ),
        parser=StringParser(),
        file_iterator=("{}-{}-".format(a, b) for a in [6] for b in range(1, 3)),
        id=lambda x: x,
        max_token_function_depth=3
    )
    evaluator.eval("results/aggregations/ores/string-1-{1,5}.txt")

    """
    experiment = RobotParser().parse_all(file_prefix="2")
    (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
    print("Experiment had an average success rate of {}%, average running time: {}, and {}% of programs were "
          "completely successful".format(ave_suc, ave_time, com_suc))
    """

    """
    Use this to run groups of test case, experiments, defined by file prefix
    
    experiment = StringParser().parse_all(file_prefix="1-130")
    (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
    print("Experiment had an average success rate of {}%, average running time: {}, and {}% of programs were "
          "completely successful".format(ave_suc, ave_time, com_suc))
        
    """

    """
    Use this to run groups of experiments defined by file prefix
    ""
    for i in range(1, 30):
        experiment = StringParser().parse_all(file_prefix="1-10-".format(i))
        (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment)
    """
