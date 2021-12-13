import random

from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken
from search.vlns.large_neighborhood_search.repair.repair import Repair


class InsertNRepair2(Repair):

    def __init__(self, initial_max_n, max_max_n: int, w_trans: float, w_if: float, w_loop: float):
        assert initial_max_n >= 0

        super().__init__()

        self.max_n = initial_max_n
        self.max_max_n = max_max_n

        self.w_trans = w_trans
        self.w_if = w_if
        self.w_loop = w_loop

    def repair(self, seqs: list[list[EnvToken]]) -> Program:
        assert len(seqs) == 2

        seq = seqs[0]

        # Pick N, minimum of 1
        n = random.randint(1, self.max_n + 1)

        for _ in range(n):
            seq.append(self.random_token(w_trans=self.w_trans, w_if=self.w_if, w_loop=self.w_loop))

        seq.extend(seqs[1])

        return Program(seq)

    def increment_search_depth(self):
        if self.max_n != self.max_max_n:
            self.max_n += 1
