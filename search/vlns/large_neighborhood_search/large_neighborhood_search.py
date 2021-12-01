import copy
from statistics import mean

from common.experiment import TestCase, Example
from common.prorgam import Program
from common.tokens.abstract_tokens import Token, EnvToken, BoolToken

from search.abstract_search import Search
from search.search_result import SearchResult
from search.vlns.large_neighborhood_search.accept.accept import Accept
from search.vlns.large_neighborhood_search.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search.repair.repair import Repair
from search.vlns.large_neighborhood_search.tokens.sequence_token import SeqToken


class LNS(Search):

    def __init__(self, time_limit: float, accept: Accept, destroy: Destroy, repair: Repair):
        super().__init__(time_limit)
        self.accept = accept
        self.destroy = destroy
        self.repair = repair

        self.x_best = None
        self.c_best = float('inf')
        self.x_current = None
        self.c_current = float('inf')
        self.iteration_number = 1

        self.best_cost_per_iteration = []
        self.current_cost_per_iteration = []

    def setup(self, test_case: TestCase, trans_tokens: set[EnvToken], bool_tokens: set[BoolToken]):
        self.repair.set_token_libraries(trans_tokens, bool_tokens)
        self.repair.cost = lambda s: self.cost_train(test_case, s)

        self.x_best = Program([])
        self.c_best = self.cost_train(test_case, self.x_best)
        self.x_current = Program([])
        self.c_current = self.c_best
        self.iteration_number = 1

        self.best_cost_per_iteration = []
        self.current_cost_per_iteration = []

    def iteration(self, test_case: TestCase, trans_tokens: set[EnvToken], bool_tokens: set[BoolToken]) -> bool:
        destroyed = self.destroy.destroy(self.x_current)
        x_temp = self.repair.repair(destroyed)
        c_temp = self.cost_train(test_case, x_temp)

        self.best_cost_per_iteration.append(self.c_best.__round__(1))
        self.current_cost_per_iteration.append(self.c_current.__round__(1))

        # New best solution found
        if c_temp < self.c_best:
            self.x_best = x_temp
            self.c_best = c_temp

            self._best_program = copy.deepcopy(self.x_best)

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

        return res

    @staticmethod
    def cost_seq(tc: TestCase, seq: SeqToken):
        def ex_cost(ex: Example):
            try:
                return seq.apply(ex.input_environment).distance(ex.output_environment)
            except:
                return float('inf')

        return mean([ex_cost(ex) for ex in tc.training_examples])