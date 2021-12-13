from random import random

from common.tokens.control_tokens import If, LoopWhile, EnvToken, BoolToken
from search.vlns.large_neighborhood_search_seqtoken.repair.repair import Repair
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SequenceToken, SeqToken, RemoveToken


class StochasticSingleRepair(Repair):

    def __init__(self, p_if: float, p_loop: float, p_remove: float, p_split: float,
                 n_if: int, n_loop: int, n_bool: int, n_env: int):
        super().__init__()

        assert 0 <= p_if <= 1
        assert 0 <= p_loop <= 1
        assert 0 <= p_remove <= 1
        assert 0 <= p_split <= 1
        assert p_if + p_loop + p_remove + p_split <= 1

        self.c_if = p_if
        self.c_loop = p_loop + self.c_if
        self.c_remove = p_remove + self.c_loop
        self.c_split = p_split + self.c_remove

        self.n_if = n_if
        self.n_loop = n_loop
        self.n_bool = n_bool
        self.n_env = n_env

    def repair_sequence(self, destroyed: SequenceToken) -> SeqToken:
        return self._repair_sequence(destroyed, destroyed)

    def _repair_sequence(self, program_head: SeqToken, destroyed: SeqToken) -> SeqToken:
        if len(destroyed) == 0:
            return destroyed

        # Repair head if needed
        if isinstance(destroyed.head, DestroyedToken):
            r = random()

            if r < self.c_if:
                ifs = [self.random_if_token() for _ in range(self.n_if)]
                destroyed.head = self._stochastic_search_env(program_head, destroyed, ifs)
            elif r < self.c_loop:
                loops = [self.random_loop_token() for _ in range(self.n_loop)]
                destroyed.head = self._stochastic_search_env(program_head, destroyed, loops)
            elif r < self.c_remove:
                if isinstance(destroyed.tail, SequenceToken):
                    destroyed.head = destroyed.tail.head
                    destroyed.tail = destroyed.tail.tail

                    return self.repair_sequence(destroyed)
                else:
                    destroyed.head = RemoveToken()

                    return destroyed
            elif r < self.c_split:
                envs = self.env_token_sample(self.n_env)
                destroyed.head = self._stochastic_search_env(program_head, destroyed, envs)
                destroyed.tail = SequenceToken(self.env_token_sample(1)[0], destroyed.tail)
            else:
                envs = self.env_token_sample(self.n_env)
                destroyed.head = self._stochastic_search_env(program_head, destroyed, envs)

        elif isinstance(destroyed.head, If):
            if isinstance(destroyed.head.cond, DestroyedToken):
                bools = self.bool_token_sample(self.n_bool)
                destroyed.head.cond = self._stochastic_search_bool(program_head, destroyed, bools)

            destroyed.head.e1 = [self._repair_sequence(program_head, destroyed.head.e1[0])]
            destroyed.head.e2 = [self._repair_sequence(program_head, destroyed.head.e2[0])]

        elif isinstance(destroyed.head, LoopWhile):
            if isinstance(destroyed.head.cond, DestroyedToken):
                bools = self.bool_token_sample(self.n_bool)
                destroyed.head.cond = self._stochastic_search_bool(program_head, destroyed, bools)

            destroyed.head.loop_body = [self._repair_sequence(program_head, destroyed.head.loop_body[0])]

        # Repair tail if needed
        if isinstance(destroyed.tail, SequenceToken):
            destroyed.tail = self.repair_sequence(destroyed.tail)

        return destroyed

    def _stochastic_search_env(self, program_head: SeqToken, destroyed: SequenceToken, tokens: list[EnvToken]) -> EnvToken:
        t_best = RemoveToken()
        c_best = self.cost(program_head)

        for t_current in tokens:
            destroyed.head = t_current
            c_current = self.cost(program_head)

            if c_current < c_best:
                t_best = t_current
                c_best = c_current

        destroyed.head = t_best

        return t_best

    def _stochastic_search_bool(self, program_head: SeqToken, destroyed: SequenceToken, tokens: list[BoolToken]) -> EnvToken:
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