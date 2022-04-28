import random

from common.program import Program, EnvToken
from common.settings.settings import Settings
from solver.search.search_algorithm import SearchAlgorithm


class LNS(SearchAlgorithm):

    def __init__(self, max_destroy_n: int, max_repair_n: int):
        self.max_destroy_n = max_destroy_n
        self.max_repair_n = max_repair_n

    def setup(self):
        pass

    def iteration(self) -> bool:
        # Destroy and repair best solution
        new_program = self._repair(self._destroy(self.best_program))

        # Evaluate, best program will be set by SearchAlgorithm.evaluate
        self.evaluate(new_program)

        # Keep running until cost is zero
        return self.best_cost != 0

    def _destroy(self, program: Program) -> (list[EnvToken], list[EnvToken]):
        # Pick N
        mn = min(self.max_destroy_n, len(program.sequence))
        n = random.randint(0, mn + 1)

        # Pick index of first to be destroyed token
        i = random.randint(0, len(program.sequence) - n + 1)

        # Return slice of part before destroyed and after
        return program.sequence[:i], program.sequence[i + n:]

    def _repair(self, seqs: (list[EnvToken], list[EnvToken])) -> Program:
        seq = seqs[0]

        # Pick N, minimum of 1
        n = random.randint(1, self.max_repair_n + 1)

        # Append N random tokens
        for _ in range(n):
            seq.append(random.choice(self.tokens))

        # Extend sequence and return program
        seq.extend(seqs[1])
        return Program(seq)