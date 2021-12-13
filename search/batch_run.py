import json
import os
import time
from collections import Iterable
from itertools import chain
from multiprocessing import Pool

from evaluation.experiment_procedure import extract_trans_tokens_from_domain_name, extract_bool_tokens_from_domain_name
from example_parser.parser import Parser, TestCase
from example_parser.pixel_parser import PixelParser
from example_parser.robot_parser import RobotParser
from example_parser.string_parser import StringParser
from search.MCTS.mcts import MCTS
from search.a_star.a_star import AStar
from search.abstract_search import SearchAlgorithm
from search.brute.brute import Brute
from search.gen_prog.vanilla_GP import VanillaGP
from search.metropolis_hastings.metropolis import MetropolisHasting
from search.vlns.large_neighborhood_search.algorithms.remove_n_insert_n import RemoveNInsertN


class BatchRun:

    def __init__(self,
                 domain: str,
                 files: (Iterable[int], Iterable[int], Iterable[int]),
                 search_algorithm: SearchAlgorithm,
                 multi_core: bool = True,
                 print_results: bool = False):
        self.domain = domain
        self.search_algorithm = search_algorithm
        self.algorithm_name = self._get_algorithm_name(search_algorithm)
        self.files = self._complement_iters(domain, files)
        self.multi_core = multi_core
        self.print_results = print_results

        self.parser = self._get_parser(domain)
        self.test_cases = self._get_test_cases(self.files)

        self.token_library = extract_trans_tokens_from_domain_name(domain)
        self.bools = extract_bool_tokens_from_domain_name(domain)

    def run(self) -> dict:
        results = []
        correct_results = []
        not_correct_results = []
        correct = 0

        if self.multi_core:
            with Pool(processes=os.cpu_count() - 1) as pool:
                for tc in self.test_cases:
                    res = pool.apply_async(self._test_case, (tc,))
                    results.append(res)

                results = [r.get() for r in results]
        else:
            for tc in self.test_cases:
                res = self._test_case(tc)
                results.append(res)

        for res in results:
            if res['test_cost'] == 0 and res['train_cost'] == 0:
                correct += 1
                correct_results.append(res)
            else:
                not_correct_results.append(res)

            #self.debug_print(str(res))

        s = len(self.test_cases)
        p = (100 * correct / s).__round__(1)
        self.debug_print("{} / {} ({}%) cases solved.".format(correct, s, p))

        keys = ["test_cost", "train_cost", "execution_time", "program_length", "visited_programs", "iterations"]
        ave_res = self._average(results, keys)
        ave_cor = self._average(correct_results, keys)
        ave_ncor = self._average(not_correct_results, keys)

        self.debug_print("Average overall: {}".format(ave_res))
        self.debug_print("Average correct: {}".format(ave_cor))
        self.debug_print("Average not correct: {}".format(ave_ncor))

        final = {
            "domain": self.domain,
            "files": str(self.files),
            "average": ave_res,
            "average_correct": ave_cor,
            "average_failed": ave_ncor,
            "results": results,
        }

        self._store_results(final)

        return final

    def _test_case(self, test_case: TestCase) -> dict:
        result = self.search_algorithm.run(test_case.training_examples, self.token_library, self.bools).dictionary
        program = result["program"]
        result["program"] = str(program)

        ca = test_case.path_to_result_file.split("-")

        d = {
            "file": "{}-{}-{}".format(ca[1], ca[2], ca[3]),
            "test_cost": SearchAlgorithm.cost(test_case.test_examples, program),
            "train_cost": SearchAlgorithm.cost(test_case.training_examples, program),
            "execution_time": result["execution_time"],
            "program_length": result["program_length"],
            "visited_programs": result["visited_programs"],
        }

        d.update(result)
        #d["failed_train_outputs"] = []
        #d["failed_test_outputs"] = []

        for ex in test_case.training_examples:
            env = program.interp(ex.input_environment)
            if ex.output_environment.distance(env) > 0:
                d["failed_train_outputs"].append(env)

        for ex in test_case.test_examples:
            try:
                env = program.interp(ex.input_environment)

                if ex.output_environment.distance(env) > 0:
                    d["failed_test_outputs"].append(env)
            except:
                d["failed_test_outputs"].append("Failed for: {}".format(ex.input_environment))

        self.debug_print(str(d))

        return d

    def _get_test_cases(self, files: (Iterable[int], Iterable[int], Iterable[int])) -> list[TestCase]:
        res = []

        for i1 in files[0]:
            for i2 in files[1]:
                for i3 in files[2]:
                    res.append(self.parser.parse_file("{}-{}-{}.pl".format(i1, i2, i3)))

        return res

    def _store_results(self, res: dict):
        path = "{}/results/{}".format(os.getcwd(), self.domain)

        if not os.path.exists(path):
            os.makedirs(path)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        file_name = "{}-{}.json".format(self.algorithm_name, timestr)

        with open("{}/{}".format(path, file_name), "w") as file:
            file.write(json.dumps(res))

    def debug_print(self, msg: str):
        if self.print_results:
            print(msg)

    @staticmethod
    def _average(dicts: list[dict], keys: list[str]):
        res = {k: 0 for k in keys}

        for d in dicts:
            for k in keys:
                if d[k] != float('inf'):
                    res[k] += d[k] / len(dicts)

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

    @staticmethod
    def _complement_iters(domain: str, iters: (Iterable[int], Iterable[int], Iterable[int])):
        def_iter = None

        if domain == "string":
            def_iter = range(1, 10), chain(range(1, 278), range(279, 328)), range(1,10)
        elif domain == "robot":
            def_iter = [2,4,6,8,10], range(0, 10), range(0, 11)
        elif domain == "pixel":
            def_iter = [1,2,3,4,5], range(0, 10), range(1, 11)
        else:
            raise Exception()

        return (
            def_iter[0] if len(iters[0]) == 0 else iters[0],
            def_iter[1] if len(iters[1]) == 0 else iters[1],
            def_iter[2] if len(iters[2]) == 0 else iters[2]
        )

    @staticmethod
    def _get_algorithm_name(algo: SearchAlgorithm):
        map = {
            MetropolisHasting: "metro",
            Brute: "brute",
            MCTS: "mcts",
            VanillaGP: "gp",
            RemoveNInsertN: "VLNS",
            AStar: "Astar",
        }

        return map[algo.__class__]