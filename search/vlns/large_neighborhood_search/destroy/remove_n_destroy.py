from random import random, choices

from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken
from search.vlns.large_neighborhood_search.destroy.destroy import Destroy


class ExtractNDestroy(Destroy):
    """For each token in the program, an extraction will happen with probability p_extract. If an extraction occurs; a
    random N is selected from n_options according to weight distribution n_weight. N tokens, including the current
    token, will be removed from the sequence splitting the sequence.

    This destroy method runs in O(n), where n is the sequence size.
    """

    def __init__(self, p_extract: float, n_options: list[int], n_weights):
        """See class documentation."""
        assert 0 <= p_extract <= 1

        super().__init__()

        self.p_extract = p_extract
        self.n_options = n_options
        self.n_weights = n_weights

    def destroy(self, program: Program) -> list[list[EnvToken]]:
        seq = program.sequence
        res = [[]]

        index = 0

        while index < len(seq):
            # Start extracting if this yields True.
            if random() < self.p_extract:
                # Pick N according to weights
                n = choices(self.n_options, weights=self.n_weights)[0]

                # Lower N if it is larger than amount of remaining tokens
                n = min(n, len(seq) - index)

                # Skip n tokens
                index += n

                # Create new empty sub sequence
                res.append([])

            # Else add the token to the last sub sequence
            else:
                res[len(res) - 1].append(seq[index])
                index += 1

        # Append empty sequence.
        # - This will make sure the repair method can always stitch at least two subsequences together.
        if len(res) == 1:
            res.append([])

        return res

    def set_search_depth(self, n: int):
        self.n_weights = [1] * (n+1)
        self.n_options = range(0, n+1)
