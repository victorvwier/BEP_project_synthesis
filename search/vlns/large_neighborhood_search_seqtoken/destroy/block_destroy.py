from random import random

from common.tokens.control_tokens import LoopWhile, If
from search.vlns.large_neighborhood_search_seqtoken.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedEnvToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import EmptySequenceToken, SeqToken


class BlockDestroy(Destroy):
    """Destroy method that destroys entire blocks. Blocks are sequences of tokens separated by ControlTokens
    (If, Loop)."""

    def __init__(self, p_destroy: float):
        """Initializes the BlockDestroy method. A chance 'p_destroy' is given that denotes the chance that a block will
        be destroyed."""
        assert 0 <= p_destroy <= 1

        self.p_destroy = p_destroy
        self._destroying = False

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        return self.destroy_sequence_block(seq, random() <= self.p_destroy)

    def destroy_sequence_block(self, seq: SeqToken, destroying: bool) -> SeqToken:
        if isinstance(seq, EmptySequenceToken):
            return seq

        # Destroy head
        if isinstance(seq.head, If):
            seq.head.e1 = [self.destroy_sequence(seq.head.e1[0])]
            seq.head.e2 = [self.destroy_sequence(seq.head.e2[0])]
            seq.tail = self.destroy_sequence(seq.tail)
            return seq
        elif isinstance(seq.head, LoopWhile):
            seq.head.loop_body = [self.destroy_sequence(seq.head.loop_body[0])]
            seq.tail = self.destroy_sequence(seq.tail)
            return seq
        elif destroying:
            seq.head = DestroyedEnvToken(seq.head)

        seq.tail = self.destroy_sequence_block(seq.tail, destroying)

        # Return
        return seq
