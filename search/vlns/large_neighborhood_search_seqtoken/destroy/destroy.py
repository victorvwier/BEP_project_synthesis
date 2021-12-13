from collections import Callable

from common.prorgam import Program
from search.vlns.large_neighborhood_search_seqtoken.tokens.destroyed_token import DestroyedToken
from search.vlns.large_neighborhood_search_seqtoken.tokens.sequence_token import SequenceToken, SeqToken, EmptySequenceToken


class Destroy:
    """Interface for a Destroy method."""

    def __init__(self):
        self.cost: Callable[[SeqToken], float]
        self.cost = lambda p: -1

    def destroy(self, solution: Program) -> SeqToken:
        """Destructs a given 'solution'. Returns a SequenceToken containing, among others, DestroyedTokens."""

        # If a solution has 2 or less tokens return two destroyed token.
        if solution.number_of_tokens(1) < 2:
            return SequenceToken(DestroyedToken(destroyed_token=None),
                                 SequenceToken(DestroyedToken(destroyed_token=None), EmptySequenceToken()))

        seq = SequenceToken.from_list(solution.sequence)

        return self.destroy_sequence(seq)

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        """Destroys a given SequenceToken. Should return the destroyed SequenceToken"""

        raise NotImplementedError()
