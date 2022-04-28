import copy
import heapq
from math import exp

from common.program import Program, InvalidTransition
from common.settings.settings import Settings
from common.tokens.control_tokens import LoopIterationLimitReached
from solver.search.search_algorithm import SearchAlgorithm


class AStar(SearchAlgorithm):

    def __init__(self, weight: float):
        assert 0 <= weight <= 1

        self.weight = weight

        self.open_states = []
        self.came_from = {}
        self.token = {}
        self.g_score = {}
        self.f_score = {}

    def setup(self):
        # Add empty program as start node

        self.open_states = []
        self.came_from = {}
        self.token = {}
        self.g_score = {}
        self.f_score = {}

        self.open_states = [(self.best_cost * (1 - self.weight), self.best_state)]
        self.g_score[self.best_state] = 0
        self.f_score[self.best_state] = self.best_cost

        heapq.heapify(self.open_states)

    def iteration(self):
        _, state = heapq.heappop(self.open_states)

        if self.f_score[state] == 0:
            self.best_program = self._reconstruct_program(state)
            self.best_cost = 0

            return False

        for token in self.tokens:
            try:
                new_state = tuple(map(token.apply, copy.deepcopy(state)))
            except (InvalidTransition, LoopIterationLimitReached):
                continue

            # Path is shorter
            if self.g_score[state] + 1 < self.g_score.get(new_state, float("inf")):
            #if new_state not in self.f_score:
                self.came_from[new_state] = state
                self.token[new_state] = token
                self.g_score[new_state] = self.g_score[state] + 1 - exp(- 0.3 * token.number_of_tokens())
                self.f_score[new_state] = self.evaluate_state(new_state)

                new_cost = self.g_score[new_state] * self.weight + self.f_score[new_state] * (1 - self.weight)

                heapq.heappush(self.open_states, (new_cost, new_state))

        return len(self.open_states) > 0

    def _reconstruct_program(self, state):
        program = []

        while state in self.came_from:
            program.append(self.token[state])
            state = self.came_from[state]

        program.reverse()

        return Program(program)
