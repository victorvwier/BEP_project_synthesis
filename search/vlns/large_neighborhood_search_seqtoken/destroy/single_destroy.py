from random import random

from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search_seqtoken.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedEnvToken, DestroyedBoolToken, \
    DestroyedToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SequenceToken, SeqToken, EmptySequenceToken


class SingleDestroy(Destroy):
    """Destroys single tokens at random."""

    def __init__(self, prob: float):
        """Initializes a new SingleDestroy class. Tokens are destroyed randomly with a probability of `prob`."""
        super().__init__()
        assert 0 <= prob <= 1

        self.prob = prob

    def destroy_sequence(self, seq: SequenceToken) -> SeqToken:
        if len(seq) == 0:
            return seq

        # Destroy head with prob.
        if random() <= self.prob:
            seq.head = DestroyedEnvToken(seq.head)
        # Recursively destroy if token bodies.
        elif isinstance(seq.head, If) and False:
            seq.head.e1 = [self.destroy_sequence(seq.head.e1[0])]
            seq.head.e2 = [self.destroy_sequence(seq.head.e2[0])]
        # Recursively destroy loop token body.
        elif isinstance(seq.head, LoopWhile) and False:
            seq.head.loop_body = [self.destroy_sequence(seq.head.loop_body[0])]

        # Extend sequence by 1 and return if the end of sequence is encountered.
        if len(seq.tail) == 0:
            seq.tail = SequenceToken(DestroyedToken(destroyed_token=None), EmptySequenceToken())
            return seq

        # Destroy tail
        seq.tail = self.destroy_sequence(seq.tail)

        # Return
        return seq
