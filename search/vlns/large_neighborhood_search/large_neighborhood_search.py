import time

from common.experiment import Example
from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken, BoolToken, TransToken
from search.abstract_search import SearchAlgorithm
from search.search_result import SearchResult
from search.vlns.large_neighborhood_search.accept.accept import Accept
from search.vlns.large_neighborhood_search.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search.invent.invent import Invent
from search.vlns.large_neighborhood_search.invent.variable_depth_invent import VariableDepthInvent
from search.vlns.large_neighborhood_search.repair.repair import Repair


class LNS(SearchAlgorithm):
    """Implements the abstract Large Neighborhood Search algorithm given an Accept, Destroy and Repair method. Also a
    time limit can be set."""

    def __init__(self, time_limit: float, accept: Accept, destroy: Destroy, repair: Repair, invent: Invent,
                 increase_depth_after: int, debug: bool = False):
        super().__init__(time_limit)

        # Init given parameters
        self.accept = accept
        self.destroy = destroy
        self.repair = repair
        self.invent = invent
        self.increase_depth_after = increase_depth_after
        self.debug = debug

        # Make sure repair can access invent
        self.repair.invent = invent

        # Init needed variables
        self.sol_current = None
        self.cost_best = -1
        self.cost_current = -1

        self.iterations_since_last_best = 0

        self.stats = {}

    def setup(self, test_case: list[Example], trans_tokens: list[TransToken], bool_tokens: list[BoolToken]):
        self.invent.setup(trans_tokens, bool_tokens)
        self.accept.reset()
        self.destroy.reset()
        self.repair.reset()

        self._best_program = Program([])
        self.sol_current = Program([])
        self.cost_best = self.cost(exs=test_case, p=self._best_program)
        self.cost_current = self.cost_best

        self.cost_dict = {}
        self.iterations_since_last_best = 0

        self.number_of_iterations = 0
        self.number_of_explored_programs = 0
        self.stats["search_depth"] = 1
        self.stats["time_destroy"] = 0
        self.stats["time_repair"] = 0
        self.stats["time_cost"] = 0
        self.stats["explored_per_size_tokens"] = []
        self.stats["explored_per_size_sequence"] = []
        self.cost_per_iteration = []

    def iteration(self, test_case: list[Example], tokens: list[EnvToken], bt) -> bool:
        if self.cost_best == 0:
            return False

        self.debug_print("\n")
        self.debug_print("-=-=-=[Iteration {}]=-=-=-".format(self.number_of_iterations))
        self.debug_print("Program ({}): {}".format(self.cost_current, self.sol_current))
        t_b = time.process_time()

        # Destroy current solution
        destroyed = self.destroy.destroy(self.sol_current)
        t_d = time.process_time()
        self.debug_print("Destroyed: {}".format(destroyed))

        # Repair destroyed solution into temporary solution
        x_temp = self.repair.repair(destroyed)
        t_r = time.process_time()

        # Calculate cost of temporary solution
        #c_temp = self.cost(test_case, x_temp)
        c_temp = self.eff_cost(test_case, x_temp)
        t_c = time.process_time()
        self.debug_print("Repaired ({}): {}".format(c_temp, x_temp))

        # New best solution found
        if c_temp < self.cost_best:
            self.cost_best = c_temp
            self._best_program = x_temp

            self.iterations_since_last_best = 0

            pair = (self.number_of_iterations, self.cost_best.__round__(2))
            self.cost_per_iteration.append(pair)
        else:
            self.iterations_since_last_best += 1

            if self.iterations_since_last_best >= self.increase_depth_after:
                self.stats["search_depth"] += 1

                self.destroy.increment_search_depth()
                self.repair.increment_search_depth()
                self.invent.increment_depth()

                self.iterations_since_last_best = 0

        # Accepted as new current solution
        if self.accept.accept(self.cost_current, c_temp, self.sol_current, x_temp):
            self.sol_current = x_temp
            self.cost_current = c_temp

        # Update stats
        self.number_of_iterations += 1
        self.stats["time_destroy"] += t_d - t_b
        self.stats["time_repair"] += t_r - t_d
        self.stats["time_cost"] += t_c - t_r

        # Repeat if no fully correct solution found
        return c_temp != 0

    def extend_result(self, res: SearchResult) -> SearchResult:
        # Round times for readability
        self.stats["time_destroy"] = self.stats["time_destroy"].__round__(3)
        self.stats["time_repair"] = self.stats["time_repair"].__round__(3)
        self.stats["time_cost"] = self.stats["time_cost"].__round__(3)

        self.stats.update(res.dictionary)
        res.dictionary = self.stats

        return res

    def debug_print(self, msg: str):
        if self.debug:
            print(msg)

    cost_dict = {}

    def eff_cost(self, test_case: list[Example], program: Program):
        key = str(program)

        if key not in self.cost_dict:
            self.cost_dict[key] = self.cost(test_case, program)

            self.number_of_explored_programs += 1

            st = program.number_of_tokens()
            ss = len(program.sequence)

            while len(self.stats["explored_per_size_tokens"]) <= st:
                self.stats["explored_per_size_tokens"].append(0)

            while len(self.stats["explored_per_size_sequence"]) <= ss:
                self.stats["explored_per_size_sequence"].append(0)

            self.stats["explored_per_size_tokens"][st] += 1
            self.stats["explored_per_size_sequence"][ss] += 1

        return self.cost_dict[key]
