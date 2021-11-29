import random

from common_environment.abstract_tokens import Token, ControlToken, BoolToken, EnvToken
from interpreter.interpreter import Program
from parser.string_parser import StringParser
from string_environment.string_tokens import Drop, MoveRight
from vlns.large_neighborhood_search.cost import Cost
from vlns.large_neighborhood_search.destroy.destroyed import DiscardToken, DestroyedToken
from vlns.large_neighborhood_search.repair.repair import Repair


class SingleStochasticRepair(Repair):

    def __init__(self, domain: str, max_function_token_depth: int, n_env: int, n_bool: int, p_invented: float = 0):
        assert n_env > 0
        assert n_bool > 0
        assert 0 <= p_invented <= 1

        super().__init__(domain, max_function_token_depth)

        self.n_env = n_env
        self.n_bool = n_bool
        self.p_invented = p_invented

    def repair_destroyed_env(self, seq: list[EnvToken], token: DestroyedToken, index: int) -> EnvToken:
        tokens = [DiscardToken()]
        tokens += self.random_invented(self.n_env) if random.random() <= self.p_invented else self.random_env(self.n_env)

        def set_token(t: Token):
            seq[index] = t

        best_index = self._find_best(seq, [lambda _, __: set_token(t) for t in tokens])

        return tokens[best_index]

    def repair_destroyed_bool(self, seq: list[EnvToken], control_token: ControlToken, index: int) -> BoolToken:
        tokens = self.random_bool(self.n_bool)

        def set_token(t: Token):
            control_token.cond = t

        best_index = self._find_best(seq, [lambda _, __: set_token(t) for t in tokens])

        return tokens[best_index]


if __name__ == "__main__":
    p = Program(
            [DestroyedToken(MoveRight()), DestroyedToken(MoveRight()), DestroyedToken(MoveRight())]
        )

    r = SingleStochasticRepair(
        domain="string",
        max_function_token_depth=3,
        p_invented=0.1,
        n_bool=10,
        n_env=10,
    )

    pars = StringParser(
        path="../../../programs/e2-strings/data/train/",
    )
    pars.test_path="../../../programs/e2-strings/data/test/"

    r.cost = lambda p: Cost().cost(p, pars.parse_file("1-1-1.pl"))
    res = r.repair(p.sequence)

    print(str(res))