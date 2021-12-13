import random
from collections import Callable

from common.prorgam import Program
from common.tokens.abstract_tokens import EnvToken, BoolToken
from search.vlns.large_neighborhood_search_seqtoken.repair.repair import Repair
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken, SequenceToken


class MultiMethodRepair(Repair):

    def __init__(self, methods: list[Repair], weights: list[int]):
        super().__init__()
        self.methods = methods
        self.weights = weights

    def repair(self, destroyed: SeqToken) -> Program:
        method = random.choices(self.methods, weights=self.weights, k=1)[0]

        return method.repair(destroyed)

    def repair_sequence(self, seq: SequenceToken) -> SeqToken:
        pass

    def set_token_libraries(self, env_tokens: set[EnvToken], bool_tokens: set[BoolToken]):
        self.env_tokens = env_tokens
        self.bool_tokens = bool_tokens

        for m in self.methods:
            m.set_token_libraries(env_tokens, bool_tokens)
            m.cost = self.cost

    def set_seq_cost(self, cost: Callable[[SeqToken], float]):
        for m in self.methods:
            m.set_seq_cost(cost)

    def set_current_cost(self, cost: float):
        for m in self.methods:
            m.set_current_cost(cost)