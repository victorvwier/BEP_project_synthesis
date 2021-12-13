from random import random

from common.tokens.control_tokens import If, LoopWhile
from search.vlns.large_neighborhood_search_seqtoken.repair.repair import Repair
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken, SequenceToken, RemoveToken


class ShrinkRepair(Repair):

    def __init__(self, p_extract: float):
        assert 0 <= p_extract <= 1

        super().__init__()

        self.p_extract = p_extract

    def repair_sequence(self, destroyed: SequenceToken) -> SeqToken:
        return self._repair_sequence(destroyed, destroyed)

    def _repair_sequence(self, destroyed: SeqToken, program_head: SequenceToken) -> SeqToken:
        if len(destroyed) == 0:
            return destroyed

        # Repair head if needed
        if isinstance(destroyed.head, DestroyedToken):
            r = random()
            t = destroyed.head.destroyed_token

            # If If-token encountered, replace head with one of two branches randomly
            if r < self.p_extract and isinstance(t, If):
                destroyed.head = t.e1[0] if random() < 0.5 else t.e2[0]

            # If While-token encountered, replace head with loop body
            elif r < self.p_extract and  isinstance(t, LoopWhile):
                destroyed.head = t.loop_body[0]

            # Else a normal token is encountred
            else:
                """
                # Cost with token
                cost_with = self.cost(program_head)

                old_token = t
                destroyed.head = RemoveToken()

                # Cost without token
                cost_without = self.cost(program_head)

                # Bring back old token if cost is better
                if cost_with < cost_without:
                    destroyed.head = old_token
                """
                if t is not None:
                    destroyed.head = t
                else:
                    destroyed.head = RemoveToken()

        elif isinstance(destroyed.head, If):
            destroyed.head.e1 = [self.repair_sequence(destroyed.head.e1[0])]
            destroyed.head.e2 = [self.repair_sequence(destroyed.head.e2[0])]

        elif isinstance(destroyed.head, LoopWhile):
            destroyed.head.loop_body = [self.repair_sequence(destroyed.head.loop_body[0])]

        # Repair tail if needed
        if isinstance(destroyed.tail, SequenceToken):
            destroyed.tail = self.repair_sequence(destroyed.tail)

        return destroyed
