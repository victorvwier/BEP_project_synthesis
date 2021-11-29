import time
from typing import TypeVar

from interpreter.interpreter import Program
from parser.experiment import TestCase
from vlns.large_neighborhood_search.accept.accept import Accept
from vlns.large_neighborhood_search.cost import Cost
from vlns.large_neighborhood_search.destroy import Destroy
from vlns.large_neighborhood_search.repair import Repair
from vlns.search import ProgramSearch

T = TypeVar('T')


class LNS(ProgramSearch):

    def __init__(self, domain: str, accept: Accept, destroy: Destroy, repair: Repair, cost: Cost, max_iterations: int, max_token_function_depth: int):
        super().__init__(domain, max_token_function_depth, cost)
        self.domain = domain
        self.accept = accept
        self.destroy = destroy
        self.repair = repair
        self.max_iterations = max_iterations

    def find(self, initial_solution: Program, test_case: TestCase) -> Program:
        t_d, t_r, t_c = 0, 0, 0

        self.repair.cost = lambda p: self.cost.cost(p, test_case)

        x_best = initial_solution
        c_best = self.cost.cost(x_best, test_case)
        x_current = initial_solution
        c_current = c_best

        for i in range(1, self.max_iterations + 1):
            # Destroy and repair current solution.
            t_d1 = time.time()
            d_temp = self.destroy.destroy(x_current)
            t_dr2 = time.time()
            x_temp = self.repair.repair(d_temp)
            t_rc3 = time.time()
            c_temp = self.cost.cost(x_temp, test_case)
            t_c4 = time.time()

            t_d += t_dr2 - t_d1
            t_r += t_rc3 - t_dr2
            t_c += t_c4 - t_rc3

            # Correct solution found
            if c_current == 0:
                print("Destroy: {}, repair: {}, cost: {}".format(t_d, t_r, t_c))
                return x_current

            # If temp solution is accepted, change current to temp.
            if self.accept.accept(c_current, c_temp, x_current, x_temp, i):
                x_current = x_temp
                c_current = c_temp

            # If temp is better than best, change best to temp.
            if c_temp < c_best:
                x_best = x_temp
                c_best = c_temp

        # Return best found when iteration limit is reached.
        print("Destroy: {}, repair: {}, cost: {}".format(t_d, t_r, t_c))
        return x_best
