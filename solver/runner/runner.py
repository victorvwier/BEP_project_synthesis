import os
from multiprocessing import Pool
from statistics import mean

from solver.runner.algorithms import dicts
from solver.runner.file_manager import FileManager
from solver.runner.test_case_retriever import get_test_cases


class Runner:

    def __init__(self, lib, algo: str, setting: str, test_cases: str, time_limit_sec: float, debug: bool = False, store: bool = True, suffix: str = ""):
        self.time_limit_sec = time_limit_sec
        self.debug = debug
        self.store = store

        self.algorithm = lib["algorithms"][algo][setting]
        self.settings = lib["settings"][setting]
        self.files = lib["test_cases"][test_cases][setting[0]]

        self.file_manager = FileManager(algo, setting, suffix)

    def run(self):
        Runner.algo = self.algorithm

        if self.debug:
            print("Parsing test cases")

        exclude = self.file_manager.finished_test_cases() if self.store else []
        all_cases = get_test_cases(self.settings.domain, self.files, exclude)

        if self.debug:
            print("Parsed {} test cases".format(len(all_cases)))

        if len(all_cases) == 0:
            print("All test cases were already run")
            return 0, 0

        total_examples = [0] * len(self.files[2])
        solved_examples = [0] * len(self.files[2])

        for i, trial in enumerate(self.files[2]):
            if self.debug:
                print("Running trial #{}...".format(trial))

            cases = [tc for tc in all_cases if tc.index[2] == trial]

            if len(cases) == 0:
                print("All test cases were already run")
                total_examples[i] = 0
                solved_examples[i] = -1
                continue

            with Pool(processes=os.cpu_count() - 1) as pool:
                results = pool.map_async(self.execute_test_case, cases)
            #if True:
                #results = [self.execute_test_case(c) for c in cases]

                stats_list = []
                for program, stats in results.get():
                    stats_list.append(stats)

                    total_examples[i] += stats["test_total"]
                    solved_examples[i] += stats["test_correct"]

                if self.store:
                    self.file_manager.append_result(stats_list)

        accuracies = [float(s) / t for s, t in zip(solved_examples, total_examples)]

        return mean(accuracies)

    def execute_test_case(self, test_case):
        return self.algorithm.run(self.settings, self.time_limit_sec, self.debug, test_case)


if __name__ == "__main__":
    time_limit = 30
    debug = False
    store = False
    setting = "PG"
    algo = "MCTS"
    test_cases = "param"
    params = [0, 0.1, 0.5, 1, 1.5, 2]
    #params = [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3]
    #0.05

    params = params if test_cases == "param" else [0]
    store = False if test_cases == "param" else store

    for param in params:
        if test_cases == "param":
            print("\nParam = {}".format(param))

        mean1 = Runner(dicts(param), algo, setting, test_cases, time_limit, debug, store).run()

        print("Solved {}".format((100*mean1).__round__(1)))