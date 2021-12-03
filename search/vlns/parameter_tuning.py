from collections import Iterable, Callable

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
                 values: list[float]):
        self.search_cons = search_cons
        self.values = values
        self.repetitions = repetitions

        self.parser = self._get_parser(domain)
        self.test_cases = self._get_test_cases(files)
        self.env_tokens = set([c() for c in extract_trans_tokens_from_domain_name(domain)])
        self.bool_tokens = set([c() for c in extract_bool_tokens_from_domain_name(domain)])

    def run(self):
        for v in self.values:
            r = self._test_search(self.search_cons(v))

            r["value"] = v

            print(r)

    def _test_search(self, search: SearchAlgorithm) -> dict:
        total_cost = 0
        total_time = 0
        total_iterations = 0
        time_destroy = 0
        time_repair = 0
        time_cost = 0
        n_correct = 0
        n_failed = 0

        for _ in range(self.repetitions):
            for tc in self.test_cases:
                r = search.run(tc, self.env_tokens, self.bool_tokens)

                c = search.cost(tc, r.dictionary["program"])

                total_time += r.dictionary["execution_time"]
                total_iterations += r.dictionary["iterations"]
                time_destroy += r.dictionary["time_destroy"]
                time_repair += r.dictionary["time_repair"]
                time_cost += r.dictionary["time_cost"]

                if c == 0:
                    n_correct += 1
                if c == float('inf'):
                    n_failed += 1
                else:
                    total_cost += c

        size = len(self.test_cases) * self.repetitions

        total_cost /= size
        total_time /= size
        total_iterations /= size
        time_destroy /= size
        time_repair /= size
        time_cost /= size
        n_correct /= size
        n_failed /= size

        return {
            "ave_cost": total_cost,
            "ave_exe_time": total_time.__round__(5),
            "ave_iterations": total_iterations.__round__(1),
            "ave_time_destroy": time_destroy.__round__(5),
            "ave_time_repair": time_repair.__round__(5),
            "ave_time_cost": time_cost.__round__(5),
            "per_correct": n_correct.__round__(2),
            "per_failed": n_failed.__round__(2),
        }

    def _get_test_cases(self, files: (Iterable[int], Iterable[int], Iterable[int])) -> list[list[Example]]:
        res = []

        for i1 in files[0]:
            for i2 in files[1]:
                for i3 in files[2]:
                    res.append(self.parser.parse_file("{}-{}-{}.pl".format(i1, i2, i3)).training_examples)

        return res

    @staticmethod
    def _get_parser(domain: str) -> Parser:
        if domain == "string":
            return StringParser()
        elif domain == "string":
            return RobotParser()
        elif domain == "string":
            return PixelParser()
        else:
            raise Exception()
