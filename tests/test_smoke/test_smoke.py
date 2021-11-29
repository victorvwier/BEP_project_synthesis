import unittest

from common_environment.control_tokens import *
from common_environment.environment import *
from search.brute.brute import Brute
from string_environment.string_tokens import *
from search.abstract_search import SearchAlgorithm

from experiment_procedure import *
from parser.string_parser import StringParser
from search.abstract_search import SearchAlgorithm


class SmokeTest(unittest.TestCase):
    def test_simple(self):
        search: SearchAlgorithm = Brute
        experiment = StringParser().parse_all(file_prefix="1-1-")
        (ave_suc, ave_time, com_suc) = test_performance_single_experiment(experiment, search)
        self.assertTrue(com_suc == 1)
