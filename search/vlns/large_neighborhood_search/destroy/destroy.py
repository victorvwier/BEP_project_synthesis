from common.prorgam import Program
from search.vlns.large_neighborhood_search.tokens.destroyed_token import DestroyedToken
from search.vlns.large_neighborhood_search.tokens.sequence_token import SequenceToken, SeqToken, EmptySequenceToken


class Destroy:
    """Interface for a Destroy method."""

    def destroy(self, solution: Program) -> SeqToken:
        """Destructs a given 'solution'. Returns a SequenceToken containing, among others, DestroyedTokens."""

        if len(solution.sequence) < 3:
            return SequenceToken(
                DestroyedToken(destroyed_token=None),
                SequenceToken(
                    DestroyedToken(destroyed_token=None),
                    EmptySequenceToken()))

        seq = SequenceToken.from_list(solution.sequence)


        return self.destroy_sequence(seq)

    def destroy_sequence(self, seq: SeqToken) -> SeqToken:
        """Destroys a given SequenceToken. Should return the destroyed SequenceToken"""

        raise NotImplementedError()
