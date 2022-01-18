import heapq
import copy
import json
import os
import time
from collections import Iterable, Set
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
                 file_name: str = "",
                 multi_core: bool = True,
                 print_results: bool = False):

        self.domain = domain
        self.search_algorithm = search_algorithm
        self.algorithm_name = self._get_algorithm_name(search_algorithm)
        self.file_name = file_name
        self.files = self._complement_iters(domain, files)
        self.multi_core = multi_core
        self.print_results = print_results

        self.parser = self._get_parser(domain)

        self.token_library = extract_trans_tokens_from_domain_name(domain)
        self.bools = extract_bool_tokens_from_domain_name(domain)

        self.path = ""
        self.append_to_file = self.file_name != ""
        self._init_store_system()

        self.test_cases = self._get_test_cases()

    def run(self) -> dict:
        results = []
        correct_results = []
        not_correct_results = []
        correct = 0

        if self.multi_core:
            with Pool(processes=os.cpu_count() - 1) as pool:
                # collect results sorted and in chunks to minimize communication overhead on HPC
                for i, d in enumerate(pool.imap(self._test_case, self.test_cases, chunksize=10)):
                    self.debug_print(f"{self.search_algorithm.__class__.__name__} {i}: {d['file']}, test_cost: {d['test_cost']}, train_cost: {d['train_cost']}, time: {d['execution_time']}, length: {d['program_length']}, iterations: {d['number_of_iterations']}")
                    self._store_result(d)
                    results.append(d)
        else:
            for tc in self.test_cases:
                res = self._test_case(tc)
                results.append(res)

                self.debug_print(
                    f"{self.search_algorithm.__class__.__name__}: {res['file']}, test_cost: {res['test_cost']}, train_cost: {res['train_cost']}, time: {res['execution_time']}, length: {res['program_length']}, iterations: {res['number_of_iterations']}, initial error: {res['initial_error']}")

        for res in results:
            if res['test_cost'] == 0 and res['train_cost'] == 0:
                correct += 1
                correct_results.append(res)
            else:
                not_correct_results.append(res)

        s = len(self.test_cases)
        p = -1 if s == 0 else (100 * correct / s).__round__(1)
        self.debug_print("{} / {} ({}%) cases solved.".format(correct, s, p))

        keys = ["test_cost", "train_cost", "execution_time", "program_length", "number_of_explored_programs",
                "number_of_iterations"]
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

        return final

    def _test_case(self, test_case: TestCase) -> dict:
        search_algorithm = copy.deepcopy(self.search_algorithm)
        result = search_algorithm.run(test_case.training_examples, self.token_library, self.bools).dictionary
        program = result["program"]
        result["program"] = str(program)

        ca = test_case.path_to_result_file.split("-")

        d = {
            "file": "{}-{}-{}".format(ca[1], ca[2], ca[3]),
            "test_cost": SearchAlgorithm.cost(test_case.test_examples, program),
            "train_cost": SearchAlgorithm.cost(test_case.training_examples, program),
            "execution_time": result["execution_time"],
            "program_length": result["program_length"],
            "number_of_explored_programs": result["number_of_explored_programs"],
        }

        d.update(result)
        return d

    def _init_store_system(self):
        folder = "{}/results/{}".format(os.getcwd(), self.domain)

        if not os.path.exists(folder):
            os.makedirs(folder)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        if self.file_name == "":
            self.file_name = "{}-{}.txt".format(self.algorithm_name, timestr)
            self.last_stored = None

        self.path = "{}/{}".format(folder, self.file_name)

    def _store_result(self, res: dict):
        with open(self.path, "a") as file:
            file.write(json.dumps(res))
            file.write("\n")

    def _get_test_cases(self) -> list[TestCase]:
        all = self.parser.parse_specific_range(self.files[0], self.files[1], self.files[2])

        if not self.append_to_file:
            return all

        seen = set()

        with open(self.path, "r") as file:
            for line in file.readlines():
                obj = json.loads(line[:-1])
                seen.add(self._get_file_index(obj))

        res = []

        for tc in all:
            if tc.index not in seen:
                res.append(tc)

        return res

    def _sort_file(self):
        res = []

        with open(self.path, "r") as file:
            for line in file.readlines():
                obj = json.loads(line[:-1])
                res.append(obj)

        res = sorted(res, key=self._get_file_index)

        with open(self.path, "w") as file:
            for r in res:
                file.write(json.dumps(r))
                file.write("\n")

    def debug_print(self, msg: str):
        if self.print_results:
            print(msg)

    @staticmethod
    def _get_file_index(res: dict) -> (int, int, int):
        name = res["file"].split("/")[1][:-3]
        i = name.split("-")
        return int(i[0]), int(i[1]), int(i[2])

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
            def_iter = range(1, 10), chain(range(1, 278), range(279, 328)), range(1, 10)
        elif domain == "robot":
            def_iter = [2, 4, 6, 8, 10], range(0, 10), range(0, 11)
        elif domain == "pixel":
            def_iter = [1, 2, 3, 4, 5], range(0, 10), range(1, 11)
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
