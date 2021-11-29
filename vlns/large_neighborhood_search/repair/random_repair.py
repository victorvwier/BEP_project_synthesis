import random

from common_environment.control_tokens import If
from interpreter.interpreter import Program
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.destroy.destroyed import DestroyedToken
from vlns.large_neighborhood_search.repair.single_stochastic_repair import SingleStochasticRepair


class RandomRepair(SingleStochasticRepair):

    def __init__(self, domain: str, max_function_token_depth: int, p_invented: float = 0):
        super().__init__(domain, max_function_token_depth, n_env=1, n_bool=1, p_invented=p_invented)


if __name__ == "__main__":
    p = Program([
        DestroyedToken(MoveLeft()), DestroyedToken(MoveLeft()), DestroyedToken(MoveLeft()), MoveLeft(),
        LoopWhile(
            AtStart(),
            [DestroyedToken(MoveLeft()), MoveLeft(), DestroyedToken(MoveLeft()), MoveLeft()]
        ),
        If(
            AtStart(),
            [DestroyedToken(MoveLeft()), DestroyedToken(MoveLeft()), DestroyedToken(MoveLeft()), MoveLeft()],
            [MoveLeft(), DestroyedToken(MoveLeft()), MoveLeft(), DestroyedToken(MoveLeft())]
        ),
        MoveLeft(), DestroyedToken(MoveLeft()), MoveLeft(), MoveLeft(),
    ])

    r = RandomRepair(domain="string", max_function_token_depth=3, p_invented=0.1).repair(p.sequence)

    print(str(r))