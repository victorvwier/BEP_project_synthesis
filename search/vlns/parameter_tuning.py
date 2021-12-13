from collections import Iterable, Callable
from statistics import mean

import numpy as np

from common.experiment import Example, TestCase
from common.tokens.string_tokens import Drop
from evaluation.experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name
from example_parser.parser import Parser
from example_parser.pixel_parser import PixelParser
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
from search.abstract_search import SearchAlgorithm


class ParameterTuning:

    def __init__(self,
                 domain: str,
                 files: (Iterable[int], Iterable[int], Iterable[int]),
                 repetitions: int,
                 search_cons: Callable[[float], SearchAlgorithm],
                 values: list[float],
                 debug: bool = False):
        self.search_cons = search_cons
        self.values = values
        self.repetitions = repetitions
        self.files = files
        self.debug = debug

        self.parser = self._get_parser(domain)
        self.test_cases = self._get_test_cases(files)
        self.env_tokens = set([c() for c in extract_trans_tokens_from_domain_name(domain)])
        self.bool_tokens = set([c() for c in extract_bool_tokens_from_domain_name(domain)])

    def run(self):
        for v in self.values:
            res = []
            for _ in range(self.repetitions):
                r = self._test_search(self.search_cons(v))
                res.append(r)

            res = self._process(res)
            res["value"] = v

            print(res)

    def _test_search(self, search: SearchAlgorithm) -> dict:
        total_cost = 0
        total_time = 0
        total_iterations = 0
        total_program_length = 0
        time_destroy = 0
        time_repair = 0
        time_cost = 0
        n_correct = 0
        n_failed = 0
        correct_cases = {}

        for tc in self.test_cases:
            r = search.run(tc.training_examples, self.env_tokens, self.bool_tokens)

            c = search.cost(tc.test_examples, r.dictionary["program"])

            total_time += r.dictionary["execution_time"]
            total_iterations += r.dictionary["iterations"]
            total_program_length += r.dictionary["program_length"]
            time_destroy += r.dictionary["time_destroy"]
            time_repair += r.dictionary["time_repair"]
            time_cost += r.dictionary["time_cost"]

            ca = tc.path_to_result_file.split("-")

            if c == 0:
                n_correct += 1

                if self.debug:
                    print("Solved {}-{}-{} with: {}".format(ca[1],ca[2],ca[3], r.dictionary["program"]))

                if ca[2] not in correct_cases:
                    correct_cases[ca[2]] = 1
                else:
                    correct_cases[ca[2]] += 1
            else:
                if self.debug:
                    print("Failed solving {}-{}-{}. Best found ({}): {}".format(ca[1],ca[2],ca[3], c.__round__(2), r.dictionary["program"]))
            if c == float('inf'):
                n_failed += 1
            else:
                total_cost += c

        size = len(self.test_cases)

        total_cost /= size
        total_time /= size
        total_iterations /= size
        total_program_length /= size
        time_destroy /= size
        time_repair /= size
        time_cost /= size
        n_correct /= size
        n_failed /= size

        return {
            "ave_cost": total_cost,
            "ave_exe_time": total_time,
            "ave_iterations": total_iterations,
            "ave_time_destroy": time_destroy,
            "ave_time_repair": time_repair,
            "ave_time_cost": time_cost,
            "per_correct": n_correct,
            "per_failed": n_failed,
            "average_program_length": total_program_length,
        }

    def _process(self, results: list[dict[str, float]]) -> dict[str, (float, float)]:
        res = {}

        for d in results:
            for k, v in d.items():
                if k not in res:
                    res[k] = []

                res[k].append(v)

        return {k: (mean(v).__round__(4), np.std(v).__round__(4)) for k, v in res.items()}

    def _get_test_cases(self, files: (Iterable[int], Iterable[int], Iterable[int])) -> list[TestCase]:
        res = []

        for i1 in files[0]:
            for i2 in files[1]:
                for i3 in files[2]:
                    res.append(self.parser.parse_file("{}-{}-{}.pl".format(i1, i2, i3)))

        return res

    @staticmethod
    def _get_parser(domain: str) -> Parser:
        if domain == "string":
            return StringParser()
        elif domain == "robot":
            return RobotParser()
        elif domain == "pixel":
            return PixelParser()
        else:
            raise Exception()
