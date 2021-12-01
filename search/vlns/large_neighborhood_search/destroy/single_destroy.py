from random import random

from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search.tokens.destroyed_token import DestroyedEnvToken, DestroyedBoolToken
from search.vlns.large_neighborhood_search.tokens.sequence_token import SequenceToken, EmptySequenceToken, SeqToken


class SingleDestroy(Destroy):
    """Destroys single tokens at random."""

    def __init__(self, p_env: float, p_bool: float):
        """Initializes a new ProbabilisticProgramDestroy class. Tokens are destroyed with a probability of `prob`. If
        desired one can set the chance of destroying an environment token and boolean token separately with p_env and
        p_bool respectively."""
        assert 0 <= p_env <= 1
        assert 0 <= p_bool <= 1

        self.p_env = p_env
        self.p_bool = p_bool

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        if isinstance(seq, EmptySequenceToken):
            return seq

        # Destroy head
        if random() <= self.p_env:
            seq.head = DestroyedEnvToken(seq.head)
        elif isinstance(seq.head, If):
            seq.head.cond = DestroyedBoolToken(seq.head.cond) if random() <= self.p_bool else seq.head.cond
            seq.head.e1 = [self.destroy_sequence(seq.head.e1[0])]
            seq.head.e2 = [self.destroy_sequence(seq.head.e2[0])]
        elif isinstance(seq.head, LoopWhile):
            seq.head.cond = DestroyedBoolToken(seq.head.cond) if random() <= self.p_bool else seq.head.cond
            seq.head.loop_body = [self.destroy_sequence(seq.head.loop_body[0])]

        # Destroy tail
        seq.tail = self.destroy_sequence(seq.tail)

        # Return
        return seq
