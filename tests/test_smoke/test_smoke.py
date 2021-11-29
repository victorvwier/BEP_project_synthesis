import unittest

from evaluation.experiment_procedure import *
from testcase_parser.string_parser import StringParser
from search.abstract_search import SearchAlgorithm


class SmokeTest(unittest.TestCase):
    def test_simple(self):
        search: SearchAlgorithm = Brute
        experiment = StringParser().parse_all(file_prefix="1-1-")
        (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment, search)
        self.assertTrue(com_suc == 1)
