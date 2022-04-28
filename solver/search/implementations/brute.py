import heapq

from common.settings.settings import Settings
from common.settings.string_levenshtein import StringLevenshtein
from common.settings.string_optimized_alignment import StringOptimizedAlignment
from common.environment.string_environment import StringEnvironment
from common.experiment import Example
from common.program import Program
from common.tokens.abstract_tokens import EnvToken, BoolToken, TransToken
from common.tokens.string_tokens import TransTokens, BoolTokens
from solver.search.search_algorithm import SearchAlgorithm


class Brute(SearchAlgorithm):

    def __init__(self):
        self.program_heap = []
        self.visited_states = []

    def setup(self):
        self.program_heap = [(self.best_cost, self.best_program)]
        heapq.heapify(self.program_heap)

        self.visited_states = [self.best_state]

    def iteration(self) -> bool:
        cost, program = heapq.heappop(self.program_heap)

        # If solution
        if cost == 0:
            return False

        for token in self.tokens:
            new_program = Program(program.sequence + [token])
            new_cost, new_state, _ = self.evaluate(new_program)
            self.statistics["no._explored_programs"] += 1

            if new_state not in self.visited_states:
                heapq.heappush(self.program_heap, (new_cost, new_program))
                self.visited_states.append(new_state)

        return len(self.program_heap) > 0