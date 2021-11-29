import itertools
import random
import time
from collections import Callable, Iterator
from statistics import mean

from experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name, Program
from invent import invent2
from parser.parser import Parser, TestCase, Experiment
from robot_environment.robot_tokens import MoveRight
from vlns.search import ProgramSearch


class ProgramSearchEvaluator:

    def __init__(self, searcher: ProgramSearch, parser: Parser, file_iterator: Iterator[str], id: Callable[str, str], max_token_function_depth: int):
        self.searcher = searcher
        self.parser = parser
        self.file_iterator = file_iterator
        self.id = id

        trans_tokens = extract_trans_tokens_from_domain_name(searcher.domain)
        bool_tokens = extract_bool_tokens_from_domain_name(searcher.domain)
        self.token_library = invent2(trans_tokens, bool_tokens, max_token_function_depth)

    def eval(self, path_to_result_file: str):
        res = []

        for file_name in self.file_iterator:
            group = self.id(file_name)
            parsed = self.parser.parse_all(group, file_name)
            stats = self._eval_experiment(parsed)
            res.append((group, stats))

            print("Evaluated {}: {} with ".format(file_name, stats))

        lines = []
        for g in itertools.groupby(res, lambda e : e[0]):
            key = g[0]
            its = list(g[1])

            ave_suc = mean([e[1][0] for e in its])
            ave_time = mean([e[1][1] for e in its])
            per_suc = mean([e[1][2] for e in its]) * 100

            lines.append("{}, {}, {}, {}\n".format(key, ave_suc, ave_time, per_suc))

        file = open(path_to_result_file, "w+")
        file.writelines(lines)
        file.close()

    def _eval_test_case(self, test_case: TestCase):
        start_time = time.time()

        random_token = random.sample(self.token_library, 1)[0]
        program = self.searcher.find(Program([]), test_case)

        print("Final solution: {}".format(program))

        finish_time = time.time()

        execution_time_in_seconds = finish_time - start_time
        successes = 0

        for e in test_case.test_examples:
            try:
                result = program.interp(e.input_environment)
            except:
                print("interpreting the program threw an error")
                result = e.input_environment

            successes += 1 if e.output_environment.correct(result) else 0

        successes /= len(test_case.test_examples)

        return successes, execution_time_in_seconds

    def _eval_experiment(self, experiment: Experiment):
        res = list(map(self._eval_test_case, experiment.test_cases))

        ave_suc = mean([e[0] for e in res])
        ave_time = mean([e[1] for e in res])
        per_suc = mean([1 if e[0] == 1 else 0 for e in res])

        return ave_suc, ave_time, per_suc
