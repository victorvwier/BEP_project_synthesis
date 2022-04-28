import copy
import random
from collections import defaultdict
from math import log, sqrt

from numpy.ma import argmax, argmin

from common.program import Program
from common.settings.settings import Settings
from common.tokens.abstract_tokens import Token, InvalidTransition
from common.tokens.control_tokens import LoopIterationLimitReached
from solver.search.search_algorithm import SearchAlgorithm


class MCTS(SearchAlgorithm):

    def __init__(self, settings: Settings, time_limit_sec: float, debug: bool, c_exploration: float, rollout_depth: int):
        super().__init__(settings, time_limit_sec, debug)

        self.c_exploration = c_exploration
        self.rollout_depth = rollout_depth

        self.initial_state = None

        # Setup MCTS dictionaries
        self.came_from = {}
        self.children = {}
        self.token = {}
        self.legal_tokens = {}
        self.mcts_cost = {}
        self.visits = {}
        self.absolute_cost = {}

    def setup(self):
        self.initial_state = tuple([ex.input_environment for ex in self.training_examples])
        self.absolute_cost[self.initial_state] = self.evaluate_state(self.initial_state)

        for token in self.tokens:
            try:
                tuple(map(token.apply, copy.deepcopy(self.initial_state)))
                self.legal_tokens.get(self.initial_state, []).append(token)
            except (InvalidTransition, LoopIterationLimitReached):
                continue

    def iteration(self):
        print("Iteration {}".format(self.statistics["no._iterations"]))

        state = self._tree_policy(self.initial_state)

        print("State = {}".format(state))

        self._rollout(state)

        print("Rollout done")

        self._backpropagate(state)

        print("Rollout cost = {}".format(self.mcts_cost[state]))

        if self.absolute_cost[state] == 0:
            self.best_program = self._reconstruct_program(state)

            return False

        return True

    def _expand(self, state: tuple):
        token = self.legal_tokens.pop(0)

        try:
            new_state = tuple(map(token.apply, copy.deepcopy(state)))
        except (InvalidTransition, LoopIterationLimitReached):
            return self._tree_policy(self.initial_state)

        if new_state in self.absolute_cost:
            return self._tree_policy(self.initial_state)

        self.came_from[new_state] = state
        self.children.get(state, []).append(new_state)

        self.token[new_state] = token

        for token in self.tokens:
            try:
                tuple(map(token.apply, copy.deepcopy(state)))
                self.legal_tokens.get(state, []).append(token)
            except (InvalidTransition, LoopIterationLimitReached):
                continue

        self.absolute_cost[new_state] = self.evaluate_state(new_state)
        self.mcts_cost[new_state] = 0

        return new_state

    def _rollout(self, state: tuple):
        depth = 0

        while self.absolute_cost[state] != 0 and depth < self.rollout_depth:
            depth += 1

            try:
                state = tuple(map(self._rollout_policy(state).apply, copy.deepcopy(state)))
            except (InvalidTransition, LoopIterationLimitReached):
                continue

            if state not in self.absolute_cost:
                self.absolute_cost[state] = self.evaluate_state(state)

    def _rollout_policy(self, state: tuple) -> Token:
        return random.choice(self.tokens)

    def _backpropagate(self, state: tuple):
        cost = self.absolute_cost[state]

        while state in self.came_from:
            self.visits[state] = 1 + self.visits.get(state, 0) + 1
            self.mcts_cost[state] = cost + self.mcts_cost.get(state, 0)
            state = self.came_from[state]

    def _is_fully_expanded(self, state):
        return len(self.legal_tokens) == 0

    def _best_child(self, state):
        return self.children[argmin([self._mcts_evaluate(c, state) for c in self.children[state]])]

    def _mcts_evaluate(self, state: tuple, parent: tuple):
        q = self.mcts_cost[state]
        nc = self.visits[state]
        np = self.visits[parent]

        return q / nc + self.c_exploration * sqrt(2 * log(float(np) / nc))

    def _tree_policy(self, state: tuple):

        while self.absolute_cost[state] != 0:
            if not self._is_fully_expanded(state):
                return self._expand(state)
            else:
                state = self._best_child(state)

        return state

    def _reconstruct_program(self, state):
        program = []

        while state in self.came_from:
            program.append(self.token[state])
            state = self.came_from[state]

        program.reverse()

        return Program(program)