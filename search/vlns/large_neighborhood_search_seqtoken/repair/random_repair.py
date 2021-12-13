from random import random

from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search_seqtoken.repair.repair import Repair
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken, SequenceToken, RemoveToken


class RandomRepair(Repair):

    def __init__(self, w_if: float, w_loop: float, w_remove: float, w_split: float, w_default: float):
        w_tot = w_if + w_loop + w_remove + w_split + w_default
        p_if = w_if / w_tot
        p_loop = w_loop / w_tot
        p_remove = w_remove / w_tot
        p_split = w_split / w_tot

        self.c_if = p_if
        self.c_loop = p_loop + self.c_if
        self.c_remove = p_remove + self.c_loop
        self.c_split = p_split + self.c_remove

        super().__init__()

    def repair_sequence(self, destroyed: SeqToken) -> SeqToken:
        return self._repair_sequence(destroyed, destroyed)

    def _repair_sequence(self, destroyed: SeqToken, program_head: SeqToken) -> SeqToken:
        if len(destroyed) == 0:
            return destroyed

        # Repair head if needed
        if isinstance(destroyed.head, DestroyedToken):
            old_head = destroyed.head.destroyed_token
            r = random()

            if r < self.c_if:
                destroyed.head = self.random_if_token()
            elif r < self.c_loop:
                destroyed.head = self.random_loop_token()
            elif r < self.c_remove:
                if isinstance(destroyed.tail, SequenceToken):
                    destroyed.head = destroyed.tail.head
                    destroyed.tail = destroyed.tail.tail

                    return self._repair_sequence(destroyed, program_head)
                else:
                    destroyed.head = RemoveToken()

                    return destroyed
            elif r < self.c_split:
                destroyed.head = self.env_token_sample(1)[0]
                destroyed.tail = SequenceToken(self.env_token_sample(1)[0], destroyed.tail)
            else:
                destroyed.head = self.env_token_sample(1)[0]

            # Check if extending the program actually made the program better. If not, remove.
            if old_head is None and False:
                new_cost = self.seq_cost(program_head)

                if self.current_cost <= new_cost:
                    destroyed.head = RemoveToken()

        elif isinstance(destroyed.head, If):
            if isinstance(destroyed.head.cond, DestroyedToken):
                destroyed.head.cond = self.bool_token_sample(1)[0]

            destroyed.head.e1 = [self._repair_sequence(destroyed.head.e1[0], program_head)]
            destroyed.head.e2 = [self._repair_sequence(destroyed.head.e2[0], program_head)]

        elif isinstance(destroyed.head, LoopWhile):
            if isinstance(destroyed.head.cond, DestroyedToken):
                destroyed.head.cond = self.bool_token_sample(1)[0]

            destroyed.head.loop_body = [self._repair_sequence(destroyed.head.loop_body[0], program_head)]

        # Repair tail if needed
        if isinstance(destroyed.tail, SequenceToken):
            destroyed.tail = self._repair_sequence(destroyed.tail, program_head)

        return destroyed
