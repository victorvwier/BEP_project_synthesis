from typing import Callable, List, Tuple

from common.settings import settings
from common.settings.settings import Settings
from common.settings.string_levenshtein import StringLevenshtein
from common.tokens.abstract_tokens import InvalidTransition
from common.program import Program
from common.experiment import Example
from solver.search.search_algorithm import SearchAlgorithm
import random
import math


class MetropolisHasting(SearchAlgorithm):
    def __init__(self, alpha: float):
        self.alpha = alpha

        self.current_program = Program([])
        self.current_cost = 0

        self.weights_and_mutations = [
            (30, self._append_token),
            (5, self._insert_token),
            (20, self._remove_last_token),
            (5, self._remove_random_token),
            (2, self._reset),
        ]

        self.weights = [w for w, _ in self.weights_and_mutations]
        self.mutations = [m for _, m in self.weights_and_mutations]

    def setup(self):
        self.current_program = Program([])
        self.current_cost, _, _ = self.evaluate(self.current_program)

    def iteration(self) -> bool:
        mutation = random.choices(self.mutations, weights=self.weights, k=1)[0]

        new_program = mutation(self.current_program)
        new_cost, _, _ = self.evaluate(new_program)

        ratio = math.exp(-self.alpha * new_cost) / math.exp(-self.alpha * self.current_cost)
        if ratio > 1 or random.random() < ratio:
            self.current_program = new_program
            self.current_cost = new_cost

        return self.best_cost != 0

    # Mutations from here
    def _append_token(self, program: Program) -> Program:
        return Program(program.sequence + [random.choice(self.tokens)])

    def _insert_token(self, program: Program) -> Program:
        index = random.randint(0, len(program.sequence))

        return Program(program.sequence[:index] + [random.choice(self.tokens)] + program.sequence[index:])

    def _remove_last_token(self, program: Program) -> Program:
        return Program(program.sequence[:-1])

    def _remove_random_token(self, program: Program) -> Program:
        index = random.randint(0, len(program.sequence))

        return Program(program.sequence[:index] + program.sequence[index + 1:])

    def _reset(self, program: Program) -> Program:
        return Program([])


if __name__ == "__main__":
    algo = MetropolisHasting(StringLevenshtein(), 10, False, 1.2)
    program = Program(random.sample(algo.tokens, k=4))

    print("Program: {}".format(program))
    for mutation in algo.mutations:
        print("Mutations {}: {}".format(str(mutation), mutation(program)))

