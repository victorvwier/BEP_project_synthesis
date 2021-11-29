import random

from common_environment.control_tokens import *
from interpreter.interpreter import Program
from parser.string_parser import StringParser
from string_environment.string_tokens import *
from vlns.large_neighborhood_search.cost import Cost
from vlns.large_neighborhood_search.destroy.destroyed import DestroyedToken
from vlns.large_neighborhood_search.implementations.wat_is_een_goeie_naam.marked_token import IdToken
from vlns.large_neighborhood_search.repair.single_stochastic_repair import SingleStochasticRepair


class SequenceStochasticRepair(SingleStochasticRepair):

    def __init__(self, domain: str, max_function_token_depth: int, max_sequence_size: int, n_env: int, n_bool: int, p_invented: float = 0):
        super().__init__(domain, max_function_token_depth, n_env, n_bool, p_invented)

        self.max_sequence_size = max_sequence_size

        self.sequence_size = 0
        self.tuple = []

    def repair_destroyed_env(self, seq: list[EnvToken], token: DestroyedToken, index: int) -> EnvToken:
        if not isinstance(seq[index], DestroyedToken):
            return seq[index]

        if self.sequence_size == 0:
            while index + self.sequence_size < len(seq) and \
                    isinstance(seq[index + self.sequence_size], DestroyedToken) and \
                    self.sequence_size < self.max_sequence_size:
                self.sequence_size += 1

            tuples = [[IdToken()] * self.sequence_size]
            tuples += [self.random_invented(self.sequence_size) if random.random() <= self.p_invented
                      else self.random_env(self.sequence_size) for _ in range(self.n_env)]

            self.tuple = seq[index:index+self.sequence_size]
            best_cost = self.cost(Program(seq))
            for t in tuples:
                self._sub_tuple(seq, index, t)
                cost = self.current_cost()

                if cost < best_cost:
                    self.tuple = t
                    best_cost = cost

                if cost == 0:
                    break

        self.sequence_size -= 1

        if self.tuple is None:
            return token.destroyed_token

        t = self.tuple[len(self.tuple) - self.sequence_size - 1]

        return t.destroyed_token if isinstance(t, DestroyedToken) else t

    @staticmethod
    def _sub_tuple(seq: list[Token], index: int, tuple: list[Token]):
        i = index

        for t in tuple:
            seq[i] = t
            i += 1


if __name__ == "__main__":
    p = Program(
            [DestroyedToken(MoveRight()), DestroyedToken(MoveRight()), DestroyedToken(MoveRight())]
        )

    r = SequenceStochasticRepair(
        domain="string",
        max_function_token_depth=3,
        p_invented=0.1,
        n_bool=10,
        n_env=100,
        max_sequence_size=2
    )

    pars = StringParser(
        path="../../../programs/e2-strings/data/train/",
    )
    pars.test_path="../../../programs/e2-strings/data/test/"

    r.cost = lambda p: Cost().cost(p, pars.parse_file("1-1-1.pl"))
    res = r.repair(p.sequence)

    print(str(res))