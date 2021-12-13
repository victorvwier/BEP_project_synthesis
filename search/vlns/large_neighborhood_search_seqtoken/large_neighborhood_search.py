import copy
import time
from statistics import mean

from common.experiment import TestCase, Example
from common.prorgam import Program
from common.tokens.abstract_tokens import Token, EnvToken, BoolToken, InvalidTransition
from common.tokens.control_tokens import LoopIterationLimitReached, StringEnvironment

from search.abstract_search import SearchAlgorithm
from search.search_result import SearchResult
from search.vlns.large_neighborhood_search_seqtoken.accept.accept import Accept
from search.vlns.large_neighborhood_search_seqtoken.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search_seqtoken.repair.repair import Repair
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken


class LNS(SearchAlgorithm):

    def __init__(self, time_limit: float, accept: Accept, destroy: Destroy, repair: Repair, debug: bool = False):
        super().__init__(time_limit)
        self.accept = accept
        self.destroy = destroy
        self.repair = repair
        self.debug = debug

        self.c_best = float('inf')
        self.x_current = None
        self.c_current = float('inf')
        self.iteration_number = 1

        self.best_cost_per_iteration = []
        self.current_cost_per_iteration = []

        self.time_destroy = 0
        self.time_repair = 0
        self.time_cost = 0

        self.repair.lns = self
        self.seq_cost = lambda s: -1

    def setup(self, test_case: list[Example], trans_tokens: set[EnvToken], bool_tokens: set[BoolToken]):
        self.repair.set_seq_cost(lambda s: self.cost_seq(test_case, s))
        self.repair.set_token_libraries(trans_tokens, bool_tokens)
        self.destroy.cost = lambda s: self.cost_seq(test_case, s)

        self.c_best = self.cost(test_case, self.best_program)
        self.x_current = Program([])
        self.c_current = self.c_best
        self.iteration_number = 1

        self.best_cost_per_iteration = []
        self.current_cost_per_iteration = []

        self.time_destroy = 0
        self.time_repair = 0
        self.time_cost = 0

    def iteration(self, test_case: list[Example], trans_tokens: set[EnvToken], bool_tokens: set[BoolToken]) -> bool:
        self.repair.set_current_cost(self.c_current)

        if self.debug:
            print("\n")
            print("-=-=-=[Iteration {}]=-=-=-".format(self.iteration_number))
            print("Program ({}): {}".format(self.c_current, self.x_current))
        t_b = time.process_time()

        destroyed = self.destroy.destroy(self.x_current)
        t_d = time.process_time()
        self.time_destroy += (t_d - t_b)
        if self.debug:
            print("Destroyed: {}".format(destroyed))

        x_temp = self.repair.repair(destroyed)
        t_r = time.process_time()
        self.time_repair += (t_r - t_d)

        c_temp = self.cost(test_case, x_temp)
        t_c = time.process_time()
        self.time_cost += (t_c - t_r)
        if self.debug:
            print("Repaired ({}): {}".format(c_temp, x_temp))

        self.best_cost_per_iteration.append(self.c_best.__round__(1))
        self.current_cost_per_iteration.append(self.c_current.__round__(1))

        # New best solution found
        if c_temp < self.c_best:
            self.c_best = c_temp
            self._best_program = copy.deepcopy(x_temp)

        # Accepted as new current solution
        if self.accept.accept(self.c_current, c_temp, self.x_current, x_temp, self.iteration_number):
            self.x_current = x_temp
            self.c_current = c_temp

        self.iteration_number += 1

        # Repeat if no fully correct solution found
        return c_temp != 0

    def extend_result(self, res: SearchResult) -> SearchResult:
        res.dictionary["best_cost_per_iteration"] = self.best_cost_per_iteration
        res.dictionary["current_cost_per_iteration"] = self.current_cost_per_iteration
        res.dictionary["time_destroy"] = self.time_destroy
        res.dictionary["time_repair"] = self.time_repair
        res.dictionary["time_cost"] = self.time_cost
        res.dictionary["iterations"] = self.iteration_number - 1
        res.dictionary["program_length"] = self._best_program.number_of_tokens(1)

        return res

    @staticmethod
    def cost_seq(tc: list[Example], seq: SeqToken):
        def ex_cost(ex: Example):
            try:
                inp = copy.deepcopy(ex.input_environment)
                return seq.apply(inp).distance(ex.output_environment)
            except (InvalidTransition, LoopIterationLimitReached):
                return float('inf')

        return mean([ex_cost(ex) for ex in tc])