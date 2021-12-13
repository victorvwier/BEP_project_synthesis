import copy
import random
from collections import Set, Callable

from common.prorgam import Program, EnvToken, BoolToken, Token
from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken, SequenceToken, EmptySequenceToken


class Repair:

    def __init__(self):
        self.env_tokens = set()
        self.env_tokens: Set[EnvToken]
        self.bool_tokens = set()
        self.bool_tokens: Set[BoolToken]

        self.cost: Callable[[SeqToken], float]
        self.cost = lambda p: -1

        self.seq_cost = None

        self.current_cost = 0

        self._ifs = None
        self._loops = None

    def repair(self, destroyed: SeqToken) -> Program:
        """Repairs a given `destroyed_solution'. Returns the repaired solution."""

        if self._ifs is None:
            self._ifs = self._all_ifs()
            self._loops = self._all_loops()

        if isinstance(destroyed, EmptySequenceToken):
            destroyed = SequenceToken(self.env_token_sample(1)[0], destroyed)

        return Program(self.repair_sequence(destroyed).to_list())

    def set_seq_cost(self, cost: Callable[[SeqToken], float]):
        self.seq_cost = cost

    def set_current_cost(self, cost: float):
        self.current_cost = cost

    def repair_sequence(self, destroyed: SequenceToken) -> SeqToken:
        raise NotImplementedError()

    def set_token_libraries(self, env_tokens: set[EnvToken], bool_tokens: set[BoolToken]):
        self.env_tokens = env_tokens
        self.bool_tokens = bool_tokens

    def env_token_sample(self, k: int) -> list[EnvToken]:
        return random.sample(self.env_tokens, min(k, len(self.env_tokens)))

    def bool_token_sample(self, k: int) -> list[BoolToken]:
        return random.sample(self.bool_tokens, min(k, len(self.bool_tokens)))

    def random_if_token(self) -> If:
        return copy.copy(random.sample(self._ifs, 1)[0])

    def random_loop_token(self) -> LoopWhile:
        return copy.copy(random.sample(self._loops, 1)[0])

    def _all_ifs(self) -> list[If]:
        res = []

        for cond in self.bool_tokens:
            for e1 in self.env_tokens:
                for e2 in self.env_tokens:
                    res.append(If(cond,
                                  [SequenceToken(e1, EmptySequenceToken())],
                                  [SequenceToken(e2, EmptySequenceToken())]))

        return res

    def _all_loops(self):
        res = []

        for cond in self.bool_tokens:
            for lb in self.env_tokens:
                res.append(LoopWhile(cond, [SequenceToken(lb, EmptySequenceToken())]))

        return res
