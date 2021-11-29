import random

from common_environment.control_tokens import If
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.destroy.destroy import Destroy


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

    def seq_setup(self, seq: list[Token]):
        return

    def destroy_env_if(self, seq: list[Token], token: Token, index: int) -> bool:
        return random.random() < self.p_env

    def destroy_bool_if(self, seq: list[Token], token: Token, control_token: Token, index: int) -> bool:
        return random.random() < self.p_bool


if __name__ == "__main__":
    p = Program([
        MoveLeft(), MoveRight(), MakeUppercase(), MakeLowercase(),
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

    d = SingleDestroy(p_env=0.5, p_bool=0.5)

    d.destroy(p)

    print(str(p))