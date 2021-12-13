from math import exp, ceil

import numpy as np

from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search_seqtoken.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedEnvToken, DestroyedBoolToken, \
    DestroyedToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SequenceToken, EmptySequenceToken, SeqToken


class SingleStochasticDestroy(Destroy):
    """Destroys single tokens at random."""

    def __init__(self, f_destroy: float, temperature: float):
        super().__init__()
        """Initializes a new SingleStochasticDestroy class. 'f_destroy' is the fraction of tokens destroyed. Tokens are
        destroyed randomly with weights determining the distribution. Weights are given by exp(cost / temp), where the
        cost is the cost as if the token is removed."""
        assert 0 <= f_destroy <= 1

        self.f_destroy = f_destroy
        self.temperature = temperature

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        if len(seq) == 0:
            return seq

        prev = None
        current = seq
        size = 0
        weights = []
        tokens = []

        # Traverse sequence and build up weight list
        while len(current) > 0:
            size += 1
            tokens.append(current)
            weights.append(exp(- self.cost(current) / self.temperature))

            if isinstance(current.head, If):
                current.head.e1 = [self.destroy_sequence(current.head.e1[0])]
                current.head.e2 = [self.destroy_sequence(current.head.e2[0])]
            elif isinstance(current.head, LoopWhile):
                current.head.loop_body = [self.destroy_sequence(current.head.loop_body[0])]

            prev = current
            current = current.tail

        if sum(weights) == 0:
            weights[0] = 1

        # Select tokens to be destroyed
        n_destroy = ceil(self.f_destroy * size)
        to_destroy = np.random.choice(tokens, n_destroy, p=[w / sum(weights) for w in weights])

        # Destroy tokens
        for t in to_destroy:
            t.head = DestroyedEnvToken(t.head)

        # Append one destroyed for sequence extending
        if prev is not None:
            prev.tail = SequenceToken(DestroyedToken(destroyed_token=None), EmptySequenceToken())

        # Return
        return seq
