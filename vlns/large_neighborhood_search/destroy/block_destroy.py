import random

from common_environment.control_tokens import *
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.destroy.destroy import Destroy


class BlockDestroy(Destroy):
    """Destroy method that destroys entire blocks. Blocks are sequences of tokens separated by ControlTokens
    (If, Loop)."""

    def __init__(self, p_destroy: float):
        """Initializes the BlockDestroy method. A chance 'p_destroy' is given that denotes the chance that a block will
        be destroyed."""
        assert 0 <= p_destroy <= 1

        self.p_destroy = p_destroy
        self._destroying = False

    def seq_setup(self, seq: list[Token]):
        self._destroying = random.random() < self.p_destroy

    def destroy_env_if(self, seq: list[Token], token: Token, index: int) -> bool:
        # If token is ControlToken the block end. A new setup is needed and the token is not destroyed.
        if isinstance(token, ControlToken):
            self.seq_setup(seq)
            return False
        else:
            return self._destroying

    def destroy_bool_if(self, seq: list[Token], token: Token, control_token: Token, index: int) -> bool:
        # Conditions are not considered blocks and will therefore never change
        return False

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
        MoveLeft(), MoveLeft(), MoveLeft(), MoveLeft(),
    ])

    d = BlockDestroy(p_destroy=0.5)

    d.destroy(p)

    print(str(p))