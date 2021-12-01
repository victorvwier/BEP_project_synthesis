import random

from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search.tokens.destroyed_token import DestroyedEnvToken
from search.vlns.large_neighborhood_search.tokens.sequence_token import SeqToken, EmptySequenceToken


class SequenceDestroy(Destroy):
    """Destructs a sequence of a random size between 2 and a given max sequence size."""

    def __init__(self, max_seq_size: int, p_destroy: float):
        """Initializes the sequence destroy method that destructs a subsequence inside a program. Since a Program"""
        assert max_seq_size >= 2
        assert 0 <= p_destroy <= 1

        self.max_seq_size = max_seq_size
        self.p_destroy = p_destroy

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        # When no sequence is destroyed
        if random.random() > self.p_destroy:
            return seq

        length = len(seq)

        # Min size 2 or seq size if that is lower
        min_size = min(length, 2)

        # Max size is given max size or seq size if that is lower
        max_size = min(self.max_seq_size, length)

        # Select random size
        amount = random.randint(min_size, max_size)

        # Select random start point
        start = random.randint(0, length - amount)

        return self.destroy_sequence_seq(seq, start, amount)

    def destroy_sequence_seq(self, seq: SeqToken, index: int, amount: int) -> SeqToken:
        if isinstance(seq, EmptySequenceToken):
            return seq

        if index == 0 and amount > 0:
            seq.head = DestroyedEnvToken(seq.head)
            amount -= 1
            index += 1
        elif isinstance(seq.head, If):
            seq.head.e1 = [self.destroy_sequence(seq.head.e1[0])]
            seq.head.e2 = [self.destroy_sequence(seq.head.e2[0])]
        elif isinstance(seq.head, LoopWhile):
            seq.head.loop_body = [self.destroy_sequence(seq.head.loop_body[0])]

        seq.tail = self.destroy_sequence_seq(seq.tail, index - 1, amount)

        # Return
        return seq
