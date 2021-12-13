import random

from common.prorgam import Program
from search.vlns.large_neighborhood_search_seqtoken.destroy.destroy import Destroy
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SeqToken, SequenceToken


class MultiMethodDestroy(Destroy):

    def __init__(self, methods: list[Destroy], weights: list[int]):
        self.methods = methods
        self.weights = weights

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        method = random.choices(self.methods, weights=self.weights, k=1)[0]

        return method.destroy_sequence(seq)