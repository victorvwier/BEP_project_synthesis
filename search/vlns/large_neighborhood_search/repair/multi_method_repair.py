import random

from common.tokens.abstract_tokens import EnvToken, BoolToken
from search.vlns.large_neighborhood_search.repair.repair import Repair
from search.vlns.large_neighborhood_search.tokens.sequence_token import SeqToken, SequenceToken


class MultiMethodRepair(Repair):

    def __init__(self, methods: list[Repair], weights: list[int]):
        super().__init__()
        self.methods = methods
        self.weights = weights

    def repair_sequence(self, seq: SequenceToken) -> SeqToken:
        method = random.choices(self.methods, weights=self.weights, k=1)[0]

        return method.repair_sequence(seq)

    def set_token_libraries(self, env_tokens: set[EnvToken], bool_tokens: set[BoolToken]):
        self.env_tokens = env_tokens
        self.bool_tokens = bool_tokens

        for m in self.methods:
            m.set_token_libraries(env_tokens, bool_tokens)
            m.cost = self.cost