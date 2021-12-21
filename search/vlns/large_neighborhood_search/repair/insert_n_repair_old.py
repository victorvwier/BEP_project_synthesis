import random

from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken
from search.vlns.large_neighborhood_search.repair.repair import Repair


class InsertNRepairOld(Repair):
    """For each token list (except last), an insertion occurs; a random N is selected from n_options according to
    weight distribution n_weight. N tokens will be inserted after the sequence stitching the sequence together.

    This repair method runs in O(n + m), where n is the total number of tokens in subsequences and m the number of
    subsequences.
    """

    def __init__(self, n_options: list[int], n_weights: list[float], w_trans: float, w_if: float, w_loop: float):
        super().__init__()

        self.n_options = n_options
        self.n_weights = n_weights

        self.w_trans = w_trans
        self.w_if = w_if
        self.w_loop = w_loop

    def repair(self, seqs: list[list[EnvToken]]) -> Program:
        res = []

        # Iterate over each subsequence
        for i, seq in enumerate(seqs):

            # Extend final sequence with subsequence
            res.extend(seq)

            # If current seq is not the last one it is possible to insert tokens between two sequences.
            if i < len(seqs) - 1:

                # Pick N according to weights
                n = random.choices(self.n_options, weights=self.n_weights)[0]

                # If n is 0 and no tokens were in the original sequence, make sure some token will be added.
                if n == 0 and len(seqs) == 2 and len(seqs[0]) == len(seqs[1]) == 0:
                    n = 1

                # Append N tokens to final sequence
                while n > 0:
                    res.append(self.random_token(w_trans=self.w_trans, w_if=self.w_if, w_loop=self.w_loop))
                    n -= 1

        return Program(res)

    def set_search_depth(self, n: int):
        self.n_weights = [1] * (n+1)
        self.n_options = range(0, n+1)
