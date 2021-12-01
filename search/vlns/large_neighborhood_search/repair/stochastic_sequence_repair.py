from random import random

from common.tokens.abstract_tokens import EnvToken, BoolToken
from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search.repair.repair import Repair
from search.vlns.large_neighborhood_search.tokens.destroyed_token import DestroyedToken
from search.vlns.large_neighborhood_search.tokens.sequence_token import SequenceToken, SeqToken


class StochasticSequenceRepair(Repair):

    def __init__(self, max_sequence_size: int, n_bool: int, n_seq: int, p_if: float, p_loop: float, p_remove: float, p_split: float):
        assert 0 <= p_if <= 1
        assert 0 <= p_loop <= 1
        assert 0 <= p_remove <= 1
        assert 0 <= p_split <= 1
        assert p_if + p_loop + p_remove + p_split <= 1

        super().__init__()

        self.max_sequence_size = max_sequence_size

        self.c_if = p_if
        self.c_loop = p_loop + self.c_if
        self.c_remove = p_remove + self.c_loop
        self.c_split = p_split + self.c_remove

        self.n_seq = n_seq
        self.n_bool = n_bool

    def repair_sequence(self, destroyed: SequenceToken) -> SeqToken:
        return self._repair_sequence(destroyed, destroyed)

    def _repair_sequence(self, program_head: SeqToken, destroyed: SequenceToken) -> SeqToken:
        if len(destroyed) == 0:
            return destroyed

        # Repair head if needed
        if isinstance(destroyed.head, DestroyedToken):
            self._stochastic_insert_seq(program_head, destroyed)

        # Repair If token
        elif isinstance(destroyed.head, If):
            if isinstance(destroyed.head.cond, DestroyedToken):
                bools = self.bool_token_sample(self.n_bool)
                destroyed.head.cond = self._stochastic_search_bool(program_head, destroyed, bools)

            destroyed.head.e1 = [self._repair_sequence(program_head, destroyed.head.e1[0])]
            destroyed.head.e2 = [self._repair_sequence(program_head, destroyed.head.e2[0])]

        # Repair Loop token
        elif isinstance(destroyed.head, LoopWhile):
            if isinstance(destroyed.head.cond, DestroyedToken):
                bools = self.bool_token_sample(self.n_bool)
                destroyed.head.cond = self._stochastic_search_bool(program_head, destroyed, bools)

            destroyed.head.loop_body = [self._repair_sequence(program_head, destroyed.head.loop_body[0])]

        # Repair tail if needed
        if isinstance(destroyed.tail, SequenceToken):
            destroyed.tail = self.repair_sequence(destroyed.tail)

        return destroyed

    def _stochastic_insert_seq(self, program_head: SeqToken, destroyed: SequenceToken):
        size = min(self.max_sequence_size, self._destroyed_sequence_size(destroyed))

        s_best = self._random_sequence(size)
        self._insert_sequence(destroyed, s_best, 0)
        c_best = self.cost(program_head)

        for _ in range(0, self.n_seq):
            s_current = self._random_sequence(size)
            self._insert_sequence(destroyed, s_current, 0)
            c_current = self.cost(program_head)

            if c_current < c_best:
                s_best = s_current
                c_best = c_current

        self._insert_sequence(destroyed, s_best, 0)

    def _stochastic_search_bool(self, program_head: SeqToken, destroyed: SequenceToken, tokens: list[BoolToken]):
        t_best = destroyed.head.cond.destroyed_token
        c_best = self.cost(program_head)

        for t_current in tokens:
            destroyed.head.cond = t_current
            c_current = self.cost(program_head)

            if c_current < c_best:
                t_best = t_current
                c_best = c_current

        destroyed.head.cond = t_best
        return t_best

    @staticmethod
    def _insert_sequence(seq_token: SeqToken, seq: list[EnvToken], i: int):
        if len(seq_token) == 0 or len(seq) == i:
            return

        seq_token.head = seq[i]

        StochasticSequenceRepair._insert_sequence(seq_token.tail, seq, i + 1)

    @staticmethod
    def _destroyed_sequence_size(seq_token: SeqToken):
        if len(seq_token) == 0 or not isinstance(seq_token.head, DestroyedToken):
            return 0

        return 1 + StochasticSequenceRepair._destroyed_sequence_size(seq_token.tail)

    def _random_sequence(self, size: int) -> list[EnvToken]:
        res = []

        for _ in range(size):
            r = random()

            if r < self.c_if:
                res.append(self.random_if_token())
            elif r < self.c_loop:
                res.append(self.random_loop_token())
            elif r < self.c_remove:
                continue
            elif r < self.c_split:
                res.append(self.env_token_sample(1)[0])
                res.append(self.env_token_sample(1)[0])
            else:
                res.append(self.env_token_sample(1)[0])

        return res
