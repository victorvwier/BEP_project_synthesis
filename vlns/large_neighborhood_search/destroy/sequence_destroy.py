import random

from common_environment.abstract_tokens import Token
from common_environment.control_tokens import If
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.destroy.destroy import Destroy


class SequenceDestroy(Destroy):
    """Destructs a sequence of a random size between 2 and a given max sequence size."""

    def __init__(self, max_seq_size: int, p_destroy: float):
        """Initializes the sequence destroy method that destructs a subsequence inside a program. Since a Program"""
        assert max_seq_size >= 2
        assert 0 <= p_destroy <= 1

        self.max_seq_size = max_seq_size
        self.p_destroy = p_destroy
        self.start = 0
        self.end = 0

    def seq_setup(self, seq: list[Token]):
        # When no sequence is destroyed
        if random.random() >= self.p_destroy:
            self.start = -1
            self.end = -1

            return

        length = len(seq)

        # Min size 2 or seq size if that is lower
        min_size = min(length, 2)

        # Max size is given max size or seq size if that is lower
        max_size = min(self.max_seq_size, length)

        # Select random size
        size = random.randint(min_size, max_size)

        # Select random start point
        self.start = random.randint(0, length - size)
        self.end = self.start + size

    def destroy_env_if(self, seq: list[Token], token: Token, index: int) -> bool:
        return self.start <= index < self.end

    def destroy_bool_if(self, seq: list[Token], token: Token, control_token: Token, index: int) -> bool:
        return self.start <= index < self.end


if __name__ == "__main__":
    p = Program([
        MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(),
        LoopWhile(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ),
        If(
            AtStart(),
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()],
            [MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft()]
        ),
    ])

    d = SequenceDestroy(max_seq_size=3, p_destroy=0.5)

    d.destroy(p)

    print(str(p))
